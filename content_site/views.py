# from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render
from django.views.generic import TemplateView
# from .models import MissionVision
from courses.models import Course
from .models import Invitated, FAQ
from random import sample
from django.http import FileResponse
from django.http import FileResponse, Http404
from django.db.models import Case, When, Value, IntegerField
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from django.template.loader import render_to_string
from collections import defaultdict

import json
import copy
import random
import logging
from urllib.parse import quote
from django.core.mail import send_mail
from django.http import HttpResponse
from smtplib import SMTPException
import socket

logger = logging.getLogger(__name__)


# from instructors.models import Instructors
# Create your views here.
class FAQListView(TemplateView):
    template_name = "content_site/faq.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        faqs = FAQ.objects.filter(is_active=True).order_by('category', 'question')
        
        grouped_faqs = defaultdict(list)
        for faq in faqs:
            grouped_faqs[faq.get_category_display()] += [faq]  # Usa display para nombre legible
        
        context['faqs'] = dict(grouped_faqs)
        return context
    
class HomePageView(TemplateView):
  template_name = 'index.html'
  
  
  def get_context_data(self, *args, **kwargs):
    context = super(HomePageView, self).get_context_data(*args, **kwargs)
    # Anotar prioridad para ordenar los cursos
    # Obtener el curso "Salsa Cubana Basico" si existe
    salsa_basico = Course.objects.filter(is_active=True, title="Salsa Principiantes").annotate(order_priority=Value(-1, output_field=IntegerField()))
    
    other_courses = Course.objects.filter(is_active=True).exclude(title="Salsa Principiantes").annotate(
            order_priority=Case(
                When(schedule="Proximamente", then=Value(1)),  # Los que tienen "Proximamente" tienen menor prioridad
                default=Value(0),  # El resto tiene mayor prioridad
                output_field=IntegerField(),
            )
        ).order_by('order_priority')  # Ordenar por prioridad
        
    list_course_you_might_like = list(salsa_basico) + list(other_courses)
        
    list_course_banner_top =  Course.objects.filter(is_active = True, is_banner_home=True)
    if list_course_banner_top.count() >= 3:
        list_course_banner_top = sample(list(list_course_banner_top), 3)

    # instructors = Instructors.objects.filter(is_active = True)
    
    # context['instructors'] = instructors
    context['list_course_banner_top'] = list_course_banner_top
    context['list_course_you_might_like'] = list_course_you_might_like
    
    return context



class ContactTemplateView(TemplateView):
  template_name = 'content_site/contact.html'

  def get_context_data(self, *args, **kwargs):
    context = super(ContactTemplateView, self).get_context_data(*args, **kwargs)
    context['name'] = 'contact'
    return context

class PrivacyPoliciesTemplateView(TemplateView):
  template_name = 'content_site/privacy_policies.html'

  def get_context_data(self, *args, **kwargs):
    context = super(PrivacyPoliciesTemplateView, self).get_context_data(*args, **kwargs)
    return context

class TermsConditionsTemplateView(TemplateView):
  template_name = 'content_site/terms_conditions.html'

  def get_context_data(self, *args, **kwargs):
    context = super(TermsConditionsTemplateView, self).get_context_data(*args, **kwargs)
    return context

class ThankYouTemplateView(TemplateView):
  template_name = 'content_site/thankyou.html'

  def get_context_data(self, *args, **kwargs):
    context = super(ThankYouTemplateView, self).get_context_data(*args, **kwargs)
    salsa_basico = Course.objects.filter(is_active=True, title="Salsa Principiantes").annotate(order_priority=Value(-1, output_field=IntegerField()))
    
    other_courses = Course.objects.filter(is_active=True).exclude(title="Salsa Principiantes").annotate(
            order_priority=Case(
                When(schedule="Proximamente", then=Value(1)),  # Los que tienen "Proximamente" tienen menor prioridad
                default=Value(0),  # El resto tiene mayor prioridad
                output_field=IntegerField(),
            )
        ).order_by('order_priority')  # Ordenar por prioridad
        
    list_course_you_might_like = list(salsa_basico) + list(other_courses)
    context['list_course_you_might_like'] = list_course_you_might_like
    return context
  
