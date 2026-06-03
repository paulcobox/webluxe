from django.urls import path
from .views import create_lead, update_lead_sede
from . import views

urlpatterns = [
   path('create-lead/', create_lead, name='create-lead'),
   path('update-lead-sede/', update_lead_sede, name='update-lead-sede'),
   path('casting/', views.casting_registration, name='casting_registration'),
   path('casting/additional-info/', views.additional_info, name='additional_info'),
   path('casting/thank-you/', views.thank_you, name='thank_you'),
   path('unsubscribe/<str:token>/', views.unsubscribe, name='unsubscribe'),
]