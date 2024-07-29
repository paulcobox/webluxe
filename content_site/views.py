from django.shortcuts import render
from django.views.generic import TemplateView
from .models import MissionVision
from courses.models import Course
from random import sample
# Create your views here.

class HomePageView(TemplateView):
  template_name = 'content_site/index.html'
  
  
  def get_context_data(self, *args, **kwargs):
    context = super(HomePageView, self).get_context_data(*args, **kwargs)
    list_course_you_might_like = Course.objects.filter(is_active=True)
    
    # Select 3 random courses (if there are at least 3 active courses)
    if list_course_you_might_like.count() >= 3:
        list_course_you_might_like = sample(list(list_course_you_might_like), 3)
        
    list_course_banner_top =  Course.objects.filter(is_active = True, is_banner_home=True)
    if list_course_banner_top.count() >= 3:
        list_course_banner_top = sample(list(list_course_banner_top), 3)

    context['list_course_banner_top'] = list_course_banner_top
    
    return context



class ContactTemplateView(TemplateView):
  template_name = 'content_site/contact.html'

  def get_context_data(self, *args, **kwargs):
    context = super(ContactTemplateView, self).get_context_data(*args, **kwargs)
    context['name'] = 'contact'
    return context
  
class AboutUsTemplateView(TemplateView):
  template_name = 'content_site/about_us.html'

  def get_context_data(self, *args, **kwargs):
    context = super(AboutUsTemplateView, self).get_context_data(*args, **kwargs)
    context['name'] = 'about_us'
    return context

class AboutMisionVisionValuesTemplateView(TemplateView):
  template_name = 'content_site/about_mision_vision.html'

  def get_context_data(self, *args, **kwargs):
    context = super(AboutMisionVisionValuesTemplateView, self).get_context_data(*args, **kwargs)
    mision =  MissionVision.objects.filter(is_active = True, type = "Mision").first()
    vision = MissionVision.objects.filter(is_active = True, type = "Vision").first()
    

    context['name'] = 'about_mision_vision'
    if mision:
      context['mision'] = mision
      context['mision_tags'] = mision.tags.split(",")
    if vision:
      context['vision'] = vision
      context['vision_tags'] = vision.tags.split(",")
    
    return context


class AboutOurPartnerTemplateView(TemplateView):
  template_name = 'content_site/about_our_partner.html'

  def get_context_data(self, *args, **kwargs):
    context = super(AboutOurPartnerTemplateView, self).get_context_data(*args, **kwargs)
    context['name'] = 'about_our_partner'
    return context
