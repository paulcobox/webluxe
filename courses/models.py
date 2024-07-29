from django.db import models
from ckeditor.fields import RichTextField
from instructors.models import Instructors
from django.utils.text import slugify

     
class Course(models.Model):
      title = models.CharField(max_length=250, blank = False, null = False, unique=True, verbose_name = "Titulo")
      schedule = models.CharField(max_length=250, blank = False, null = False, verbose_name = "Horario")
      instructor = models.ForeignKey(Instructors, on_delete = models.CASCADE, related_name = 'course', blank = False, null = False, verbose_name = "Profesor")
      price = models.IntegerField(blank = False, null = False, verbose_name = "Precio de Curso")
      image = models.ImageField(blank=True, upload_to='images/course', verbose_name = "Imagen Card")
      image_banner_top = models.ImageField(blank=True, upload_to='images/course', verbose_name = "Imagen Banner Top")
      image_fiz = models.ImageField(blank=True, upload_to='images/course', verbose_name = "Imagen Ficha Inferior Izq")
      image_fid = models.ImageField(blank=True, upload_to='images/course', verbose_name = "Imagen Ficha Inferior Der")
      video = models.FileField(upload_to='videos/course', blank=True, verbose_name="Video Ficha")
      body = RichTextField(verbose_name = "Contenido")
      place = models.CharField(max_length=250, blank = False, null = False, verbose_name = "Lugar")
      district = models.CharField(max_length=250, blank = True, null = True, verbose_name = "Distrito")
      is_active = models.BooleanField(blank = False, null = False, default = False, verbose_name = "¿Activo?")
      is_like = models.BooleanField(blank = False, null = False, default = False, verbose_name = "Curso que puede gustar")
      is_banner_home = models.BooleanField(blank = False, null = False, default = False, verbose_name = "¿Aparecera en el Banner Home?")
      type = models.CharField(max_length=50,
        verbose_name='Tipo',
        choices=[
            ('Virtual', 'Virtual'),
            ('Personalizada', 'Personalizada'),
            ('Grupal', 'Grupal'),
            ('Coreografia', 'Coreografia'),
        ],
      )
      slug = models.SlugField(max_length=250, unique=True, blank=True, null=True, verbose_name="Slug")
      created_date = models.DateTimeField(auto_now_add = True, verbose_name = "Fecha de Creación")
      modified_date = models.DateTimeField(auto_now = True, verbose_name = "Fecha de Modificación")

      class Meta:
            verbose_name = "Curso"
            verbose_name_plural = "Cursos"

      @property
      def short_body(self):
        if len(self.body) > 30:
            return self.body[:30] + '...'
        return self.body
      
      def __str__(self):
            return self.title
          
      def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Course, self).save(*args, **kwargs)
          
class Feature(models.Model):
  course = models.ForeignKey(Course, on_delete = models.CASCADE, related_name = 'feature', blank = False, null = False, verbose_name = "Curso")
  description = models.CharField(max_length=250, verbose_name="Caracteristicas")

  def __str__(self):
      return self.description