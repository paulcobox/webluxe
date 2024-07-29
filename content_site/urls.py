from django.urls import path
from .views import AboutUsTemplateView, AboutMisionVisionValuesTemplateView, AboutOurPartnerTemplateView, HomePageView, ContactTemplateView

urlpatterns = [
  path('about_us', AboutUsTemplateView.as_view(), name = 'about_us'),
  path('about_mision_vision_values', AboutMisionVisionValuesTemplateView.as_view(), name = 'about_mision_vision_values'),
  path('about_our_partner', AboutOurPartnerTemplateView.as_view(), name = 'about_our_partner'),
  
  path('', HomePageView.as_view(), name='home'), # new
  path('contact', ContactTemplateView.as_view(), name='contact'), # new
    
]