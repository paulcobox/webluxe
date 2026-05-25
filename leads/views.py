import logging
import requests
import threading
botlog = logging.getLogger("bot_protection")
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BasicInfoForm, AdditionalInfoForm
from .models import CastingRegistration, Lead
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from courses.models import Course
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.cache import cache
from .tasks import schedule_email_sequence


# Create your views here.
def validate_recaptcha(token, ip="unknown"):
    url = "https://www.google.com/recaptcha/api/siteverify"

    payload = {
        'secret': settings.RECAPTCHA_SECRET_KEY,
        'response': token
    }

    try:
        response = requests.post(url, data=payload)
        result = response.json()

        # Registrar resultado completo
        botlog.info(f"[RECAPTCHA] Resultado: {result} | IP={ip}")

        score = result.get("score", 0)
        success = result.get("success", False)

        # Registrar score y estado
        botlog.info(f"[RECAPTCHA] Score={score} | Success={success} | IP={ip}")

        # Criterio de aprobación
        if success and score >= 0.5:
            botlog.info(f"[RECAPTCHA] ✔️ Aprobado | Score={score} | IP={ip}")
            return True
        else:
            botlog.info(f"[RECAPTCHA] ❌ Rechazado | Score={score} | IP={ip}")
            return False

    except Exception as e:
        botlog.error(f"[RECAPTCHA] ❌ ERROR al validar | {str(e)} | IP={ip}")
        return False

