# blog/models.py
from django.db import models
from django.utils.text import slugify
from django.conf import settings  # Importar settings
from ckeditor.fields import RichTextField
from django.utils.html import strip_tags
import html

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Usar AUTH_USER_MODEL
    excerpt = RichTextField(blank=True, max_length=300, )
    content = RichTextField()
    image = models.ImageField(blank=True, upload_to='images/blog_images', verbose_name = "Imagen")
    published_date = models.DateTimeField(auto_now_add=True)
    visible = models.BooleanField(default=True)  # Publicación visible o no

    @property
    def clean_excerpt(self):
        """Devuelve el excerpt sin etiquetas ni entidades HTML."""
        text = strip_tags(self.excerpt)
        return html.unescape(text)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
