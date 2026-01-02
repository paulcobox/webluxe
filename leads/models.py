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
    utm_source = models.CharField(max_length=100, null=True, blank=True)
    utm_medium = models.CharField(max_length=100, null=True, blank=True)
    utm_campaign = models.CharField(max_length=100, null=True, blank=True)
    utm_term = models.CharField(max_length=100, null=True, blank=True)
    utm_content = models.CharField(max_length=100, null=True, blank=True)
    referer = models.TextField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add = True, verbose_name = "Fecha de Creación")
    modified_date = models.DateTimeField(auto_now = True, verbose_name = "Fecha de Modificación")
    omnisend_synced_at = models.DateTimeField(null=True, blank=True)
    omnisend_last_status = models.IntegerField(null=True, blank=True)
    omnisend_last_error = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


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