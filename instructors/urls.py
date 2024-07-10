from django.urls import path
from .views import InstructorsTemplateView, InstructorsDetailTemplateView

urlpatterns = [
  path('instructor', InstructorsTemplateView.as_view(), name = 'instructor'),
  path('instructor_detail', InstructorsDetailTemplateView.as_view(), name = 'instructor_detail'),
 
]