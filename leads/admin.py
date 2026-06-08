from openpyxl import Workbook
from django.http import HttpResponse
from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Lead, CastingRegistration, EmailSequenceLog


class EmailSequenceLogInline(admin.TabularInline):
    model = EmailSequenceLog
    extra = 0
    readonly_fields = ('sequence_position', 'status', 'celery_task_id', 'sent_at', 'error_message', 'created_at')
    can_delete = False
    ordering = ('sequence_position',)

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'created_date', 'unsubscribed', 'sequence_progress_display')
    list_filter = ('created_date', 'status', 'unsubscribed')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')
    readonly_fields = ('email_sequence_started_at', 'unsubscribe_token', 'meta_event_id',
                       'capi_sent', 'capi_sent_at', 'capi_response',
                       'form_age_raw')
    inlines = [EmailSequenceLogInline]

    def sequence_progress_display(self, obj):
        sent = obj.email_logs.filter(status='SENT').count()
        total = 9
        color = '#25D366' if sent == total else '#ff6a09' if sent > 0 else '#aaaaaa'
        return format_html('<span style="color:{};">{}/{}</span>', color, sent, total)
    sequence_progress_display.short_description = 'Emails enviados'

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
                    value = timezone.localtime(value).strftime('%Y-%m-%d %H:%M:%S')
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