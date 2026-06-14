import logging
import requests
import threading
logger = logging.getLogger(__name__)
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
from .tasks import schedule_email_sequence, send_capi_lead_event


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

        # Datos del wizard (landing Meta Ads)
        form_experience_raw = request.POST.get('form_experience_raw', '')
        form_motivation_raw = request.POST.get('form_motivation_raw', '')
        form_course_raw     = request.POST.get('form_course_raw', '')
        form_schedule_raw   = request.POST.get('form_schedule_raw', '')
        form_age_raw        = request.POST.get('form_age_raw', '')

        utm_source = request.POST.get('utm_source')
        utm_medium = request.POST.get('utm_medium')
        utm_campaign = request.POST.get('utm_campaign')
        utm_term = request.POST.get('utm_term')
        utm_content = request.POST.get('utm_content')
        referer = request.POST.get('referer')
        user_agent = request.POST.get('user_agent')
        meta_event_id = request.POST.get('meta_event_id', '')

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
            email=email or '',
            phone_number=phone_number,
            course_of_interest=course,
            notes=notes,
            form_experience_raw=form_experience_raw,
            form_motivation_raw=form_motivation_raw,
            form_course_raw=form_course_raw,
            form_schedule_raw=form_schedule_raw,
            form_age_raw=form_age_raw,
            utm_source=utm_source,
            utm_medium=utm_medium,
            utm_campaign=utm_campaign,
            utm_term=utm_term,
            utm_content=utm_content,
            referer=referer,
            user_agent=user_agent,
            meta_event_id=meta_event_id,
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

        # ===============================================
        # 9️⃣ Enviar evento Lead a Meta CAPI (server-side)
        # ===============================================
        send_capi_lead_event.apply_async(
            args=[lead.id, ip, user_agent or request.META.get('HTTP_USER_AGENT', '')]
        )

        return JsonResponse({'success': True, 'lead_id': lead.id})

    botlog.info(f"[REQUEST] ❌ Método NO permitido | IP={ip}")

    return JsonResponse({'success': False})


def update_lead_sede(request):
    """Actualiza la sede elegida en un lead existente. Llamado en background desde el CTA de WhatsApp."""
    if request.method != 'POST':
        return JsonResponse({'success': False})

    lead_id = request.POST.get('lead_id')
    sede    = request.POST.get('sede', '').strip()
    horario = request.POST.get('horario', '').strip()

    if not lead_id:
        return JsonResponse({'success': False})

    try:
        lead = Lead.objects.get(id=lead_id)
        lead.form_schedule_raw = f"{sede} — {horario}" if horario else sede
        lead.save(update_fields=['form_schedule_raw', 'modified_date'])
        botlog.info(f"[LEAD] Sede actualizada ID={lead_id} | Sede={sede} | Horario={horario}")

        if lead.kommo_contact_id:
            try:
                from leads.tasks import sync_lead_to_kommo
                sync_lead_to_kommo.apply_async(args=[lead.id])
            except Exception as e:
                logger.error(f'[KOMMO] Error al programar sync de sede para lead {lead_id}: {e}')

        return JsonResponse({'success': True})
    except Lead.DoesNotExist:
        botlog.warning(f"[LEAD] update_lead_sede — ID={lead_id} no encontrado")
        return JsonResponse({'success': False})




@csrf_exempt
def kommo_webhook_contact_created(request):
    """
    Receptor del webhook de Kommo cuando se crea un nuevo contacto.
    Kommo envía application/x-www-form-urlencoded.
    Por ahora: imprime en consola el payload completo y busca el teléfono del contacto.
    """
    if request.method != 'POST':
        return JsonResponse({'success': False}, status=405)

    # ── DEBUG: imprimir payload completo ──────────────────────────
    print('=' * 60)
    print('[KOMMO WEBHOOK] Nuevo evento recibido')
    print(f'  Content-Type : {request.content_type}')
    print(f'  GET params   : {dict(request.GET)}')
    print('  POST data completo:')
    for key, value in request.POST.items():
        print(f'    {key} = {value}')
    print('=' * 60)
    # ──────────────────────────────────────────────────────────────

    from leads.services.kommo_service import (
        extract_phone_from_webhook_payload,
        update_kommo_contact,
        create_kommo_deal,
        normalize_phone,
    )
    from django.utils import timezone

    # 1. Extraer contact_id
    contact_id = request.POST.get('contacts[add][0][id]')
    if not contact_id:
        print('[KOMMO WEBHOOK] ⚠️  No se encontró contact_id — ignorando evento')
        return JsonResponse({'success': True})

    # 2. Extraer teléfono del payload (sin llamada extra a Kommo)
    phone = extract_phone_from_webhook_payload(dict(request.POST))
    print(f'[KOMMO WEBHOOK] contact_id={contact_id} | teléfono extraído={phone}')

    if not phone:
        print('[KOMMO WEBHOOK] ⚠️  Sin teléfono en payload — ignorando evento')
        return JsonResponse({'success': True})

    # 3. Buscar Lead en BD por teléfono normalizado
    phone_normalized = normalize_phone(phone)
    lead = None
    for candidate in Lead.objects.filter(kommo_contact_id=None).order_by('-created_date'):
        if normalize_phone(candidate.phone_number or '') == phone_normalized:
            lead = candidate
            break

    if not lead:
        print(f'[KOMMO WEBHOOK] ℹ️  Sin Lead en BD para teléfono={phone_normalized} — nada que actualizar')
        return JsonResponse({'success': True})

    print(f'[KOMMO WEBHOOK] ✅ Lead encontrado: ID={lead.id} | {lead.first_name} {lead.last_name}')

    # 4. Guardar kommo_contact_id en el lead
    lead.kommo_contact_id = contact_id
    lead.save(update_fields=['kommo_contact_id'])

    # 5. Actualizar contacto en Kommo con datos del form
    all_data = {
        'curso':        lead.form_course_raw or '',
        'experiencia':  lead.form_experience_raw or '',
        'objetivo':     lead.form_motivation_raw or '',
        'sede_horario': lead.form_schedule_raw or '',
        'utm_campaign': lead.utm_campaign or '',
        'utm_source':   lead.utm_source or '',
        'utm_content':  lead.utm_content or '',
        'rango_edad':   lead.form_age_raw or '',
    }
    update_kommo_contact(contact_id, all_data)
    print(f'[KOMMO WEBHOOK] ✅ Contacto {contact_id} actualizado en Kommo')

    # 6. Crear deal si aún no existe
    if not lead.kommo_deal_id:
        full_name = f'{lead.first_name} {lead.last_name}'.strip()
        deal_name = f"{full_name or phone_normalized} — {lead.form_course_raw or 'Consulta'}".strip(' —')
        deal_id = create_kommo_deal(contact_id, deal_name)
        if deal_id:
            lead.kommo_deal_id = deal_id
            lead.save(update_fields=['kommo_deal_id'])
            print(f'[KOMMO WEBHOOK] ✅ Deal creado: ID={deal_id}')

    # 7. Marcar sync
    lead.kommo_synced_at  = timezone.now()
    lead.kommo_last_error = None
    lead.save(update_fields=['kommo_synced_at', 'kommo_last_error'])

    print(f'[KOMMO WEBHOOK] ✅ Lead {lead.id} sincronizado completamente')
    return JsonResponse({'success': True})


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