from django.urls import path
from .views import HomePageView, ContactTemplateView, PrivacyPoliciesTemplateView, TermsConditionsTemplateView, sitemap_view, robots_view, ThankYouTemplateView, InvitatedTemplateView, InvitatedSuccessTemplateView
from django.views.generic import RedirectView
from django.conf import settings
# from .views import test_email

urlpatterns = [
  # path('about_us', AboutUsTemplateView.as_view(), name = 'about_us'),
  # path('about_mision_vision_values', AboutMisionVisionValuesTemplateView.as_view(), name = 'about_mision_vision_values'),
  # path('about_our_partner', AboutOurPartnerTemplateView.as_view(), name = 'about_our_partner'),
  
  path('', HomePageView.as_view(), name='home'), # new
  path('contact', ContactTemplateView.as_view(), name='contact'), # new
  path('privacy-policies', PrivacyPoliciesTemplateView.as_view(), name='privacy_policies'), # new
  path('terms-conditions', TermsConditionsTemplateView.as_view(), name='terms_conditions'), # new
  path('thankyou', ThankYouTemplateView.as_view(), name='thankyou'), # new
  path('sitemap.xml', sitemap_view, name='sitemap'),
  path('robots.txt', robots_view, name='robots'),
  path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'img/logos/favicon.ico')),
  path("invite-friend/", InvitatedTemplateView.as_view(), name="invite_friend"),
  path("invite-success/", InvitatedSuccessTemplateView.as_view(), name="invite_success"),
  # path('test-email/', test_email, name='test_email'),
    
]