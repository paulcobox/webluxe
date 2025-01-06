# from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render
from django.views.generic import TemplateView
# from .models import MissionVision
from courses.models import Course
from .models import Invitated
from random import sample
from django.http import FileResponse
from django.http import FileResponse, Http404
from django.db.models import Case, When, Value, IntegerField
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from django.template.loader import render_to_string
# from django.core.mail import send_mail
from django.http import HttpResponse
# from instructors.models import Instructors
# Create your views here.

class HomePageView(TemplateView):
  template_name = 'index.html'
  
  
  def get_context_data(self, *args, **kwargs):
    context = super(HomePageView, self).get_context_data(*args, **kwargs)
    # Anotar prioridad para ordenar los cursos
    list_course_you_might_like = Course.objects.filter(is_active=True).annotate(
        order_priority=Case(
            When(schedule="Proximamente", then=Value(1)),  # Los que tienen "Proximamente" tienen menor prioridad
            default=Value(0),  # El resto tiene mayor prioridad
            output_field=IntegerField(),
        )
    ).order_by('order_priority')[:6]  # Seleccionar los primeros 6 registros
    
    # # Select 6 random courses (if there are at least 3 active courses)
    # if list_course_you_might_like.count() >= 6:
    #     list_course_you_might_like = sample(list(list_course_you_might_like), 6)
        
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
    list_course_you_might_like = Course.objects.filter(is_active=True).annotate(
        order_priority=Case(
            When(schedule="Proximamente", then=Value(1)),  # Los que tienen "Proximamente" tienen menor prioridad
            default=Value(0),  # El resto tiene mayor prioridad
            output_field=IntegerField(),
        )
    ).order_by('order_priority')[:6]  # Seleccionar los primeros 6 registros
    context['list_course_you_might_like'] = list_course_you_might_like
    return context
  
def sitemap_view(request):
    return FileResponse(open('sitemap.xml', 'rb'), content_type='application/xml')

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

        # Lógica para guardar datos en base de datos o procesamiento
        print("Nombre del Alumno:", student_name)
        print("Correo Electrónico del Alumno:", student_email)
        print("Nombre del Amigo:", friend_name)
        print("Teléfono del Amigo:", friend_phone)
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
        
        # Enviar correo de invitación con plantilla HTML
        # self.send_invitation_email(student_name, friend_name, student_email, notes)
        # Redirigir a la página de éxito
        return redirect(reverse("invite_success"))
    
    # def send_invitation_email(self, student_name, friend_name, student_email, notes):
    #     subject = f"¡{student_name} Ha invitado a {friend_name} a Cuban Groove!"
    #     from_email = settings.DEFAULT_FROM_EMAIL
    #     recipient_list = [student_email, 'paulcofiis@gmail.com']

    #     # Renderizar la plantilla HTML para el correo
    #     html_content = render_to_string("emails/invitation_email.html", {
    #         "student_name": student_name,
    #         "friend_name": friend_name,
    #         "notes": notes,
    #     })

        # Crear y enviar el correo
        # email = EmailMultiAlternatives(subject, "", from_email, recipient_list)
        # email.attach_alternative(html_content, "text/html")
        # email.send()
        
class InvitatedSuccessTemplateView(TemplateView):
    template_name = "content_site/invitated_success.html"  # Plantilla de la página de éxito
    
# def test_email(request):
#     try:
#         send_mail(
#             'Correo de prueba',
#             'Este es un correo de prueba enviado desde Django usando Gmail.',
#             'cubangroove.pe@gmail.com',  # Desde
#             ['paulcofiis@gmail.com'],  # Cambia a un correo de prueba
#             fail_silently=False,
#         )
#         return HttpResponse('Correo enviado con éxito.')
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
