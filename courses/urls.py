from django.urls import path
from .views import CoursesVirtualTemplateView, CoursesPersonalTemplateView, CoursesGroupTemplateView,CoursesChoreographyTemplateView, CoursesDetailTemplateView

urlpatterns = [
  path('courses_virtual', CoursesVirtualTemplateView.as_view(), name = 'courses_virtual'),
  path('courses_personal', CoursesPersonalTemplateView.as_view(), name = 'courses_personal'),
  path('courses_group', CoursesGroupTemplateView.as_view(), name = 'courses_group'),
  path('courses_choreography', CoursesChoreographyTemplateView.as_view(), name = 'courses_choreography'),
  path('courses/<slug:course_slug>/', CoursesDetailTemplateView.as_view(), name='courses_detail'),
]