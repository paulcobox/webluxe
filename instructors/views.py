from django.shortcuts import render
from django.views.generic import TemplateView
from instructors.models import Instructors
from django.shortcuts import get_object_or_404
# Create your views here.

class InstructorsTemplateView(TemplateView):
  template_name = 'instructors/about_instructors.html'

  def get_context_data(self, *args, **kwargs):
    context = super(InstructorsTemplateView, self).get_context_data(*args, **kwargs)
    instructors = Instructors.objects.filter(is_active = True)
    context['name'] = 'instructor'
    context['instructors'] = instructors
    return context


class InstructorsDetailTemplateView(TemplateView):
  template_name = 'instructors/instructors_detail.html'

  def get_context_data(self, *args, **kwargs):
    context = super(InstructorsDetailTemplateView, self).get_context_data(*args, **kwargs)
    instructor_slug = kwargs.get('instructor_slug')  # Assuming 'course_slug' is the URL parameter
    instructor = get_object_or_404(Instructors.objects.filter(is_active=True), slug=instructor_slug)
    context['instructor'] = instructor
    if instructor.tags_about_me:
      context['tags_about_me'] = instructor.tags_about_me.split("|")
    return context
