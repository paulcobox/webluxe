# SPEC 00 — Landing Page Publicitaria Miraflores

**Proyecto:** webluxe — Cuban Groove Peru  
**Fecha:** 2026-05-30  
**Estado:** Pendiente implementación  
**Prioridad:** Alta — para campaña publicitaria en redes sociales

---

## Objetivo

Crear una landing page independiente para captar leads de personas interesadas en cursos de baile en el distrito de Miraflores. La página será usada como destino de anuncios pagados en Instagram, Facebook y TikTok.

---

## Requerimientos

### Funcionales
- Mostrar cursos activos disponibles en Miraflores
- Formulario de captura de lead visible siempre (mobile + desktop)
- Video de YouTube embebido en sección hero
- Botón flotante de WhatsApp en esquina inferior derecha (directo al chat, no modal)
- Diseño mobile-first optimizado para tráfico de redes sociales

### No Funcionales
- URL dedicada para tracking de campañas con UTMs
- `noindex, nofollow` — no debe indexarse en Google (es página de ads)
- Reutilizar el endpoint `/create-lead/` sin modificaciones
- Cero riesgo de regresión sobre la página SEO existente `/clases-de-salsa-en-miraflores/`

---

## Decisiones Técnicas

| Decisión | Elección | Justificación |
|----------|----------|---------------|
| URL | `/landing/miraflores-baile/` | Separada del SEO, rastreable con UTMs |
| Template | Archivo nuevo `landing_miraflores_ads.html` | Sin riesgo de romper página SEO existente |
| IDs del formulario | Prefijo `ld_*` | Evita conflictos con modal global de `_base.html` |
| WhatsApp flotante | Override JS → directo a `wa.me` | Landing de ads no debe abrir modal |
| SEO robots | `noindex, nofollow` | Página de publicidad, no indexable |
| Migraciones | Ninguna | Lead model ya tiene todos los campos necesarios |

---

## Análisis de Impacto por Componente

### `courses/views.py` — AGREGAR (sin modificar existentes)
- Nueva clase `MirafloresLandingAdsView(TemplateView)`
- No tocar `MirafloresDetailTemplateView` (tiene SEO acumulado)
- **Riesgo:** Ninguno

### `courses/urls.py` — 1 línea nueva
- `path('landing/miraflores-baile/', MirafloresLandingAdsView.as_view(), name='landing_miraflores_ads')`
- Posición: antes del `path('clases-baile/<slug:course_slug>/', ...)` (última línea)
- **Riesgo:** Ninguno

### `templates/courses/landing_miraflores_ads.html` — ARCHIVO NUEVO
- Estructura: hero + video + formulario + cursos + testimonios
- Formulario siempre visible (sin `d-none d-md-block`)
- **Riesgo:** Ninguno (archivo nuevo)

### `leads/views.py` — SIN CAMBIOS
- El endpoint `/create-lead/` se reutiliza sin modificaciones
- Toda la lógica de seguridad funciona automáticamente

### `leads/models.py` — SIN CAMBIOS
- UTM fields ya existen: `utm_source`, `utm_medium`, `utm_campaign`, `utm_term`, `utm_content`

### `_base.html` — SIN CAMBIOS
- El botón WhatsApp flotante existente se sobreescribe vía JS en el template

---

## Implementación Detallada

### 1. Backend — `courses/views.py`

Agregar al final del archivo:

```python
class MirafloresLandingAdsView(TemplateView):
    template_name = 'courses/landing_miraflores_ads.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = get_object_or_404(Course, slug='clases-de-salsa-en-miraflores')
        courses = Course.objects.filter(is_active=True).annotate(
            order_priority=Case(
                When(Q(place__icontains='miraflores'), then=Value(0)),
                default=Value(1),
                output_field=IntegerField(),
            )
        ).order_by('order_priority', 'title')
        context['course'] = course
        context['list_courses'] = [c for c in courses if c.pk != course.pk]
        context['video_embed_url'] = ''  # reemplazar con ID del video de YouTube
        return context
```

> **Nota:** El filtro usa `place__icontains='miraflores'` (correcto). La vista SEO existente tenía un bug usando `surco` — no lo replicamos.

### 2. Backend — `courses/urls.py`

Agregar import y path:

```python
# En el import:
from .views import ..., MirafloresLandingAdsView

# En urlpatterns, antes de courses_detail:
path('landing/miraflores-baile/', MirafloresLandingAdsView.as_view(), name='landing_miraflores_ads'),
```

