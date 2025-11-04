# blog/views.py
from django.views.generic import ListView, DetailView
from .models import Post
from django.utils.safestring import mark_safe
import json

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'  # Tu plantilla para la lista de posts
    context_object_name = 'posts'
    # paginate_by = 6  # Paginación con 6 posts por página
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['miraflores_posts'] = Post.objects.filter(visible=True, location='miraflores')
        context['sanisidro_posts'] = Post.objects.filter(visible=True, location='sanisidro')
        context['surco_posts'] = Post.objects.filter(visible=True, location='surco')
        context['lince_posts'] = Post.objects.filter(visible=True, location='lince')
        # Agregar el schema dinámico (solo posts visibles)
        visible_posts = Post.objects.filter(visible=True)
        context['blog_schema'] = get_blog_schema(visible_posts)
        return context
    
    def get_queryset(self):
        # Esto mantiene los posts "generales" en la parte superior
        return Post.objects.filter(visible=True, location='general').order_by('-published_date')


class PostDetailByLocationView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_queryset(self):
        # Filtra por la ubicación que viene desde la ruta
        location = self.kwargs.get('location')
        return Post.objects.filter(visible=True, location=location)
    
def get_blog_schema(posts):
    items = []
    for i, post in enumerate(posts, start=1):
        items.append({
            "@type": "BlogPosting",
            "position": i,
            "headline": post.title,
            "url": f"https://cubangrooveperu.com/blog/{post.slug}/",
            "image": f"https://cubangrooveperu.com{post.image.url}",
            "datePublished": post.published_date.strftime("%Y-%m-%dT%H:%M:%S-05:00"),
            "author": {
                "@type": "Organization",
                "name": "Cuban Groove Perú",
                "url": "https://cubangrooveperu.com/"
            }
        })
    schema = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Blog de Cuban Groove Perú",
        "url": "https://cubangrooveperu.com/blog/",
        "description": "Explora artículos sobre salsa cubana, timba y danza en Lima.",
        "mainEntity": {
            "@type": "ItemList",
            "itemListElement": items
        }
    }
    return mark_safe(json.dumps(schema, ensure_ascii=False, indent=2))


# class PostDetailView(DetailView):
#     model = Post
#     template_name = 'blog/post_detail.html'  # Tu plantilla para el detalle del post
#     context_object_name = 'post'
