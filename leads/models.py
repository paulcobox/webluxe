from django.db import models
from courses.models import Course

class Lead(models.Model):
    # Contact information
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=False)
    phone_number = models.CharField(max_length=20, blank=True)

    # Lead's interests
    course_of_interest = models.ForeignKey(Course, on_delete = models.CASCADE, related_name = 'lead', blank = True, null = True, verbose_name = "Curso de Interes")
    status = models.CharField(max_length=50, choices=[('NEW', 'New'), ('PROSPECT', 'Prospect'), ('CUSTOMER', 'Customer')], default='NEW')
    notes = models.TextField(blank=True)
    
    
    # --- RAW (lo que llega del formulario) ---
    form_course_raw = models.CharField(max_length=200, blank=True, null=True)
    form_experience_raw = models.CharField(max_length=200, blank=True, null=True)
    form_schedule_raw = models.CharField(max_length=200, blank=True, null=True)
    form_motivation_raw = models.CharField(max_length=220, blank=True, null=True)
    form_age_raw = models.CharField(max_length=100, blank=True, null=True)

    # --- NORMALIZED (para reportes / filtros estables) ---
    form_course_key = models.CharField(max_length=120, blank=True, null=True, db_index=True)
    form_experience_key = models.CharField(max_length=120, blank=True, null=True, db_index=True)
    form_schedule_key = models.CharField(max_length=120, blank=True, null=True, db_index=True)
    form_motivation_key = models.CharField(max_length=120, blank=True, null=True, db_index=True)
    
    lead_interest_raw = models.CharField(max_length=500, blank=True, null=True)
    
    utm_source = models.CharField(max_length=100, null=True, blank=True)
    utm_medium = models.CharField(max_length=100, null=True, blank=True)
    utm_campaign = models.CharField(max_length=100, null=True, blank=True)
    utm_term = models.CharField(max_length=100, null=True, blank=True)
    utm_content = models.CharField(max_length=100, null=True, blank=True)
    referer = models.TextField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    meta_event_id = models.CharField(max_length=100, blank=True, null=True)
    capi_sent     = models.BooleanField(default=False)
    capi_sent_at  = models.DateTimeField(null=True, blank=True)
    capi_response = models.TextField(blank=True, default='')
    created_date = models.DateTimeField(auto_now_add = True, verbose_name = "Fecha de Creación")
    modified_date = models.DateTimeField(auto_now = True, verbose_name = "Fecha de Modificación")
    omnisend_synced_at = models.DateTimeField(null=True, blank=True)
    omnisend_last_status = models.IntegerField(null=True, blank=True)
    omnisend_last_error = models.TextField(null=True, blank=True)

    # --- Kommo CRM ---
    kommo_contact_id = models.CharField(max_length=50, blank=True, null=True, db_index=True)
    kommo_deal_id           = models.CharField(max_length=50, blank=True, null=True)
    kommo_synced_at         = models.DateTimeField(null=True, blank=True)
    kommo_last_error        = models.TextField(null=True, blank=True)
    kommo_tag_sin_respuesta = models.BooleanField(default=False)

    # --- Secuencia de correos ---
    email_sequence_started_at = models.DateTimeField(null=True, blank=True)
    unsubscribed = models.BooleanField(default=False)
    unsubscribe_token = models.CharField(max_length=64, blank=True, null=True, unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class EmailSequenceLog(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'Pendiente'),
        ('SENT', 'Enviado'),
        ('FAILED', 'Fallido'),
        ('SKIPPED', 'Omitido'),
    ]

    SEQUENCE_POSITIONS = [
        (0, 'Inmediato'),
        (1, 'Día 1'),
        (2, 'Día 3'),
        (3, 'Día 7'),
        (4, 'Día 14'),
        (5, 'Día 21'),
        (6, 'Día 30'),
        (7, 'Día 45'),
        (8, 'Día 60'),
    ]

    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        related_name='email_logs',
        verbose_name="Lead"
    )
    sequence_position = models.IntegerField(
        choices=SEQUENCE_POSITIONS,
        verbose_name="Posición en secuencia"
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING',
        verbose_name="Estado"
    )
    celery_task_id = models.CharField(max_length=255, blank=True, null=True, verbose_name="ID tarea Celery")
    sent_at = models.DateTimeField(null=True, blank=True, verbose_name="Enviado el")
    error_message = models.TextField(blank=True, null=True, verbose_name="Error")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Log de secuencia de email"
        verbose_name_plural = "Logs de secuencia de emails"
        unique_together = ('lead', 'sequence_position')
        ordering = ['lead', 'sequence_position']

    def __str__(self):
        return f"{self.lead} — pos {self.sequence_position} — {self.status}"


class CastingRegistration(models.Model):
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    occupation = models.CharField(max_length=255, blank=True, null=True)
    district = models.CharField(max_length=255, blank=True, null=True)
    dancing_experience = models.TextField(blank=True, null=True)
    genres = models.TextField(blank=True, null=True)
    experience_competing_teaching = models.TextField(blank=True, null=True)
    motivation = models.TextField(blank=True, null=True)
    goals = models.TextField(blank=True, null=True)
    practice_time_commitment = models.TextField(blank=True, null=True)
    investment_willingness = models.TextField(blank=True, null=True)
    long_term_commitment = models.BooleanField(default=False)
    other_commitments = models.TextField(blank=True, null=True)
    availability = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    omnisend_synced_at = models.DateTimeField(null=True, blank=True)
    omnisend_last_status = models.IntegerField(null=True, blank=True)
    omnisend_last_error = models.TextField(null=True, blank=True)


    def __str__(self):
        return self.full_name