from django.urls import path
from .views import create_lead
from . import views

urlpatterns = [
   path('create-lead/', create_lead, name='create-lead'),
   path('casting/', views.casting_registration, name='casting_registration'),
   path('casting/additional-info/', views.additional_info, name='additional_info'),
   path('casting/thank-you/', views.thank_you, name='thank_you'),
]