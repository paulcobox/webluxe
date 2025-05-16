from instructors.models import Instructors  # Ajusta esta importación según tu estructura de proyecto
from content_site.models import Testimony
from random import sample

def global_context(request):
    instructors = Instructors.objects.filter(is_active = True)
    list_testimony =  Testimony.objects.filter(is_active = True)
    # if list_testimony.count() >= 3:
        # list_testimony = sample(list(list_testimony), 3)
    return {
        'instructors': instructors,
        'list_testimony' : list_testimony
        # Otras variables globales que necesites
    }