def sitemap_view(request):
    return FileResponse(open('sitemap.xml', 'rb'), content_type='application/xml')  

def sitemap_blog_view(request):
    return FileResponse(open('sitemap-blog.xml', 'rb'), content_type='application/xml')  

def sitemap_general_view(request):
    return FileResponse(open('sitemap-general.xml', 'rb'), content_type='application/xml')  

def sitemap_miraflores_view(request):
    return FileResponse(open('sitemap-miraflores.xml', 'rb'), content_type='application/xml')

def robots_view(request):
    try:
        return FileResponse(open('robots.txt', 'rb'), content_type='text/plain')
    except FileNotFoundError:
        raise Http404("El archivo robots.txt no se encuentra.")
    
class InvitatedTemplateView(TemplateView):
    template_name = "content_site/invitated.html"  # Plantilla con el formulario

    def post(self, request, *args, **kwargs):
        # Obtener datos del formulario
        student_name = request.POST.get("student_name")
        student_email = request.POST.get("student_email")
        friend_name = request.POST.get("friend_name")
        friend_phone = request.POST.get("friend_phone")
        notes = request.POST.get("notes")

        # LÃ³gica para guardar datos en base de datos o procesamiento
        print("Nombre del Alumno:", student_name)
        print("Correo ElectrÃ³nico del Alumno:", student_email)
        print("Nombre del Amigo:", friend_name)
        print("TelÃ©fono del Amigo:", friend_phone)
        print("Clase Seleccionada:", notes)
        # Guardar los datos en el modelo
        
        # Verificar si el amigo ya ha sido registrado
        if Invitated.objects.filter(friend_phone=friend_phone).exists():
            # Mostrar mensaje de error si ya fue registrado
            return render(request, self.template_name, {
                "error_message": "El amigo ya ha sido registrado como invitado y solo puede ser invitado una vez.",
                "student_name": student_name,
                "student_email": student_email,
                "friend_name": friend_name,
                "friend_phone": friend_phone,
                "notes": notes,
            })
            
        Invitated.objects.create(
            student_name=student_name,
            student_email=student_email,
            friend_name=friend_name,
            friend_phone=friend_phone,
            notes=notes,
        )
        
        # Enviar correo de invitaciÃ³n con plantilla HTML
        # self.send_invitation_email(student_name, friend_name, student_email, notes)
        # Redirigir a la pÃ¡gina de Ã©xito
        return redirect(reverse("invite_success"))
    
    def send_aviso_email(self, student_name, friend_name, student_email, notes):
        subject = f"Â¡Lead de {friend_name} a Cuban Groove!"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [student_email, 'paulcofiis@gmail.com', '']

        # Renderizar la plantilla HTML para el correo
        html_content = render_to_string("emails/invitation_email.html", {
            "friend_name": friend_name,
            "notes": notes,
        })

        email = EmailMultiAlternatives(subject, "", from_email, recipient_list)
        email.attach_alternative(html_content, "text/html")
        email.send()
        

        


def test_email(request):
    try:
        send_mail(
            "Correo de prueba",
            "Este es un correo de prueba desde Django con Gmail.",
            "Cuban Groove <info@cubangrooveperu.com>",  # Remitente
            ["paulcofiis@gmail.com"],  # Destinatario
            fail_silently=False,
        )
        return HttpResponse("Correo enviado correctamente")
    except SMTPException as e:
        # Captura errores especÃ­ficos de SMTP
        error_message = f"Error SMTP al enviar el correo: {str(e)}"
        logger.error(error_message)  # Registra el error en los logs
        return HttpResponse(error_message, status=500)
    except socket.error as e:
        # Captura errores de conexiÃ³n (por ejemplo, problemas de red)
        error_message = f"Error de conexiÃ³n: {str(e)}"
        logger.error(error_message)  # Registra el error en los logs
        return HttpResponse(error_message, status=500)
    except Exception as e:
        # Captura cualquier otro error inesperado
        error_message = f"Error inesperado: {str(e)}"
        logger.error(error_message)  # Registra el error en los logs
        return HttpResponse(error_message, status=500)
              