### 3. Frontend — `templates/courses/landing_miraflores_ads.html`

**Estructura del template:**

```
{% extends '_base.html' %}

[META BLOCK]
- noindex, nofollow
- Open Graph para redes sociales
- Title específico para la campaña

[CONTENT BLOCK]

SECCIÓN 1 — HERO
- H1 de la campaña
- Sub-headline con propuesta de valor
- Botón CTA → scroll al formulario (#ld-form)
- Video YouTube (iframe responsive, condicional a video_embed_url)

SECCIÓN 2 — FORMULARIO (siempre visible, sin d-none)
- id="ld-form" (target del scroll del CTA)
- IDs únicos: ld_name, ld_last_name, ld_email, ld_phone_number, ld_notes
- names estándar del POST: first_name, last_name, email, phone_number, notes
- Hidden fields: course_of_interest, utm_*, honeypot (website)
- Botón submit verde con ícono WhatsApp

SECCIÓN 3 — CURSOS
- Tarjetas de cursos activos (priorizando Miraflores)
- Layout: 1 col mobile, 2-3 col desktop

SECCIÓN 4 — TESTIMONIOS
- Carousel de list_testimony (context processor global)

[JAVASCRIPT BLOCK]
- Override del botón WhatsApp flotante → directo a wa.me
- Submit con grecaptcha.execute() → fetch '/create-lead/'
- GTag event de conversión
- assignUTMsToAllForms() al cargar
```

**JavaScript crítico — Override WhatsApp flotante:**
```javascript
document.addEventListener('DOMContentLoaded', function() {
    const waIcon = document.querySelector('.whatsapp-icon button');
    if (waIcon) {
        waIcon.removeAttribute('data-bs-toggle');
        waIcon.removeAttribute('data-bs-target');
        waIcon.addEventListener('click', function(e) {
            e.preventDefault();
            window.open('https://wa.me/51991337159?text=Hola%2C+quiero+informes+sobre+las+clases+en+Miraflores', '_blank');
        });
    }
});
```

---

## Riesgos y Mitigaciones

| Riesgo | Severidad | Mitigación |
|--------|-----------|------------|
| IDs duplicados con modal global de `_base.html` | Alta | IDs con prefijo `ld_` en todos los inputs |
| WhatsApp abre modal en vez de ir directo | Alta | Override JS eliminando `data-bs-toggle` y `data-bs-target` |
| Bug existente: vista SEO filtra por `surco` en vez de `miraflores` | Media | Corregido en nueva vista — no replicar el bug |
| Video placeholder vacío en primera versión | Baja | Condicional `{% if video_embed_url %}` en template |
| Formulario oculto en móvil (como en template actual) | Alta | No usar `d-none d-md-block` — formulario siempre visible |

---

## Información Pendiente del Usuario

Antes del despliegue final se requiere:

- [ ] **URL del video de YouTube** — para el embed en el hero
- [ ] **Copy del H1** — texto publicitario principal (ej: "Aprende Salsa en Miraflores")
- [ ] **Confirmación de cursos a mostrar** — ¿solo Miraflores o todos activos con Miraflores primero?

---

## Checklist de Implementación

### Backend (`django-backend-specialist`)
- [ ] Agregar `MirafloresLandingAdsView` en `courses/views.py`
- [ ] Agregar import en `courses/urls.py`
- [ ] Agregar `path('landing/miraflores-baile/', ...)` en `courses/urls.py`
- [ ] Ejecutar `python manage.py check` — sin errores

### Frontend (`frontend-dev-specialist`)
- [ ] Crear `templates/courses/landing_miraflores_ads.html`
- [ ] Implementar bloque `meta_robots` con `noindex, nofollow`
- [ ] Hero section con video YouTube condicional
- [ ] Formulario siempre visible con IDs `ld_*`
- [ ] Tarjetas de cursos responsivas
- [ ] Sección de testimonios con carousel
- [ ] JS: override WhatsApp flotante → directo a `wa.me`
- [ ] JS: submit con reCAPTCHA + fetch `/create-lead/`
- [ ] JS: GTag evento de conversión

### QA
- [ ] Verificar formulario visible en móvil (Chrome DevTools, viewport 375px)
- [ ] Verificar botón WhatsApp va directo al chat (no abre modal)
- [ ] Verificar UTMs se capturan en el modelo Lead
- [ ] Verificar video YouTube embebido es responsivo
- [ ] Verificar `noindex` en el head del HTML
- [ ] Verificar secuencia de emails se dispara al crear lead
