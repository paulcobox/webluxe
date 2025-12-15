from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Course
from django.shortcuts import get_object_or_404
from django.db.models import Case, When, Value, IntegerField, Q
from itertools import chain
# Create your views here.

class SalsaCercaDeMiTemplateView(TemplateView):

    template_name = 'courses/course_detail_district.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        course_slug = 'clases-de-salsa-cerca-de-mi'
        course_title_zone = 'Cerca de ti'

        course = get_object_or_404(Course, slug=course_slug)

        salsa_basico = Course.objects.filter(
            is_active=True,
            title="Principiantes"
        ).annotate(
            order_priority=Value(-1, output_field=IntegerField())
        )

        other_courses = Course.objects.filter(
            is_active=True
        ).exclude(
            title="Principiantes"
        ).annotate(
            order_priority=Case(
                When(schedule="Proximamente", then=Value(1)),
                default=Value(0),
                output_field=IntegerField(),
            )
        ).order_by('order_priority')

        combined_qs = list(chain(salsa_basico, other_courses))
        list_course_you_might_like = [c for c in combined_qs if c.pk != course.pk]

        context['course'] = course
        context['course_title_zone'] = course_title_zone
        context['list_course_you_might_like'] = list_course_you_might_like

        return context


class AcademiaSalsaLimaTemplateView(TemplateView):

    template_name = 'courses/course_detail_district.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        course_slug = 'academia-de-salsa-en-lima'
        course_title_zone = 'Lima'

        course = get_object_or_404(Course, slug=course_slug)

        salsa_basico = Course.objects.filter(
            is_active=True,
            title="Principiantes"
        ).annotate(
            order_priority=Value(-1, output_field=IntegerField())
        )

        other_courses = Course.objects.filter(
            is_active=True
        ).exclude(
            title="Principiantes"
        ).annotate(
            order_priority=Case(
                When(schedule="Proximamente", then=Value(1)),
                default=Value(0),
                output_field=IntegerField(),
            )
        ).order_by('order_priority')

        combined_qs = list(chain(salsa_basico, other_courses))
        list_course_you_might_like = [c for c in combined_qs if c.pk != course.pk]

        context['course'] = course
        context['course_title_zone'] = course_title_zone
        context['list_course_you_might_like'] = list_course_you_might_like

        return context


class LimaDetailTemplateView(TemplateView):
  
  template_name = 'courses/course_detail_district.html'

  def get_context_data(self, *args, **kwargs):
    context = super(LimaDetailTemplateView, self).get_context_data(*args, **kwargs)
    course_slug = 'clases-de-salsa-en-lima'  # Assuming 'course_slug' is the URL parameter
    course_title_zone = 'Lima'  # Assuming 'course_slug' is the URL parameter
    course = get_object_or_404(Course, slug=course_slug)
    # video_id = YouTube(course.video_url).video_id
    # course.video_url = f"https://www.youtube.com/embed/{video_id}"
    salsa_basico = Course.objects.filter(is_active=True, title="Principiantes").annotate(order_priority=Value(-1, output_field=IntegerField()))
    
    other_courses = Course.objects.filter(is_active=True).exclude(title="Principiantes").annotate(
            order_priority=Case(
                When(schedule="Proximamente", then=Value(1)),  # Los que tienen "Proximamente" tienen menor prioridad
                default=Value(0),  # El resto tiene mayor prioridad
                output_field=IntegerField(),
            )
        ).order_by('order_priority')  # Ordenar por prioridad
        
    combined_qs = list(chain(salsa_basico, other_courses))
    list_course_you_might_like = [c for c in combined_qs if c.pk != course.pk]
    

    context['course'] = course
    context['course_title_zone'] = course_title_zone
    context['list_course_you_might_like'] = list_course_you_might_like
   
    
    return context

class SurcoDetailTemplateView(TemplateView):
  
  template_name = 'courses/course_detail_district.html'

  def get_context_data(self, *args, **kwargs):
    context = super(SurcoDetailTemplateView, self).get_context_data(*args, **kwargs)
    course_slug = 'clases-de-salsa-en-surco'  # Assuming 'course_slug' is the URL parameter
    course_title_zone = 'Surco'  # Assuming 'course_slug' is the URL parameter
    course = get_object_or_404(Course, slug=course_slug)
    # video_id = YouTube(course.video_url).video_id
    # course.video_url = f"https://www.youtube.com/embed/{video_id}"
    salsa_basico = Course.objects.filter(is_active=True, title="Principiantes").annotate(order_priority=Value(-1, output_field=IntegerField()))
    
    other_courses = Course.objects.filter(is_active=True).exclude(title="Principiantes").annotate(
            order_priority=Case(
                When(schedule="Proximamente", then=Value(1)),  # Los que tienen "Proximamente" tienen menor prioridad
                default=Value(0),  # El resto tiene mayor prioridad
                output_field=IntegerField(),
            )
        ).order_by('order_priority')  # Ordenar por prioridad
        
    combined_qs = list(chain(salsa_basico, other_courses))
    list_course_you_might_like = [c for c in combined_qs if c.pk != course.pk]
    

    context['course'] = course
    context['course_title_zone'] = course_title_zone
    context['list_course_you_might_like'] = list_course_you_might_like
   
    
    return context



