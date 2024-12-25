from django.urls import path
from .views import CoursesVirtualTemplateView, CoursesPersonalTemplateView, CoursesGroupTemplateView,CoursesChoreographyTemplateView, CoursesDetailTemplateView, CoursesGroupAllTemplateView

urlpatterns = [
  path('courses-virtual', CoursesVirtualTemplateView.as_view(), name = 'courses_virtual'),
  path('courses-personal', CoursesPersonalTemplateView.as_view(), name = 'courses_personal'),
  path('courses-group', CoursesGroupAllTemplateView.as_view(), name = 'courses_group'),
  # path('courses-group', CoursesGroupTemplateView.as_view(), name = 'courses_group'),
  path('courses-choreography', CoursesChoreographyTemplateView.as_view(), name = 'courses_choreography'),
  path('courses/<slug:course_slug>/', CoursesDetailTemplateView.as_view(), name='courses_detail'),
]