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
    created_date = models.DateTimeField(auto_now_add = True, verbose_name = "Fecha de Creación")
    modified_date = models.DateTimeField(auto_now = True, verbose_name = "Fecha de Modificación")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
