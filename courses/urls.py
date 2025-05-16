from django.urls import path
from .views import CoursesDetailOnlineTemplateView, CoursesDetailParticularTemplateView, CoursesDetailEventsTemplateView,CoursesGroupAllTemplateView, CoursesDetailTemplateView

urlpatterns = [
  path('online/', CoursesDetailOnlineTemplateView.as_view(), name = 'courses_online'),
  path('particulares/', CoursesDetailParticularTemplateView.as_view(), name = 'courses_particulares'),
  path('novios-eventos/', CoursesDetailEventsTemplateView.as_view(), name = 'courses_events'),
  path('', CoursesGroupAllTemplateView.as_view(), name = 'courses_group'),
  # path('courses-group', CoursesGroupTemplateView.as_view(), name = 'courses_group'),
  path('<slug:course_slug>/', CoursesDetailTemplateView.as_view(), name='courses_detail'),
]