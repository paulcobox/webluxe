from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Course, Testimony
from webluxe.utils import get_actual_date
from django.shortcuts import get_object_or_404
import calendar
from random import sample
# Create your views here.

class CoursesVirtualTemplateView(TemplateView):
  template_name = 'courses/courses.html'

  def get_context_data(self, *args, **kwargs):
    month = get_actual_date().month
    context = super(CoursesVirtualTemplateView, self).get_context_data(*args, **kwargs)
    page_course = self.request.GET.get('page_course')
    courses =  Course.objects.filter(is_active = True, type = "Virtual", month__gte = month).all()
    list_courses_by_month = []
    list_courses = []
    dict_courses_by_month = {}

    months= list(courses.order_by().distinct().values_list('month', flat=True))

    for month in months:
      for course in courses:
        if month == course.month:
          list_courses.append(course)

      dict_courses_by_month = {
        'month' : month,
        'month_name': str(calendar.month_name[int(month)]).capitalize(),
        'courses' : list_courses
      }
      list_courses_by_month.append(dict_courses_by_month)

    context['title'] = 'CURSOS VIRTUALES'
    context['list_courses_by_month'] = list_courses_by_month
    
    return context

class CoursesFaceTemplateView(TemplateView):
  template_name = 'courses/courses.html'

  def get_context_data(self, *args, **kwargs):
    month = get_actual_date().month
    context = super(CoursesFaceTemplateView, self).get_context_data(*args, **kwargs)
    page_course = self.request.GET.get('page_course')
    courses =  Course.objects.filter(is_active = True, type = "Presencial", month__gte = month).all()
    list_courses_by_month = []
    list_courses = []
    dict_courses_by_month = {}

    months= list(courses.order_by().distinct().values_list('month', flat=True))

    for month in months:
      for course in courses:
        if month == course.month:
          list_courses.append(course)

      dict_courses_by_month = {
        'month' : month,
        'month_name': str(calendar.month_name[int(month)]).capitalize(),
        'courses' : list_courses
      }
      list_courses_by_month.append(dict_courses_by_month)

    context['title'] = 'CURSOS PRESENCIALES'
    context['list_courses_by_month'] = list_courses_by_month
    
    return context

class CoursesRecordTemplateView(TemplateView):
  template_name = 'courses/courses.html'

  def get_context_data(self, *args, **kwargs):
    month = get_actual_date().month
    context = super(CoursesRecordTemplateView, self).get_context_data(*args, **kwargs)
    page_course = self.request.GET.get('page_course')
    courses =  Course.objects.filter(is_active = True, type = "Grabada", month__gte = month).all()
    list_courses_by_month = []
    list_courses = []
    dict_courses_by_month = {}

    months= list(courses.order_by().distinct().values_list('month', flat=True))

    for month in months:
      for course in courses:
        if month == course.month:
          list_courses.append(course)

      dict_courses_by_month = {
        'month' : month,
        'month_name': str(calendar.month_name[int(month)]).capitalize(),
        'courses' : list_courses
      }
      list_courses_by_month.append(dict_courses_by_month)

    context['title'] = 'CURSOS GRABADAS'
    context['list_courses_by_month'] = list_courses_by_month
    
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


    list_testimony =  Testimony.objects.filter(is_active = True)


    context['course'] = course
    context['list_course_you_might_like'] = list_course_you_might_like
    context['list_testimony'] = list_testimony
    
    return context
  
   