class MirafloresDetailTemplateView(TemplateView):
  
  template_name = 'courses/course_detail_district.html'

  def get_context_data(self, *args, **kwargs):
    context = super(MirafloresDetailTemplateView, self).get_context_data(*args, **kwargs)
    course_slug = 'clases-de-salsa-en-miraflores'  # Assuming 'course_slug' is the URL parameter
    course_title_zone = 'Miraflores (a pocos minutos)'  # Assuming 'course_slug' is the URL parameter
    course = get_object_or_404(Course, slug=course_slug)
    
    # Ordenar: primero los cursos que tengan "surco" en el campo Lugar (insensible a mayúsculas)
    courses = Course.objects.filter(is_active=True).annotate(
        order_priority=Case(
            When(Q(place__icontains='surco'), then=Value(0)),  # prioridad más alta
            default=Value(1),
            output_field=IntegerField(),
        )
    ).order_by('order_priority', 'title')

    # Excluir el curso actual
    list_course_you_might_like = [c for c in courses if c.pk != course.pk]

    # Contexto
    context['course'] = course
    context['course_title_zone'] = course_title_zone
    context['list_course_you_might_like'] = list_course_you_might_like

    return context


class LinceDetailTemplateView(TemplateView):
  
  template_name = 'courses/course_detail_district.html'

  def get_context_data(self, *args, **kwargs):
    context = super(LinceDetailTemplateView, self).get_context_data(*args, **kwargs)
    course_slug = 'clases-de-salsa-en-lince'  # Assuming 'course_slug' is the URL parameter
    course_title_zone = 'Lince'  # Assuming 'course_slug' is the URL parameter
    course = get_object_or_404(Course, slug=course_slug)
    
    # Ordenar: primero los cursos que tengan "lince" en el campo Lugar (insensible a mayúsculas)
    courses = Course.objects.filter(is_active=True).annotate(
        order_priority=Case(
            When(Q(place__icontains='lince'), then=Value(0)),  # prioridad más alta
            default=Value(1),
            output_field=IntegerField(),
        )
    ).order_by('order_priority', 'title')  # primero los de Lince, luego alfabéticamente

    # Excluir el curso actual
    list_course_you_might_like = [c for c in courses if c.pk != course.pk]

    # Contexto
    context['course'] = course
    context['course_title_zone'] = course_title_zone
    context['list_course_you_might_like'] = list_course_you_might_like

    return context

class SanIsidroDetailTemplateView(TemplateView):
  
  template_name = 'courses/course_detail_district.html'

  def get_context_data(self, *args, **kwargs):
    context = super(SanIsidroDetailTemplateView, self).get_context_data(*args, **kwargs)
    course_slug = 'clases-de-salsa-en-san-isidro'  # Assuming 'course_slug' is the URL parameter
    course_title_zone = 'San Isidro'  # Assuming 'course_slug' is the URL parameter
    course = get_object_or_404(Course, slug=course_slug)
    
    # Ordenar: primero los cursos que tengan "lince" en el campo Lugar (insensible a mayúsculas)
    courses = Course.objects.filter(is_active=True).annotate(
        order_priority=Case(
            When(Q(place__icontains='San Isidro'), then=Value(0)),  # prioridad más alta
            default=Value(1),
            output_field=IntegerField(),
        )
    ).order_by('order_priority', 'title')  # primero los de Lince, luego alfabéticamente

    # Excluir el curso actual
    list_course_you_might_like = [c for c in courses if c.pk != course.pk]

    # Contexto
    context['course'] = course
    context['course_title_zone'] = course_title_zone
    context['list_course_you_might_like'] = list_course_you_might_like

    return context


class CoursesDetailOnlineTemplateView(TemplateView):
  
  template_name = 'courses/course_detail_otros.html'

  def get_context_data(self, *args, **kwargs):
    context = super(CoursesDetailOnlineTemplateView, self).get_context_data(*args, **kwargs)
    course_slug = 'online'  # Assuming 'course_slug' is the URL parameter
    course = get_object_or_404(Course, slug=course_slug)
    # video_id = YouTube(course.video_url).video_id
    # course.video_url = f"https://www.youtube.com/embed/{video_id}"
    salsa_basico = Course.objects.filter(is_active=True, title="Principiantes").annotate(order_priority=Value(-1, output_field=IntegerField()))
    
    other_courses = Course.objects.filter(is_active=True).exclude(title="Principiantes").annotate(
            order_priority=Case(
                When(schedule="Proximamente", then=Value(1)),  # Los que tienen "Proximamente" tienen menor prioridad
                default=Value(0),  # El resto tiene mayor prioridad
                output_field=IntegerField(),
            )
        ).order_by('order_priority')  # Ordenar por prioridad
        
    combined_qs = list(chain(salsa_basico, other_courses))
    list_course_you_might_like = [c for c in combined_qs if c.pk != course.pk]
    
    context['course'] = course
    context['list_course_you_might_like'] = list_course_you_might_like
   
    
    return context

