from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Lead
from courses.models import Course

# Create your views here.

@csrf_exempt
def create_lead(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        course_of_interest_id = request.POST.get('course_of_interest')
        notes = request.POST.get('notes')
        course_of_interest = request.POST.get('course_of_interest')
        
        if course_of_interest:
            course_of_interest = Course.objects.get(title=str(course_of_interest))
        else:
            course_of_interest = None

        lead = Lead.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            course_of_interest=course_of_interest,
            notes=notes
        )

        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