class InvitatedSuccessTemplateView(TemplateView):
    template_name = "content_site/invitated_success.html"  # Plantilla de la pÃ¡gina de Ã©xito


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# THANK YOU â€” LEAD ADS FACEBOOK
# PÃ¡gina de agradecimiento post-formulario de Lead Ads.
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
class ThankyouLeadAdsView(TemplateView):
    template_name = 'landing/thankyou_lead_ads.html'

    def get_context_data(self, **kwargs):
        import random
        context = super().get_context_data(**kwargs)
        from content_site.models import Testimony
        testimonies = list(Testimony.objects.filter(is_active=True))
        random.shuffle(testimonies)
        context.update({
            'hero_image_url': 'https://images.unsplash.com/photo-1545959570-a94084071b5d?w=1400&q=80',
            'list_testimony': testimonies,
        })
        return context


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# LANDING META ADS â€” JUNIO 2026
# Para actualizar precios, vacantes u horarios edita solo esta clase.
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
class LandingMetaAdsJun2026View(TemplateView):
    template_name = 'landing/meta_ads_jun2026.html'

    # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
    # EDITAR AQUI: precios, horarios, vacantes, bullets
    # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
    REF_MIRAFLORES = 'Miraflores Â· 1 cdra. Parque Kennedy'

    RAICES_CUBANAS = {
        'name': 'Raices Cubanas',
        'tagline': 'Rumba y Danzas Afrocubanas â€” complementa cualquier nivel',
        'schedule': 'Sabados', 'time': '4:30 pm â€“ 6:00 pm',
        'ref': 'Miraflores Â· 1 cdra. Parque Kennedy',
    }

    PROGRAMS = {
        'basico': {
            'id': 'basico',
            'name': 'Salsa Cubana Basico',
            'tagline': 'Construye tu base con tecnica y confianza',
            'benefits': [
                'Coordinacion y musicalidad desde cero',
                'Pasos libres y tecnica corporal',
                'Introduccion al trabajo en pareja',
            ],
            'sedes': [
                {
                    'id': 'viernes', 'name': 'Viernes',
                    'schedule': 'Viernes', 'time': '8:00 pm â€“ 10:00 pm',
                    'ref': 'Miraflores Â· 1 cdra. Parque Kennedy',
                    'vacantes': 4,
                },
                {
                    'id': 'sabado', 'name': 'Sabado',
                    'schedule': 'Sabado', 'time': '3:00 pm â€“ 4:30 pm',
                    'ref': 'Miraflores Â· 1 cdra. Parque Kennedy',
                    'vacantes': 3,
                },
            ],
            'raices_addon': True,
            'timba_addon': False,
        },
        'intermedio': {
            'id': 'intermedio',
            'name': 'Salsa Cubana Intermedio',
            'tagline': 'Potencia tu tecnica, musicalidad y presencia',
            'benefits': [
                'Musicalidad aplicada y control corporal',
                'Pasos libres, variaciones y energia',
                'Fluidez y seguridad al bailar',
            ],
            'sedes': [
                {
                    'id': 'martes', 'name': 'Martes',
                    'schedule': 'Martes', 'time': '8:00 pm â€“ 10:00 pm',
                    'ref': 'Miraflores Â· 1 cdra. Parque Kennedy',
                    'vacantes': 5,
                },
            ],
            'raices_addon': True,
            'timba_addon': False,
        },
        'ladyStyle': {
            'id': 'ladyStyle',
            'name': 'Cuban Lady Style',
            'tagline': 'Tecnica, sensualidad y presencia escenica',
            'benefits': [
                'Tecnica femenina y movimiento corporal',
                'Brazos, lineas, expresion y musicalidad',
                'Seguridad y proyeccion escenica',
            ],
            'sedes': [
                {
                    'id': 'jueves', 'name': 'Jueves',
                    'schedule': 'Jueves', 'time': '8:00 pm â€“ 10:00 pm',
                    'ref': 'Miraflores Â· 1 cdra. Parque Kennedy',
                    'vacantes': 6,
                },
            ],
            'raices_addon': True,
            'timba_addon': True,
        },
        'timbafusion': {
            'id': 'timbafusion',
            'name': 'Timba Fusion y Reparto',
            'tagline': 'Sabor, actitud y flow urbano cubano',
            'benefits': [
                'Primera hora: pasos sueltos fusionados con Timba moderna',
                'Segunda hora: pasos sueltos de Reparto',
                'Coordinacion, flow, actitud e interpretacion musical',
            ],
            'sedes': [
                {
                    'id': 'sabado', 'name': 'Sabado',
                    'schedule': 'Sabado', 'time': '6:00 pm â€“ 7:30 pm',
                    'ref': 'Miraflores Â· 1 cdra. Parque Kennedy',
                    'vacantes': 4,
                },
            ],
            'raices_addon': False,
            'timba_addon': False,
        },
        'privadas': {
            'id': 'privadas',
            'name': 'Clases Privadas',
            'tagline': 'Atencion 100% personalizada para ti',
            'benefits': [
                'Progreso personalizado a tu ritmo',
                'Horarios totalmente flexibles',
                'Correccion tecnica inmediata',
            ],
            'sedes': [
                {
                    'id': 'coordinar', 'name': 'A coordinar',
                    'schedule': 'A coordinar', 'time': 'Horario flexible',
                    'ref': 'Miraflores Â· 1 cdra. Parque Kennedy',
                    'vacantes': None,
                },
            ],
            'raices_addon': False,
            'timba_addon': False,
        },
    }

    def _programs_with_random_vacantes(self):
        programs = copy.deepcopy(self.PROGRAMS)
        for prog in programs.values():
            for sede in prog['sedes']:
                if sede['vacantes'] is not None:
                    sede['vacantes'] = random.randint(2, 4)
        return programs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from content_site.models import Testimony
        testimonies = list(Testimony.objects.filter(is_active=True))
        random.shuffle(testimonies)
        context.update({
            'hero_image_url':  'https://images.unsplash.com/photo-1545959570-a94084071b5d?w=1400&q=80',
            'stats_count':     '500+',
            'stats_label':     'alumnos formados',
            'programs_json':   json.dumps(self._programs_with_random_vacantes()),
            'raices_json':     json.dumps(self.RAICES_CUBANAS),
            'whatsapp_number': '51933275831',
            'list_testimony':  testimonies,
        })
        return context


