from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Course
from webluxe.utils import get_actual_date
from django.shortcuts import get_object_or_404
import calendar
from random import sample
# Create your views here.

class CoursesVirtualTemplateView(TemplateView):
  template_name = 'courses/courses.html'

  def get_context_data(self, *args, **kwargs):
    context = super(CoursesVirtualTemplateView, self).get_context_data(*args, **kwargs)
    courses =  Course.objects.filter(is_active = True, type = "Virtual").all()
    context['title'] = 'CLASE DE BAILE VIRTUALES'
    context['list_courses'] = courses
    
    return context

class CoursesPersonalTemplateView(TemplateView):
  template_name = 'courses/courses.html'

  def get_context_data(self, *args, **kwargs):
    context = super(CoursesPersonalTemplateView, self).get_context_data(*args, **kwargs)
    courses =  Course.objects.filter(is_active = True, type = "Personalizada").all()
    context['title'] = 'CLASES DE BAILE PERSONALIZADAS'
    context['list_courses'] = courses
    
    return context

class CoursesGroupTemplateView(TemplateView):
  template_name = 'courses/courses.html'

  def get_context_data(self, *args, **kwargs):
    context = super(CoursesGroupTemplateView, self).get_context_data(*args, **kwargs)
    courses =  Course.objects.filter(is_active = True, type = "Grupal").all()
    context['title'] = 'CLASES DE BAILE GRUPALES'
    context['list_courses'] = courses
    
    return context

class CoursesChoreographyTemplateView(TemplateView):
  template_name = 'courses/courses.html'

  def get_context_data(self, *args, **kwargs):
    context = super(CoursesChoreographyTemplateView, self).get_context_data(*args, **kwargs)
    courses =  Course.objects.filter(is_active = True, type = "Coreografia").all()
    context['title'] = 'COREOGRAFIAS PARA EVENTOS'
    context['list_courses'] = courses
    
    return context

  
class CoursesDetailTemplateView(TemplateView):
  
  template_name = 'courses/course_detail.html'

  def get_context_data(self, *args, **kwargs):
    context = super(CoursesDetailTemplateView, self).get_context_data(*args, **kwargs)
    course_slug = kwargs.get('course_slug')  # Assuming 'course_slug' is the URL parameter
    course = get_object_or_404(Course.objects.filter(is_active=True), slug=course_slug)

    list_course_you_might_like = Course.objects.filter(is_active=True).exclude(pk=course.pk)
    # Select 3 random courses (if there are at least 3 active courses)
    if list_course_you_might_like.count() >= 3:
        list_course_you_might_like = sample(list(list_course_you_might_like), 3)


    context['course'] = course
    context['list_course_you_might_like'] = list_course_you_might_like
   
    
    return context
  
   