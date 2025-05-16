from django.contrib import admin
from .models import Course, Feature, FAQ

# Register your models here.

class FeatureInline(admin.TabularInline):
    model = Feature
    extra = 1  # Número de campos en blanco para mostrar inicialmente
    
class FAQInline(admin.TabularInline):
    model = FAQ
    extra = 2  # Número de campos en blanco para mostrar inicialmente
    
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [FAQInline]
    list_display = ('title', 'schedule', 'instructor', 'price', 'is_active')
    list_filter = ('is_active', 'instructor')
    search_fields = ('title', 'schedule', 'instructor__name')
    prepopulated_fields = {'slug': ('title',)}
    