# def test_email(request):
#     try:
#         send_mail(
#             'Correo de prueba',
#             'Este es un correo de prueba enviado desde Django usando Gmail.',
#             'cubangroove.pe@gmail.com',  # Desde
#             ['paulcofiis@gmail.com'],  # Cambia a un correo de prueba
#             fail_silently=False,
#         )
#         return HttpResponse('Correo enviado con Ã©xito.')
#     except Exception as e:
#         return HttpResponse(f'Error al enviar el correo: {e}')

# class AboutMisionVisionValuesTemplateView(TemplateView):
#   template_name = 'content_site/about_mision_vision.html'

#   def get_context_data(self, *args, **kwargs):
#     context = super(AboutMisionVisionValuesTemplateView, self).get_context_data(*args, **kwargs)
#     mision =  MissionVision.objects.filter(is_active = True, type = "Mision").first()
#     vision = MissionVision.objects.filter(is_active = True, type = "Vision").first()
    

#     context['name'] = 'about_mision_vision'
#     if mision:
#       context['mision'] = mision
#       context['mision_tags'] = mision.tags.split(",")
#     if vision:
#       context['vision'] = vision
#       context['vision_tags'] = vision.tags.split(",")
    
#     return context


# class AboutOurPartnerTemplateView(TemplateView):
#   template_name = 'content_site/about_our_partner.html'

#   def get_context_data(self, *args, **kwargs):
#     context = super(AboutOurPartnerTemplateView, self).get_context_data(*args, **kwargs)
#     context['name'] = 'about_our_partner'
#     return context

