from django.shortcuts import render
from django.views.generic import TemplateView
from .models import MissionVision
# Create your views here.


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
