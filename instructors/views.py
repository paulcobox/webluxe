from django.shortcuts import render
from django.views.generic import TemplateView
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
  template_name = 'instructors/about_instructors_detail.html'

  def get_context_data(self, *args, **kwargs):
    context = super(InstructorsDetailTemplateView, self).get_context_data(*args, **kwargs)

    try:
        instructor = Instructors.objects.get(id = 1)
    except Instructors.DoesNotExist:
        raise Exception("El Instructors no existe.")


    context['name'] = 'instructor_detail'
    context['instructor'] = instructor
    if instructor.tags_mission:
      context['mision_tags'] = instructor.tags_mission.split(",")
    return context
