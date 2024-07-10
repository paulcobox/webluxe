from django.urls import path
from .views import CoursesVirtualTemplateView, CoursesFaceTemplateView, CoursesRecordTemplateView,CoursesDetailTemplateView

urlpatterns = [
  path('courses_virtual', CoursesVirtualTemplateView.as_view(), name = 'courses_virtual'),
  path('courses_face', CoursesFaceTemplateView.as_view(), name = 'courses_face'),
  path('courses_record', CoursesRecordTemplateView.as_view(), name = 'courses_record'),
  path('courses/<slug:course_slug>/', CoursesDetailTemplateView.as_view(), name='courses_detail'),
]