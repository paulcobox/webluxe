# blog/models.py
from django.db import models
from django.utils.text import slugify
from django.conf import settings  # Importar settings

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Usar AUTH_USER_MODEL
    excerpt = models.TextField(max_length=300, blank=True)
    content = models.TextField()
    image = models.ImageField(blank=True, upload_to='images/blog_images', verbose_name = "Imagen")
    published_date = models.DateTimeField(auto_now_add=True)
    visible = models.BooleanField(default=True)  # Publicación visible o no

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
