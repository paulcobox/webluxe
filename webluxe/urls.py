"""webluxe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('courses.urls')),
    path('', include('content_site.urls')),
    path('', include('instructors.urls')),
    path('', include('leads.urls')),
    path('', include('blog.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

redirect_patterns = [
    re_path(r'^courses/salsa-cubana-basico/$', lambda r: redirect('/clases-baile/salsa-principiantes/', permanent=True)),
    re_path(r'^courses/afrocubano/$', lambda r: redirect('/clases-baile/afro/', permanent=True)),
    re_path(r'^courses/tecnica-para-la-danza-y-disociacion-corporal/$', lambda r: redirect('/clases-baile/danza/', permanent=True)),
    re_path(r'^courses/timba-pasos-sueltos/$', lambda r: redirect('/clases-baile/salsa/', permanent=True)),
    re_path(r'^courses/reparto/$', lambda r: redirect('/clases-baile/salsa/', permanent=True)),
    re_path(r'^courses/cuban-lady-style/$', lambda r: redirect('/clases-baile/salsa/', permanent=True)),
    re_path(r'^courses/timba-session-coreografico/$', lambda r: redirect('/clases-baile/salsa/', permanent=True)),
    re_path(r'^courses-group/$', lambda r: redirect('/clases-baile/', permanent=True)),
    re_path(r'^courses_virtual/$', lambda r: redirect('/clases-baile/online/', permanent=True)),
    
    # =========================
    # BLOG ANTIGUO → BLOG LOCAL MIRAFLORES
    # =========================
    re_path(
        r'^blog/donde-bailar-salsa-en-miraflores/?$',
        lambda r: redirect(
            '/clases-de-salsa-en-miraflores/donde-bailar-salsa-en-miraflores/',
            permanent=True
        )
    ),
    re_path(
        r'^blog/beneficios-de-bailar-salsa/?$',
        lambda r: redirect(
            '/clases-de-salsa-en-miraflores/beneficios-de-bailar-salsa/',
            permanent=True
        )
    ),
    re_path(
        r'^blog/beneficios-de-bailar-salsa?$',
        lambda r: redirect(
            '/clases-de-salsa-en-miraflores/beneficios-de-bailar-salsa/',
            permanent=True
        )
    ),
    re_path(
        r'^blog/beneficios-de-bailar-salsa-en-miraflores/?$',
        lambda r: redirect(
            '/clases-de-salsa-en-miraflores/beneficios-de-bailar-salsa/',
            permanent=True
        )
    ),
    re_path(
        r'^blog/beneficios-de-bailar-salsa-en-miraflores?$',
        lambda r: redirect(
            '/clases-de-salsa-en-miraflores/beneficios-de-bailar-salsa/',
            permanent=True
        )
    ),
    re_path(
        r'^blog/la-casa-de-la-salsa-miraflores/?$',
        lambda r: redirect(
            '/clases-de-salsa-en-miraflores/casa-de-la-salsa/',
            permanent=True
        )
    ),
    re_path(
        r'^blog/la-casa-de-la-salsa-miraflores?$',
        lambda r: redirect(
            '/clases-de-salsa-en-miraflores/casa-de-la-salsa/',
            permanent=True
        )
    ),
    re_path(
        r'^encuentra-tu-estilo-ideal/?$',
        lambda r: redirect(
            '/clases-de-salsa-en-miraflores/encuentra-tu-estilo-ideal/',
            permanent=True
        )
    ),

    
    # =========================
    # SLUGS CON UNDERSCORE → GUION MEDIO (SEO)
    # =========================
    re_path(
        r'^clases-de-salsa-en-san_isidro/?$',
        lambda r: redirect(
            '/clases-de-salsa-en-san-isidro/',
            permanent=True
        )
    ),
    
    re_path(
        r'^terms_conditions/?$',
        lambda r: redirect(
            '/terms-conditions/',
            permanent=True
        )
    ),
    
    re_path(
        r'^instructor/lucero-coronado/?$',
        lambda r: redirect(
            '/instructor/luxe-coronado/',
            permanent=True
        )
    ),
    
    re_path(
        r'^instructor/lucero-coronado?$',
        lambda r: redirect(
            '/instructor/luxe-coronado/',
            permanent=True
        )
    ),
    
    re_path(
        r'^courses/salsa-principiantes/?$',
        lambda r: redirect('/clases-baile/salsa-principiantes/', permanent=True)
    ),
    
    re_path(
        r'^courses/salsa-principiantes?$',
        lambda r: redirect('/clases-baile/salsa-principiantes/', permanent=True)
    ),
    
    re_path(
        r'^courses_choreography/?$',
        lambda r: redirect('/clases-baile/', permanent=True)
    ),

    re_path(
        r'^courses_choreography?$',
        lambda r: redirect('/clases-baile/', permanent=True)
    )
    

]

# urlpatterns += redirect_patterns
urlpatterns = redirect_patterns + urlpatterns