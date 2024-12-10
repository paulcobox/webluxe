from django.shortcuts import render
from django.views.generic import TemplateView
# from .models import MissionVision
from courses.models import Course
from random import sample
from django.http import FileResponse
from django.http import FileResponse, Http404
# from instructors.models import Instructors
# Create your views here.

class HomePageView(TemplateView):
  template_name = 'index.html'
  
  
  def get_context_data(self, *args, **kwargs):
    context = super(HomePageView, self).get_context_data(*args, **kwargs)
    list_course_you_might_like = Course.objects.filter(is_active=True)
    
    # Select 3 random courses (if there are at least 3 active courses)
    if list_course_you_might_like.count() >= 3:
        list_course_you_might_like = sample(list(list_course_you_might_like), 3)
        
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
  
def sitemap_view(request):
    return FileResponse(open('sitemap.xml', 'rb'), content_type='application/xml')

def robots_view(request):
    try:
        return FileResponse(open('robots.txt', 'rb'), content_type='text/plain')
    except FileNotFoundError:
        raise Http404("El archivo robots.txt no se encuentra.")
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
