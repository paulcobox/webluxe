from django.shortcuts import render, redirect
from .forms import BasicInfoForm, AdditionalInfoForm
from .models import CastingRegistration
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Lead
from courses.models import Course
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Create your views here.

@csrf_exempt
def create_lead(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        course_of_interest_id = request.POST.get('course_of_interest')
        notes = request.POST.get('notes')
        course_of_interest = request.POST.get('course_of_interest')
        # utm_source = request.POST.get('utm_source')
        # utm_medium = request.POST.get('utm_medium')
        # utm_campaign = request.POST.get('utm_campaign')
        # utm_term = request.POST.get('utm_term')
        # utm_content = request.POST.get('utm_content')
        # referer = request.POST.get('referer')
        # user_agent = request.POST.get('user_agent')

        
        if course_of_interest:
            course_of_interest = Course.objects.get(title=str(course_of_interest))
        else:
            course_of_interest = None

        lead = Lead.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            course_of_interest=course_of_interest,
            notes=notes
            # utm_source=utm_source,
            # utm_medium=utm_medium,
            # utm_campaign=utm_campaign,
            # utm_term=utm_term,
            # utm_content=utm_content,
            # referer=referer,
            # user_agent=user_agent
        )
        
        # Enviar correo de aviso al admin
        subject = f"Nuevo lead registrado: {first_name} {last_name}"
        context = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone_number': phone_number,
            'course_of_interest': course_of_interest.title if course_of_interest else "No especificado",
            'notes': notes,
            # 'referer': referer,
            # 'user_agent': user_agent,
            'created_date': lead.created_date,
        }
        html_message = render_to_string('emails/new_lead_notification.html', context)
        plain_message = strip_tags(html_message)  # Versión en texto plano del correo
        from_email = "Cuban Groove <info@cubangrooveperu.com>"  # Remitente
        to_email = ["paulcofiis@gmail.com"]  # Tu dirección de correo para recibir el aviso

        # Enviar el correo
        # send_mail(
        #     subject,
        #     plain_message,
        #     from_email,
        #     to_email,
        #     html_message=html_message,  # Enviar el correo en formato HTML
        # )

        # Enviar correo de confirmación al cliente
        subject_client = f"¡Gracias por contactarnos, {first_name}!"
        context_client = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone_number': phone_number,
            'course_of_interest': course_of_interest.title if course_of_interest else "No especificado",
            'notes': notes,
        }
        html_message_client = render_to_string('emails/lead_confirmation.html', context_client)
        plain_message_client = strip_tags(html_message_client)  # Versión en texto plano del correo
        to_email_client = [email]  # Correo del cliente

        send_mail(
            subject_client,
            plain_message_client,
            from_email,
            to_email_client,
            html_message=html_message_client,  # Enviar el correo en formato HTML
        )
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})



def casting_registration(request):
    if request.method == 'POST':
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