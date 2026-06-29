---
name: project-landing-pages
description: Patron arquitectonico para landing pages de publicidad pagada — URL separada de SEO, template independiente extendiendo _base.html
metadata:
  type: project
---

Se establecio el patron para landing pages de ads en el proyecto webluxe.

**Decision:** Landing pages de publicidad usan URL y template propios, separados de las paginas SEO equivalentes.

**Por que:** La pagina `/clases-de-salsa-en-miraflores/` tiene SEO acumulado. Modificarla para ads (noindex, formulario siempre visible, WhatsApp directo) comprometeria el SEO. La solucion es una URL bajo `/landing/<nombre>/` con template independiente.

**Patron aplicado (primera instancia):**
- URL: `/landing/miraflores-baile/` en `courses/urls.py`
- Vista: `MirafloresLandingAdsView` en `courses/views.py`
- Template: `templates/courses/landing_miraflores_ads.html`
- Extiende `_base.html` (no un base minimalista) para reutilizar reCAPTCHA, UTM JS, estilos
- Usa `{% block meta_robots %}noindex, nofollow{% endblock %}` obligatoriamente
- No usa `.mobile-contact-bar` — el formulario es visible directamente en mobile

**Problema de IDs duplicados resuelto:**
- Los formularios de landing DEBEN usar IDs con prefijo `ld_*` para evitar colision con el modal global `#exampleModal` de `_base.html` que usa `id="name"`, `id="last_name"`, `id="email"`, `id="phone_number"`, `id="message"`.
- Los `name` attributes del POST se mantienen estandar (lo que consume `create_lead()`).

**Override del WhatsApp flotante:**
- `_base.html` no tiene `{% block whatsapp_icon %}` — no es overrideable via herencia de templates.
- Solucion: JS en `{% block javascript %}` remueve `data-bs-toggle`/`data-bs-target` y asigna `onclick` directo a `https://wa.me/51933275831`.

**Video YouTube:**
- Se almacena en la vista como variable de contexto `video_embed_url = ''`, no en el modelo Course.
- El template usa `{% if video_embed_url %}` para mostrar el embed o un placeholder.
- Formato requerido: `https://www.youtube.com/embed/VIDEO_ID`.

**Why:** Trafico de ads en redes sociales es predominantemente mobile. El formulario oculto en mobile de `course_detail_district.html` (d-none d-md-block) es incompatible con una landing de conversion.

**How to apply:** Cada nueva landing page de publicidad debe seguir este patron. Si se crean 3+ landing pages, considerar agregar `{% block whatsapp_icon %}` en `_base.html` para override limpio.
