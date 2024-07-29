from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.

class Instructors(models.Model):
      name = models.CharField(max_length=250, blank = False, null = False, verbose_name = "Nombre")
      tags_about_me = models.CharField(max_length=500, blank = False, null = False, verbose_name = "Tags Acerca de Mi")
      tags_mission = models.CharField(max_length=500, blank = False, null = False, verbose_name = "Tags Mision")
      specialty = models.CharField(max_length=250, blank = False, null = False, verbose_name = "Especialidad")
      about_me = RichTextField(verbose_name = "Acerca de Mi", blank = False, null = False)
      mission = RichTextField(verbose_name = "Mi Mision", blank = False, null = False)
      image = models.ImageField(blank=True, upload_to='images', verbose_name = "Imagen de Instructor")
      is_active = models.BooleanField(blank = False, null = False, default = False, verbose_name = "¿Activo?")
      facebook = models.URLField(max_length=500, blank = True, null = True, verbose_name = "Facebook")
      tiktok = models.URLField(max_length=500, blank = True, null = True, verbose_name = "Tiktok")
      instagram = models.URLField(max_length=500, blank = True, null = True, verbose_name = "Instagram")
      youtube = models.URLField(max_length=500, blank = True, null = True, verbose_name = "Youtube")
      created_date = models.DateTimeField(auto_now_add = True, verbose_name = "Fecha de Creación")
      modified_date = models.DateTimeField(auto_now = True, verbose_name = "Fecha de Modificación")

      class Meta:
            verbose_name = "Instructor"
            verbose_name_plural = "Instructores"

      def __str__(self):
            return self.name