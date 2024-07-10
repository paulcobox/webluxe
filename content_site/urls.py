from django.urls import path
from .views import AboutUsTemplateView, AboutMisionVisionValuesTemplateView

urlpatterns = [
  path('about_us', AboutUsTemplateView.as_view(), name = 'about_us'),
  path('about_mision_vision_values', AboutMisionVisionValuesTemplateView.as_view(), name = 'about_mision_vision_values'),
  path('about_our_partner', AboutOurPartnerTemplateView.as_view(), name = 'about_our_partner')
]