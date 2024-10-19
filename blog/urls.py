# blog/urls.py
from django.urls import path
from .views import PostListView, PostDetailView

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),  # Listado de posts
    path('<slug:slug>/', PostDetailView.as_view(), name='post_detail'),  # Detalle de un post
]
