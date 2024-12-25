from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Course
from webluxe.utils import get_actual_date
from django.shortcuts import get_object_or_404
import calendar
from random import sample
from leads.models import Lead
from pytube import YouTube
from django.db.models import Case, When, Value, IntegerField
# Create your views here.

class CoursesVirtualTemplateView(TemplateView):
  template_name = 'courses/courses.html'

  def get_context_data(self, *args, **kwargs):
    context = super(CoursesVirtualTemplateView, self).get_context_data(*args, **kwargs)
    courses =  Course.objects.filter(is_active = True, type = "Virtual").all()
    
    list_course_you_might_like = Course.objects.filter(is_active=True).exclude(id__in=courses.values_list('id', flat=True))
    if list_course_you_might_like.count() >= 3:
      list_course_you_might_like = sample(list(list_course_you_might_like), 3)

    context['list_course_you_might_like'] = list_course_you_might_like
    
    context['title'] = 'Clases de Baile Virtual'
    context['list_courses'] = courses
    
    return context

class CoursesPersonalTemplateView(TemplateView):
  template_name = 'courses/courses.html'

  def get_context_data(self, *args, **kwargs):
    context = super(CoursesPersonalTemplateView, self).get_context_data(*args, **kwargs)
    courses =  Course.objects.filter(is_active = True, type = "Personalizada").all()
    
    list_course_you_might_like = Course.objects.filter(is_active=True).exclude(id__in=courses.values_list('id', flat=True))
    if list_course_you_might_like.count() >= 3:
      list_course_you_might_like = sample(list(list_course_you_might_like), 3)

    context['list_course_you_might_like'] = list_course_you_might_like
    
    context['title'] = 'Clases de Baile Personalizadas'
    context['list_courses'] = courses
    
    return context

class CoursesGroupAllTemplateView(TemplateView):
  template_name = 'courses/courses.html'

  def get_context_data(self, *args, **kwargs):
    context = super(CoursesGroupAllTemplateView, self).get_context_data(*args, **kwargs)
   
    # Anotar prioridad para ordenar los cursos
    courses = Course.objects.filter(is_active=True).annotate(
        order_priority=Case(
            When(schedule="Proximamente", then=Value(1)),  # Los que tienen "Proximamente" tienen menor prioridad
            default=Value(0),  # El resto tiene mayor prioridad
            output_field=IntegerField(),
        )
    ).order_by('order_priority')  # Ordenar por prioridad

    # context['list_course_you_might_like'] = list_course_you_might_like
    context['title'] = 'Clases de Baile'
    context['list_courses'] = courses
    
    return context



class CoursesGroupTemplateView(TemplateView):
  template_name = 'courses/courses.html'

  def get_context_data(self, *args, **kwargs):
    context = super(CoursesGroupTemplateView, self).get_context_data(*args, **kwargs)
    courses =  Course.objects.filter(is_active = True, type = "Grupal").all()
    
    list_course_you_might_like = Course.objects.filter(is_active=True).exclude(id__in=courses.values_list('id', flat=True))
    if list_course_you_might_like.count() >= 3:
      list_course_you_might_like = sample(list(list_course_you_might_like), 3)

    context['list_course_you_might_like'] = list_course_you_might_like
    context['title'] = 'Clases de Baile en Grupo'
    context['list_courses'] = courses
    
    return context

class CoursesChoreographyTemplateView(TemplateView):
  template_name = 'courses/courses.html'

  def get_context_data(self, *args, **kwargs):
    context = super(CoursesChoreographyTemplateView, self).get_context_data(*args, **kwargs)
    courses =  Course.objects.filter(is_active = True, type = "Coreografia").all()
    
    list_course_you_might_like = Course.objects.filter(is_active=True).exclude(id__in=courses.values_list('id', flat=True))
    if list_course_you_might_like.count() >= 3:
      list_course_you_might_like = sample(list(list_course_you_might_like), 3)

    context['list_course_you_might_like'] = list_course_you_might_like
    
    context['title'] = 'Coreografias para Eventos (Concursos, Matrimonios, Empresas, Etc)'
    context['list_courses'] = courses
    
    return context

  
class CoursesDetailTemplateView(TemplateView):
  
  template_name = 'courses/course_detail.html'

  def get_context_data(self, *args, **kwargs):
    context = super(CoursesDetailTemplateView, self).get_context_data(*args, **kwargs)
    course_slug = kwargs.get('course_slug')  # Assuming 'course_slug' is the URL parameter
    course = get_object_or_404(Course.objects.filter(is_active=True), slug=course_slug)
    # video_id = YouTube(course.video_url).video_id
    # course.video_url = f"https://www.youtube.com/embed/{video_id}"
    list_course_you_might_like = Course.objects.filter(is_active=True).exclude(pk=course.pk)
    
    list_course_you_might_like = list_course_you_might_like.filter(is_active=True).annotate(
        order_priority=Case(
            When(schedule="Proximamente", then=Value(1)),  # Los que tienen "Proximamente" tienen menor prioridad
            default=Value(0),  # El resto tiene mayor prioridad
            output_field=IntegerField(),
        )
    ).order_by('order_priority')[:6]  # Seleccionar los primeros 6 registros
    

    context['course'] = course
    context['list_course_you_might_like'] = list_course_you_might_like
   
    
    return context
  
   