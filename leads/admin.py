from openpyxl import Workbook
from django.http import HttpResponse
from django.contrib import admin
from .models import Lead, CastingRegistration



admin.site.register(Lead)

class CastingRegistrationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'email', 'occupation', 'district', 'created_at')
    list_filter = ('district', 'created_at')
    search_fields = ('full_name', 'phone', 'email', 'occupation')
    actions = ['export_as_excel']  # Agrega la acción de exportar a Excel

    def export_as_excel(self, request, queryset):
        # Nombre del archivo Excel
        filename = "casting_registrations.xlsx"

        # Crea un libro de Excel y una hoja de trabajo
        wb = Workbook()
        ws = wb.active

        # Mapeo de nombres de campos a títulos en español
        field_titles = {
            'full_name': 'Nombre Completo',
            'phone': 'Teléfono',
            'email': 'Correo Electrónico',
            'occupation': 'Ocupación',
            'district': 'Distrito',
            'dancing_experience': 'Experiencia en Baile',
            'genres': 'Géneros que Domina',
            'experience_competing_teaching': 'Experiencia Compitiendo o Enseñando',
            'motivation': 'Motivación para Unirse',
            'goals': 'Objetivos como Bailarín/a',
            'practice_time_commitment': 'Tiempo de Compromiso para Ensayar',
            'investment_willingness': 'Disposición a Invertir en Formación',
            'long_term_commitment': 'Compromiso a Largo Plazo',
            'other_commitments': 'Otros Compromisos',
            'availability': 'Disponibilidad en Horarios',
            'created_at': 'Fecha de Registro',
        }

        # Obtiene los nombres de las columnas del modelo
        field_names = [field.name for field in self.model._meta.fields]

        # Escribe la fila de encabezados en español
        ws.append([field_titles.get(field, field) for field in field_names])

        # Escribe los datos de cada registro seleccionado
        for obj in queryset:
            row = []
            for field in field_names:
                value = getattr(obj, field)
                # Convierte la fecha a una cadena de texto
                if field == 'created_at' and value:
                    value = value.strftime('%Y-%m-%d %H:%M:%S')
                row.append(value)
            ws.append(row)

        # Crea una respuesta HTTP con el archivo Excel
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        wb.save(response)

        return response

    export_as_excel.short_description = "Exportar seleccionados a Excel"

# Registra el modelo con la clase ModelAdmin personalizada
admin.site.register(CastingRegistration, CastingRegistrationAdmin)