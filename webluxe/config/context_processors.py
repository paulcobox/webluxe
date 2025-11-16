from instructors.models import Instructors  # Ajusta esta importación según tu estructura de proyecto
from content_site.models import Testimony
from django.conf import settings
from django.core.cache import cache

def global_context(request):
    instructors = cache.get_or_set('instructors_active', Instructors.objects.filter(is_active=True), 86400)
    list_testimony = cache.get_or_set('testimony_active', Testimony.objects.filter(is_active=True), 86400)

    return {
        'instructors': instructors,
        'list_testimony': list_testimony,
        "RECAPTCHA_SITE_KEY": settings.RECAPTCHA_SITE_KEY
    }