from django.urls import path
from .views import FAQListView, HomePageView, ContactTemplateView, PrivacyPoliciesTemplateView, TermsConditionsTemplateView, sitemap_view, robots_view, ThankYouTemplateView, InvitatedTemplateView, InvitatedSuccessTemplateView, sitemap_blog_view, sitemap_general_view, sitemap_miraflores_view
from django.views.generic import RedirectView
from django.conf import settings
from .views import test_email  # Asegúrate de importar la vista

# from .views import test_email

urlpatterns = [
  # path('about_us', AboutUsTemplateView.as_view(), name = 'about_us'),
  # path('about_mision_vision_values', AboutMisionVisionValuesTemplateView.as_view(), name = 'about_mision_vision_values'),
  # path('about_our_partner', AboutOurPartnerTemplateView.as_view(), name = 'about_our_partner'),
  
  path('', HomePageView.as_view(), name='home'), # new
  path('contact/', ContactTemplateView.as_view(), name='contact'), # new
  path('privacy-policies/', PrivacyPoliciesTemplateView.as_view(), name='privacy_policies'), # new
  path('terms-conditions/', TermsConditionsTemplateView.as_view(), name='terms_conditions'), # new
  path('thankyou', ThankYouTemplateView.as_view(), name='thankyou'), # new
  path('sitemap.xml', sitemap_view, name='sitemap'),
  path('sitemap-blog.xml', sitemap_blog_view, name='sitemap_blog'),
  path('sitemap-general.xml', sitemap_general_view, name='sitemap_general'),
  path('sitemap-miraflores.xml', sitemap_miraflores_view, name='sitemap_miraflores'),
  path('robots.txt', robots_view, name='robots'),
  path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'img/logos/favicon.ico')),
  path('favicon.png', RedirectView.as_view(url=settings.STATIC_URL + 'img/logos/favicon.png')),
  path("invite-friend/", InvitatedTemplateView.as_view(), name="invite_friend"),
  path("invite-success/", InvitatedSuccessTemplateView.as_view(), name="invite_success"),
  path("enviar-correo/", test_email, name="enviar_correo"),
  path('preguntas-frecuentes/', FAQListView.as_view(), name='faq'),
]
  # path('test-email/', test_email, name='test_email'),
    
