from django.db import models
from ckeditor.fields import RichTextField
from django.core.validators import FileExtensionValidator
from courses.models import Course
# Create your models here.

class MissionVision(models.Model):#por usuario o masivo
      title = models.CharField(max_length=250, blank = False, null = False, unique=True, verbose_name = "Titulo")
      image = models.ImageField(blank=True, upload_to='images', verbose_name = "Imagen")
      body = RichTextField(verbose_name = "Texto")
      is_active = models.BooleanField(blank = False, null = False, default = False, verbose_name = "¿Activo?")
      tags = models.CharField(max_length=500, blank = False, null = False, verbose_name = "Etiquetas")
      type = models.CharField(max_length=50,
        verbose_name='Tipo',
        choices=[
            ('Mision', 'Mision'),
            ('Vision', 'Vision')
        ],
      )
      created_date = models.DateTimeField(auto_now_add = True, verbose_name = "Fecha de Creación")
      modified_date = models.DateTimeField(auto_now = True, verbose_name = "Fecha de Modificación")

      class Meta:
            verbose_name = "Mision Vision"
            verbose_name_plural = "Mision Vision"

      def __str__(self):
            return self.title


      
class Banner(models.Model):
      name = models.CharField(max_length=250, blank = False, null = False, verbose_name = "Nombre")
      type = models.CharField(max_length=50,
        verbose_name='Tipo',
        choices=[
            ('Top', 'Top'),
        ],
      )
      image = models.ImageField(blank=True, upload_to='images', verbose_name = "Imagen Banner")
      is_active = models.BooleanField(blank = False, null = False, default = False, verbose_name = "¿Activo?")
      course = models.ForeignKey(Course, on_delete = models.CASCADE, related_name = 'banner', blank = False, null = False, verbose_name = "Curso")
      created_date = models.DateTimeField(auto_now_add = True, verbose_name = "Fecha de Creación")
      modified_date = models.DateTimeField(auto_now = True, verbose_name = "Fecha de Modificación")

      class Meta:
            verbose_name = "Instructor"
            verbose_name_plural = "Instructores"

      def __str__(self):
            return self.name


         
class Testimony(models.Model):
      name = models.CharField(max_length=250, blank = False, null = False, unique=False, verbose_name = "Nombre del Cliente")
      profession = models.CharField(max_length=250, blank = False, null = False, unique=False, verbose_name = "Profesión")
      description = RichTextField(verbose_name = "Descripcion")
      video = models.FileField(upload_to='videos/testimony', blank=True, verbose_name="Video Testimonio")
      is_active = models.BooleanField(blank = False, null = False, default = False, verbose_name = "¿Activo?")
      created_date = models.DateTimeField(auto_now_add = True, verbose_name = "Fecha de Creación")
      modified_date = models.DateTimeField(auto_now = True, verbose_name = "Fecha de Modificación")

      class Meta:
            verbose_name = "Testimonio"
            verbose_name_plural = "Testimonios"

      def __str__(self):
            return self.name + self.profession
