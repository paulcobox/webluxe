# blog/views.py
from django.views.generic import ListView, DetailView
from .models import Post

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'  # Tu plantilla para la lista de posts
    context_object_name = 'posts'
    paginate_by = 6  # Paginación con 6 posts por página

    def get_queryset(self):
        return Post.objects.filter(visible=True).order_by('-published_date')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'  # Tu plantilla para el detalle del post
    context_object_name = 'post'
