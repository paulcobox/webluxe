from django.db import models
from ckeditor.fields import RichTextField
from instructors.models import Instructors

     
class Course(models.Model):
      title = models.CharField(max_length=250, blank = False, null = False, unique=True, verbose_name = "Titulo")
      schedule = models.CharField(max_length=250, blank = False, null = False, unique=True, verbose_name = "Horario")
      month = models.IntegerField(max_length=50,
        verbose_name='Mes',
        choices=[
            (1, 'Enero'),
            (2, 'Febrero'),
            (3, 'Marzo'),
            (4, 'Abril'),
            (5, 'Mayo'),
            (6, 'Junio'),
            (7, 'Julio'),
            (8, 'Agosto'),
            (9, 'Septiembre'),
            (10, 'Octubre'),
            (11, 'Noviembre'),
            (12, 'Diciembre'),
        ],
      )
      instructor = models.ForeignKey(Instructors, on_delete = models.CASCADE, related_name = 'course', blank = False, null = False, verbose_name = "Profesor")
      price = models.IntegerField(blank = False, null = False, verbose_name = "Precio de Curso")
      image = models.ImageField(blank=True, upload_to='images/course', verbose_name = "Imagen Card")
      image_fiz = models.ImageField(blank=True, upload_to='images/course', verbose_name = "Imagen Ficha Inferior Izq")
      image_fid = models.ImageField(blank=True, upload_to='images/course', verbose_name = "Imagen Ficha Inferior Der")
      video = models.FileField(upload_to='videos/course', blank=True, verbose_name="Video Ficha")
      body = RichTextField(verbose_name = "Contenido")
      place = RichTextField(verbose_name = "Lugar")
      is_active = models.BooleanField(blank = False, null = False, default = False, verbose_name = "¿Activo?")
      is_like = models.BooleanField(blank = False, null = False, default = False, verbose_name = "Curso que puede gustar")
      type = models.CharField(max_length=50,
        verbose_name='Tipo',
        choices=[
            ('Virtual', 'Virtual'),
            ('Presencial', 'Presencial'),
            ('Grabada', 'Grabada'),
        ],
      )
      created_date = models.DateTimeField(auto_now_add = True, verbose_name = "Fecha de Creación")
      modified_date = models.DateTimeField(auto_now = True, verbose_name = "Fecha de Modificación")

      class Meta:
            verbose_name = "Curso"
            verbose_name_plural = "Cursos"

      def __str__(self):
            return self.title
          
 