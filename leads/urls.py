from django.urls import path
from .views import create_lead

urlpatterns = [
   path('create-lead/', create_lead, name='create-lead'),
]