def get_client_ip(request):
    """Obtiene la IP real del cliente incluso detrás de proxies/NGINX."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # Puede venir "IP1, IP2, IP3", tomamos la primera
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')

    # Si por alguna razón viene vacío, lo evitamos
    if not ip:
        ip = "unknown"

    return ip

@csrf_exempt
def create_lead(request):

    # === Log inicio del request ===
    ip = get_client_ip(request)
    ua = request.META.get('HTTP_USER_AGENT', 'unknown')
    botlog.info(f"[REQUEST] Nuevo intento | IP={ip} | UA={ua}")

    if request.method == 'POST':

        # =====================================================
        # 1️⃣ Validación reCAPTCHA
        # =====================================================
        recaptcha_token = request.POST.get("recaptcha_token")
        botlog.info(f"[RECAPTCHA] Token recibido: {str(recaptcha_token)[:25]}... | IP={ip}")

        if not validate_recaptcha(recaptcha_token, ip):
            botlog.info(f"[RECAPTCHA] ❌ INVALIDO | IP={ip}")
            return JsonResponse({'success': False, 'error': 'invalid_recaptcha'})

        botlog.info(f"[RECAPTCHA] ✔️ VALIDO | IP={ip}")

        # =====================================================
        # 2️⃣ HONEYPOT
        # =====================================================
        if request.POST.get("website"):
            botlog.info(f"[HONEYPOT] 🚨 BOT DETECTADO | IP={ip} | website llenado")
            return JsonResponse({'success': False, 'error': 'bot_detected'})

        # =====================================================
        # 3️⃣ RATE LIMIT
        # =====================================================
        key = f"lead_attempts_{ip}"
        attempts = cache.get(key, 0) + 1
        cache.set(key, attempts, 60)

        botlog.info(f"[RATE LIMIT] IP={ip} lleva {attempts} intentos en 60s")

        if attempts > 2:
            botlog.info(f"[RATE LIMIT] 🚨 EXCEDIDO | IP={ip}")
            return JsonResponse({'success': False, 'error': 'rate_limited'})

        # =====================================================
        # 4️⃣ DATOS DEL LEAD
        # =====================================================
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        notes = request.POST.get('notes')
        course_title = request.POST.get('course_of_interest')

        utm_source = request.POST.get('utm_source')
        utm_medium = request.POST.get('utm_medium')
        utm_campaign = request.POST.get('utm_campaign')
        utm_term = request.POST.get('utm_term')
        utm_content = request.POST.get('utm_content')
        referer = request.POST.get('referer')
        user_agent = request.POST.get('user_agent')

        botlog.info(
            f"[LEAD] Datos recibidos | "
            f"Name={first_name} {last_name} | Email={email} | Phone={phone_number} | "
            f"Course={course_title} | IP={ip}"
        )

        # =====================================================
        # 5️⃣ Obtener curso
        # =====================================================
        if course_title:
            try:
                course = Course.objects.get(title=str(course_title))
            except Course.DoesNotExist:
                course = None
                botlog.error(f"[LEAD] ❗ Curso '{course_title}' NO encontrado | IP={ip}")
        else:
            course = None

        # =====================================================
        # 6️⃣ Guardar lead en BD
        # =====================================================
        lead = Lead.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            course_of_interest=course,
            notes=notes,
            utm_source=utm_source,
            utm_medium=utm_medium,
            utm_campaign=utm_campaign,
            utm_term=utm_term,
            utm_content=utm_content,
            referer=referer,
            user_agent=user_agent,
        )

        botlog.info(f"[LEAD] ✔️ Lead guardado con ID={lead.id} | IP={ip}")

        # =====================================================
        # 7️⃣ Enviar correo al admin
        # =====================================================
        subject = f"Nuevo lead registrado: {first_name} {last_name}"
        context = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone_number': phone_number,
            'course_of_interest': course.title if course else "No especificado",
            'notes': notes,
            'utm_source': utm_source,
            'utm_medium': utm_medium,
            'utm_campaign': utm_campaign,
            'utm_term': utm_term,
            'utm_content': utm_content,
            'referer': referer,
            'user_agent': user_agent,
            'created_date': lead.created_date,
        }

        html_message = render_to_string('emails/new_lead_notification.html', context)
        plain_message = strip_tags(html_message)

        send_async_email(
            subject,
            plain_message,
            "Cuban Groove <info@cubangrooveperu.com>",
            ["paulcofiis@gmail.com"],
            html_message=html_message
        )

        # ===============================================
        # 8️⃣ Iniciar secuencia de 9 correos via Celery
        # ===============================================
        schedule_email_sequence(lead)

        return JsonResponse({'success': True})

    botlog.info(f"[REQUEST] ❌ Método NO permitido | IP={ip}")

    return JsonResponse({'success': False})




def send_async_email(subject, plain_message, from_email, to_email, html_message=None):
    def _send():
        send_mail(
            subject,
            plain_message,
            from_email,
            to_email,
            html_message=html_message,
        )
    threading.Thread(target=_send).start()


def casting_registration(request):
    if request.method == 'POST':
        
        # 🔐 Validación reCAPTCHA
        recaptcha_token = request.POST.get("recaptcha_token")
        if not validate_recaptcha(recaptcha_token):
            return JsonResponse({'success': False, 'error': 'invalid_recaptcha'})
        
        # 1️⃣ HONEYPOT anti-bots
        if request.POST.get("website"):
            return JsonResponse({'success': False, 'error': 'bot_detected'})
        
        # 2️⃣ RATE LIMIT por IP (bloqueo de bots en lote)
        ip = request.META.get('REMOTE_ADDR')
        key = f"lead_attempts_{ip}"
        attempts = cache.get(key, 0) + 1
        cache.set(key, attempts, 60)  # ventana de 60 segundos

        if attempts > 2:
            return JsonResponse({'success': False, 'error': 'rate_limited'})
        
        form = BasicInfoForm(request.POST)
        if form.is_valid():
            registration = form.save()
            request.session['registration_id'] = registration.id
            return redirect('additional_info')
    else:
        form = BasicInfoForm()
    return render(request, 'casting/basic_info.html', {'form': form})

def additional_info(request):
    registration_id = request.session.get('registration_id')
    if not registration_id:
        return redirect('casting_registration')
    
    registration = CastingRegistration.objects.get(id=registration_id)
    if request.method == 'POST':
        
        # 🔐 Validación reCAPTCHA
        recaptcha_token = request.POST.get("recaptcha_token")
        if not validate_recaptcha(recaptcha_token):
            return JsonResponse({'success': False, 'error': 'invalid_recaptcha'})
        
        # 1️⃣ HONEYPOT anti-bots
        if request.POST.get("website"):
            return JsonResponse({'success': False, 'error': 'bot_detected'})
        
        # 2️⃣ RATE LIMIT por IP (bloqueo de bots en lote)
        ip = request.META.get('REMOTE_ADDR')
        key = f"lead_attempts_{ip}"
        attempts = cache.get(key, 0) + 1
        cache.set(key, attempts, 60)  # ventana de 60 segundos

        if attempts > 2:
            return JsonResponse({'success': False, 'error': 'rate_limited'})
        
        form = AdditionalInfoForm(request.POST, instance=registration)
        if form.is_valid():
            form.save()
            del request.session['registration_id']
            return redirect('thank_you')
    else:
        form = AdditionalInfoForm(instance=registration)
    return render(request, 'casting/additional_info.html', {'form': form})

def thank_you(request):
    return render(request, 'casting/thank_you.html')


def unsubscribe(request, token):
    lead = get_object_or_404(Lead, unsubscribe_token=token)
    if not lead.unsubscribed:
        lead.unsubscribed = True
        lead.save(update_fields=['unsubscribed'])
    return render(request, 'emails/unsubscribe_confirm.html', {'first_name': lead.first_name})