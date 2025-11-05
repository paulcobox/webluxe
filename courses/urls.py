from django.urls import path
from .views import CoursesDetailOnlineTemplateView, CoursesDetailParticularTemplateView, CoursesDetailEventsTemplateView,CoursesGroupAllTemplateView, CoursesDetailTemplateView, SurcoDetailTemplateView, LinceDetailTemplateView, SanIsidroDetailTemplateView, MirafloresDetailTemplateView

urlpatterns = [
  path('clases-baile/online/', CoursesDetailOnlineTemplateView.as_view(), name = 'courses_online'),
  path('clases-baile/particulares/', CoursesDetailParticularTemplateView.as_view(), name = 'courses_particulares'),
  path('clases-baile/novios-eventos/', CoursesDetailEventsTemplateView.as_view(), name = 'courses_events'),
  path('clases-baile/', CoursesGroupAllTemplateView.as_view(), name = 'courses_group'),
  path('clases-de-salsa-en-surco/', SurcoDetailTemplateView.as_view(), name = 'courses_surco'),
  path('clases-de-salsa-en-miraflores/', MirafloresDetailTemplateView.as_view(), name = 'courses_miraflores'),
  path('clases-de-salsa-en-san_isidro/', SanIsidroDetailTemplateView.as_view(), name = 'courses_san_isidro'),
  path('clases-de-salsa-en-lince/', LinceDetailTemplateView.as_view(), name = 'courses_lince'),
  # path('clases-salsa-lince', CoursesGroupAllTemplateView.as_view(), name = 'courses_group'),
  # path('clases-salsa-san-isisdro', CoursesGroupAllTemplateView.as_view(), name = 'courses_group'),
  # path('courses-group', CoursesGroupTemplateView.as_view(), name = 'courses_group'),
  path('clases-baile/<slug:course_slug>/', CoursesDetailTemplateView.as_view(), name='courses_detail'),
]