class CoursesDetailParticularTemplateView(TemplateView):
  
  template_name = 'courses/course_detail_otros.html'

  def get_context_data(self, *args, **kwargs):
    context = super(CoursesDetailParticularTemplateView, self).get_context_data(*args, **kwargs)
    course_slug = 'particulares'  # Assuming 'course_slug' is the URL parameter
    course = get_object_or_404(Course, slug=course_slug)
    # video_id = YouTube(course.video_url).video_id
    # course.video_url = f"https://www.youtube.com/embed/{video_id}"
    salsa_basico = Course.objects.filter(is_active=True, title="Principiantes").annotate(order_priority=Value(-1, output_field=IntegerField()))
    
    other_courses = Course.objects.filter(is_active=True).exclude(title="Principiantes").annotate(
            order_priority=Case(
                When(schedule="Proximamente", then=Value(1)),  # Los que tienen "Proximamente" tienen menor prioridad
                default=Value(0),  # El resto tiene mayor prioridad
                output_field=IntegerField(),
            )
        ).order_by('order_priority')  # Ordenar por prioridad
        
    combined_qs = list(chain(salsa_basico, other_courses))
    list_course_you_might_like = [c for c in combined_qs if c.pk != course.pk]
    

    context['course'] = course
    context['list_course_you_might_like'] = list_course_you_might_like
   
    
    return context
  
  
class CoursesDetailEventsTemplateView(TemplateView):
  
  template_name = 'courses/course_detail_otros.html'

  def get_context_data(self, *args, **kwargs):
    context = super(CoursesDetailEventsTemplateView, self).get_context_data(*args, **kwargs)
    course_slug = 'novios-eventos'  # Assuming 'course_slug' is the URL parameter
    course = get_object_or_404(Course, slug=course_slug)
    # video_id = YouTube(course.video_url).video_id
    # course.video_url = f"https://www.youtube.com/embed/{video_id}"
    salsa_basico = Course.objects.filter(is_active=True, title="Principiantes").annotate(order_priority=Value(-1, output_field=IntegerField()))
    
    other_courses = Course.objects.filter(is_active=True).exclude(title="Principiantes").annotate(
            order_priority=Case(
                When(schedule="Proximamente", then=Value(1)),  # Los que tienen "Proximamente" tienen menor prioridad
                default=Value(0),  # El resto tiene mayor prioridad
                output_field=IntegerField(),
            )
        ).order_by('order_priority')  # Ordenar por prioridad
        
    combined_qs = list(chain(salsa_basico, other_courses))
    list_course_you_might_like = [c for c in combined_qs if c.pk != course.pk]
    

    context['course'] = course
    context['list_course_you_might_like'] = list_course_you_might_like
   
    
    return context
  
  

class CoursesGroupAllTemplateView(TemplateView):
    template_name = 'courses/courses.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CoursesGroupAllTemplateView, self).get_context_data(*args, **kwargs)
        
        # Obtener el curso "Salsa Cubana Basico" si existe
        salsa_basico = Course.objects.filter(
            is_active=True, 
            title="Salsa Principiantes"
        ).annotate(
            order_priority=Value(-1, output_field=IntegerField())  # Prioridad máxima
        )

        # Obtener el resto de los cursos
        other_courses = Course.objects.filter(is_active=True).exclude(
            title="Salsa Principiantes"
        ).annotate(
            order_priority=Case(
                When(schedule="Proximamente", then=Value(1)),  # Los que tienen "Proximamente" tienen menor prioridad
                default=Value(0),  # El resto tiene mayor prioridad
                output_field=IntegerField(),
            )
        ).order_by('order_priority')  # Ordenar por prioridad

        # Combinar los cursos, colocando "Salsa Cubana Basico" al inicio
        courses = list(salsa_basico) + list(other_courses)

        context['title'] = 'Clases de Baile'
        context['list_courses'] = courses
        
        return context


 
class CoursesDetailTemplateView(TemplateView):
  
  template_name = 'courses/course_detail.html'

  def get_context_data(self, *args, **kwargs):
    context = super(CoursesDetailTemplateView, self).get_context_data(*args, **kwargs)
    course_slug = kwargs.get('course_slug')  # Assuming 'course_slug' is the URL parameter
    course = get_object_or_404(Course.objects.filter(is_active=True), slug=course_slug)

    list_course_you_might_like = Course.objects.filter(is_active=True).exclude(pk=course.pk)
    
    list_course_you_might_like = list_course_you_might_like.filter(is_active=True).annotate(
        order_priority=Case(
            When(schedule="Proximamente", then=Value(1)),  # Los que tienen "Proximamente" tienen menor prioridad
            default=Value(0),  # El resto tiene mayor prioridad
            output_field=IntegerField(),
        )
    ).order_by('order_priority')[:6]  # Seleccionar los primeros 6 registros
    

    context['course'] = course
    print('entroooooooooooooo', course.body_title)
    context['list_course_you_might_like'] = list_course_you_might_like
    
    return context
   

  
   