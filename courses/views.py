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
from itertools import chain
# Create your views here.


class CoursesDetailOnlineTemplateView(TemplateView):
  
  template_name = 'courses/course_detail_otros.html'

  def get_context_data(self, *args, **kwargs):
    context = super(CoursesDetailOnlineTemplateView, self).get_context_data(*args, **kwargs)
    course_slug = 'online'  # Assuming 'course_slug' is the URL parameter
    course = get_object_or_404(Course, slug=course_slug)
    # video_id = YouTube(course.video_url).video_id
    # course.video_url = f"https://www.youtube.com/embed/{video_id}"
    salsa_basico = Course.objects.filter(is_active=True, title="Salsa Principiantes").annotate(order_priority=Value(-1, output_field=IntegerField()))
    
    other_courses = Course.objects.filter(is_active=True).exclude(title="Salsa Principiantes").annotate(
            order_priority=Case(
                When(schedule="Proximamente", then=Value(1)),  # Los que tienen "Proximamente" tienen menor prioridad
                default=Value(0),  # El resto tiene mayor prioridad
                output_field=IntegerField(),
            )
        ).order_by('order_priority')  # Ordenar por prioridad
        
    combined_qs = list(chain(salsa_basico, other_courses))
    list_course_you_might_like = [c for c in combined_qs if c.pk != course.pk]
    
    context['course'] = course
    context['list_course_you_might_like'] = list_course_you_might_like
   
    
    return context

class CoursesDetailParticularTemplateView(TemplateView):
  
  template_name = 'courses/course_detail_otros.html'

  def get_context_data(self, *args, **kwargs):
    context = super(CoursesDetailParticularTemplateView, self).get_context_data(*args, **kwargs)
    course_slug = 'particulares'  # Assuming 'course_slug' is the URL parameter
    course = get_object_or_404(Course, slug=course_slug)
    # video_id = YouTube(course.video_url).video_id
    # course.video_url = f"https://www.youtube.com/embed/{video_id}"
    salsa_basico = Course.objects.filter(is_active=True, title="Salsa Principiantes").annotate(order_priority=Value(-1, output_field=IntegerField()))
    
    other_courses = Course.objects.filter(is_active=True).exclude(title="Salsa Principiantes").annotate(
            order_priority=Case(
                When(schedule="Proximamente", then=Value(1)),  # Los que tienen "Proximamente" tienen menor prioridad
                default=Value(0),  # El resto tiene mayor prioridad
                output_field=IntegerField(),
            )
        ).order_by('order_priority')  # Ordenar por prioridad
        
    combined_qs = list(chain(salsa_basico, other_courses))
    list_course_you_might_like = [c for c in combined_qs if c.pk != course.pk]
    

    context['course'] = course
    context['list_course_you_might_like'] = list_course_you_might_like
   
    
    return context
  
  
class CoursesDetailEventsTemplateView(TemplateView):
  
  template_name = 'courses/course_detail_otros.html'

  def get_context_data(self, *args, **kwargs):
    context = super(CoursesDetailEventsTemplateView, self).get_context_data(*args, **kwargs)
    course_slug = 'novios-eventos'  # Assuming 'course_slug' is the URL parameter
    course = get_object_or_404(Course, slug=course_slug)
    # video_id = YouTube(course.video_url).video_id
    # course.video_url = f"https://www.youtube.com/embed/{video_id}"
    salsa_basico = Course.objects.filter(is_active=True, title="Salsa Principiantes").annotate(order_priority=Value(-1, output_field=IntegerField()))
    
    other_courses = Course.objects.filter(is_active=True).exclude(title="Salsa Principiantes").annotate(
            order_priority=Case(
                When(schedule="Proximamente", then=Value(1)),  # Los que tienen "Proximamente" tienen menor prioridad
                default=Value(0),  # El resto tiene mayor prioridad
                output_field=IntegerField(),
            )
        ).order_by('order_priority')  # Ordenar por prioridad
        
    combined_qs = list(chain(salsa_basico, other_courses))
    list_course_you_might_like = [c for c in combined_qs if c.pk != course.pk]
    

    context['course'] = course
    context['list_course_you_might_like'] = list_course_you_might_like
   
    
    return context
  
  

class CoursesGroupAllTemplateView(TemplateView):
    template_name = 'courses/courses.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CoursesGroupAllTemplateView, self).get_context_data(*args, **kwargs)
        
        # Obtener el curso "Salsa Cubana Basico" si existe
        salsa_basico = Course.objects.filter(
            is_active=True, 
            title="Salsa Principiantes"
        ).annotate(
            order_priority=Value(-1, output_field=IntegerField())  # Prioridad máxima
        )

        # Obtener el resto de los cursos
        other_courses = Course.objects.filter(is_active=True).exclude(
            title="Salsa Principiantes"
        ).annotate(
            order_priority=Case(
                When(schedule="Proximamente", then=Value(1)),  # Los que tienen "Proximamente" tienen menor prioridad
                default=Value(0),  # El resto tiene mayor prioridad
                output_field=IntegerField(),
            )
        ).order_by('order_priority')  # Ordenar por prioridad

        # Combinar los cursos, colocando "Salsa Cubana Basico" al inicio
        courses = list(salsa_basico) + list(other_courses)

        context['title'] = 'Clases de Baile'
        context['list_courses'] = courses
        
        return context


 
class CoursesDetailTemplateView(TemplateView):
  
  template_name = 'courses/course_detail.html'

  def get_context_data(self, *args, **kwargs):
    context = super(CoursesDetailTemplateView, self).get_context_data(*args, **kwargs)
    course_slug = kwargs.get('course_slug')  # Assuming 'course_slug' is the URL parameter
    course = get_object_or_404(Course.objects.filter(is_active=True), slug=course_slug)

    list_course_you_might_like = Course.objects.filter(is_active=True).exclude(pk=course.pk)
    
    list_course_you_might_like = list_course_you_might_like.filter(is_active=True).annotate(
        order_priority=Case(
            When(schedule="Proximamente", then=Value(1)),  # Los que tienen "Proximamente" tienen menor prioridad
            default=Value(0),  # El resto tiene mayor prioridad
            output_field=IntegerField(),
        )
    ).order_by('order_priority')[:6]  # Seleccionar los primeros 6 registros
    

    context['course'] = course
    print('entroooooooooooooo', course.body_title)
    context['list_course_you_might_like'] = list_course_you_might_like
    
    return context
   

  
   