# blog/urls.py
from django.urls import path
from .views import PostListView, PostDetailByLocationView

urlpatterns = [
    path('blog/', PostListView.as_view(), name='post_list'),  # Listado de posts
    # path('<slug:slug>/', PostDetailByLocationView.as_view(), name='post_detail'),  # Detalle de un post
     # Clusters locales (solo detalle, sin lista)
    path('clases-de-salsa-en-miraflores/<slug:slug>/', 
         PostDetailByLocationView.as_view(), 
         {'location': 'miraflores'}, 
         name='post_miraflores'),

    path('clases-de-salsa-en-san-isidro/<slug:slug>/', 
         PostDetailByLocationView.as_view(), 
         {'location': 'sanisidro'}, 
         name='post_sanisidro'),

    path('clases-de-salsa-en-surco/<slug:slug>/', 
         PostDetailByLocationView.as_view(), 
         {'location': 'surco'}, 
         name='post_surco'),

    # Blog general (si quieres mantenerlo)
    path('blog/<slug:slug>/', PostDetailByLocationView.as_view(), {'location': 'general'}, name='post_general'),
]
