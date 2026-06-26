from django.urls import path
from django.views.generic import RedirectView
from .views import create_lead, update_lead_sede, kommo_webhook_contact_created
from . import views

urlpatterns = [
   path('create-lead/', create_lead, name='create-lead'),
   path('update-lead-sede/', update_lead_sede, name='update-lead-sede'),
   path('webhooks/kommo/contact-created/', kommo_webhook_contact_created, name='kommo_webhook_contact_created'),
   path('casting/', RedirectView.as_view(url='/', permanent=True)),
   path('casting/additional-info/', RedirectView.as_view(url='/', permanent=True)),
   path('casting/thank-you/', RedirectView.as_view(url='/', permanent=True)),
   path('unsubscribe/<str:token>/', views.unsubscribe, name='unsubscribe'),
]