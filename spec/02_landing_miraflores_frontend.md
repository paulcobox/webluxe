# SPEC 02 — Plan de Implementación Frontend: Landing Miraflores Ads

**Proyecto:** webluxe — Cuban Groove Peru  
**Fecha:** 2026-05-30  
**Agente:** frontend-dev-specialist  
**Estado:** Pendiente implementación  
**Relacionado con:** `00_landing_miraflores_ads.md`, `01_landing_miraflores_backend.md`  
**Prerrequisito:** Spec 01 completado (vista y URL registradas)

---

## Resumen

Plan de implementación frontend para la landing page publicitaria de Miraflores. Consiste en 9 fases de construcción del template `landing_miraflores_ads.html` más 5 bloques de JavaScript. El template reemplaza el mínimo de arranque creado por el backend.

---

## Archivo a Crear

`templates/courses/landing_miraflores_ads.html`

---

## Observaciones Críticas del Código Existente

### Conflictos de IDs con `_base.html`
El modal global `#exampleModal` en `_base.html` (líneas 266-311) usa los IDs: `name`, `last_name`, `email`, `phone_number`, `message`, `website`, `course_of_interest`, `referer`, `user_agent`, `utm_*`. El formulario de la landing **debe usar el prefijo `ld_` en todos los IDs** para evitar que `document.getElementById()` devuelva el elemento incorrecto.

### `name` attributes sin prefijo (crítico)
`assignUTMsToAllForms()` en `_base.html` busca por `querySelectorAll('[name="utm_source"]')`, no por ID. Los atributos `name` deben ser exactamente los que espera el endpoint `create_lead`: `first_name`, `last_name`, `email`, `phone_number`, `notes`, `utm_source`, etc. Solo los atributos `id` y `for` llevan el prefijo `ld_`.

### Override del botón WhatsApp flotante
El botón `.whatsapp-icon > button` en `_base.html` tiene `data-bs-toggle="modal" data-bs-target="#exampleModal"`. Bootstrap 5 interpreta estos atributos en el momento del click y abre el modal antes de que cualquier listener personalizado se ejecute. Para redirigir a `wa.me` directo, el JS de la landing debe **remover ambos atributos** con `removeAttribute()` antes de agregar el nuevo listener.

### Bug a NO replicar
`course_detail_district.html` línea 150 tiene `d-none d-md-block` en el contenedor del formulario, ocultándolo en mobile. El formulario de la landing **no debe tener ningún `d-none`** — visible siempre.

### Colisión de variable `course` en el loop
`{% for course in list_courses %}` sobreescribe la variable `course` del contexto dentro del bloque. Usar `{% for c in list_courses %}` en su lugar para evitar que FAQs y testimonios lean el dato incorrecto.

---

## Bloques Django a Sobreescribir

| Bloque | Contenido |
|--------|-----------|
| `{% block title %}` | Título de campaña + marca |
| `{% block meta_robots %}` | `noindex, nofollow` — OBLIGATORIO |
| `{% block meta_description %}` | `{{ course.meta_description }}` |
| `{% block meta_keywords %}` | Keywords de campaña Miraflores |
| `{% block open_graph %}` | `og:type = website`, imagen del logo estático |
| `{% block twiter_card %}` | Consistente con Open Graph |
| `{% block structured_data %}` | Vacío (sin valor SEO con noindex) |
| `{% block content %}` | Todo el cuerpo de la landing |
| `{% block javascript %}` | JS específico de la landing |

---

## Fase F1 — Cabecera y bloques meta

**Qué construir:** Declaración del template y todos los bloques del `<head>`.

**Acciones:**
1. `{% extends '_base.html' %}` y `{% load static %}` en la primera línea
2. `meta_robots`: contenido exacto `noindex, nofollow`
3. `title`: usar `course.seo_title` si existe, fallback a texto fijo de campaña
4. `meta_description`: `{{ course.meta_description }}` con fallback
5. `open_graph`: `og:type = website`, `og:url = {{ request.build_absolute_uri }}`, imagen del logo estático del proyecto
6. `structured_data`: bloque vacío

**Variables consumidas:** `course.seo_title`, `course.meta_description`, `course.meta_keywords`

**Validación:** "Ver código fuente" → `<meta name="robots" content="noindex, nofollow">` presente en el `<head>`.

---

## Fase F2 — Hero section (layout dos columnas)

**Qué construir:** Sección principal above-the-fold.

**Layout:**
- Contenedor: `container-xxl py-4` como apertura de `{% block content %}`
- Row: `row g-4 align-items-start`
- Columna izquierda (contenido): `col-12 col-lg-7` — **sin `d-none`**
- Columna derecha (formulario): `col-12 col-lg-5` — **sin `d-none d-md-block`**

**Columna izquierda:**
- `<h1 class="custom-h2 color-oran">{{ course.h1 }}</h1>` — único H1 de la página
- `<p class="custom-h2 color-cafe">{{ course.body_title | safe }}</p>`
- `<p>{{ course.technical_details | safe }}</p>`
- `<h2 class="custom-h2 color-cafe">Beneficios...</h2>` + `{{ course.benefits | safe }}`
- Tarjetas de datos destacados (precio, horario, lugar) como `row g-2` con íconos FontAwesome: `fa-tag`, `fa-clock`, `fa-map-marker-alt`

**Columna derecha:** Contiene el formulario de la Fase F3.

**Mobile vs desktop:**
- Mobile/tablet (<992px): columnas apiladas, ancho completo
- Desktop (≥992px): lado a lado 7/12 + 5/12

**Validación:** En viewport 375px ambas columnas deben ser visibles, sin scroll horizontal.

---

## Fase F3 — Formulario de lead inline (componente crítico)

**Qué construir:** Formulario de captura siempre visible.

**IDs y names:**

| Campo visible | `id` (prefijo ld_) | `name` (para backend) |
|--------------|--------------------|-----------------------|
| Nombre | `ld_first_name` | `first_name` |
| Apellido | `ld_last_name` | `last_name` |
| Email | `ld_email` | `email` |
| WhatsApp | `ld_phone` | `phone_number` |
| Consulta | `ld_notes` | `notes` |

**Campos hidden:**

| Campo | `id` | `name` |
|-------|------|--------|
| Honeypot | `ld_website` | `website` |
| Curso | `ld_course_of_interest` | `course_of_interest` |
| UTM source | `ld_utm_source` | `utm_source` |
| UTM medium | `ld_utm_medium` | `utm_medium` |
| UTM campaign | `ld_utm_campaign` | `utm_campaign` |
| UTM term | `ld_utm_term` | `utm_term` |
| UTM content | `ld_utm_content` | `utm_content` |
| Referer | `ld_referer` | `referer` |
| User agent | `ld_user_agent` | `user_agent` |

**Estructura:**
- `<form id="leadForm_miraflores">` con borde `border border-2 rounded-3 p-4`
- `{% csrf_token %}` inmediatamente después de `<form ...>`
- Título del form: `<p class="custom-h4 text-dark mb-3">Solicita más información.</p>`
- Layout campos: `row g-3`, nombre/apellido en `col-md-6`, email/WhatsApp en `col-md-6`, textarea en `col-12`
- Todos los campos visibles con clase `form-floating` (label animado Bootstrap 5)
- WhatsApp: `type="tel"`, `pattern="^\+?[0-9]{9,}$"`, `inputmode="numeric"`
- Honeypot: `style="display:none !important;"`
- Botón submit: `id="ld_submitForm"`, `type="button"`, `class="btn btn-success w-100 py-3"`, ícono `fa-whatsapp`

**Elementos de feedback:**
- Div gracias: `id="thankYouMessage_miraflores"`, `class="d-none text-center"`, mismo borde que el form
- Overlay de proceso: `id="processingOverlay_miraflores"`, `class="position-fixed top-0 start-0 w-100 h-100 d-none d-flex align-items-center justify-content-center"`, `z-index: 1050`, fondo `rgba(255,255,255,0.8)`

**Validación:** DevTools console → `document.querySelectorAll('[id="email"]').length` debe retornar `1`. En viewport 375px el formulario debe ser visible sin scroll horizontal.

---

## Fase F4 — Sección de video YouTube (condicional)

**Qué construir:** Embed responsivo con renderizado condicional.

**Estructura:**
- Envuelto en `{% if video_embed_url %}` / `{% endif %}`
- Contenedor: `container-xxl py-4`
- Título: `<h2 class="custom-h2 color-cafe text-center mb-4">`
- Wrapper responsive: `<div class="ratio ratio-16x9">` (clase Bootstrap 5 nativa)
- `<iframe src="{{ video_embed_url }}" allowfullscreen loading="lazy" frameborder="0">`

**Validación:** Con `video_embed_url` vacío la sección no debe aparecer en el DOM renderizado.

---

## Fase F5 — Grid de cursos disponibles

**Qué construir:** Lista de cursos activos priorizando Miraflores.

**Estructura:**
- `container-xxl py-4`
- Encabezado: `<p class="section-title bg-white text-center px-3 color-oran custom-h6">` + `<p class="custom-h2 mb-2">`
- Grid: `row g-4 justify-content-center`
- Cards: `col-lg-4 col-md-6 col-12` — 3 col desktop, 2 tablet, 1 mobile
- Clase de card: `course-item bg-light` (patrón del proyecto)
- Imagen: `img-fluid`, `loading="lazy"`, `style="width:100%; height:200px; object-fit:cover;"`
- Badge precio: `<div class="infoPrice"><strong>S/.{{ c.price }}</strong></div>`
- Cuerpo: título `<h3 class="custom-h5">`, horario con `fa-star color-oran`, ubicación con `fa-map-marker-alt`, instructor con `fa-chalkboard-teacher`
- Card completa como enlace: `<a href="{% url 'courses_detail' c.slug %}">`

**Nota crítica:** Usar `{% for c in list_courses %}` (no `course`) para evitar sobreescribir la variable de contexto principal.

**Envolver en:** `{% if list_courses %}` para no mostrar sección vacía.

**Validación:** Con 3+ cursos, grid de 3 columnas en desktop sin overflow.

---

## Fase F6 — Sección de testimonios

**Qué construir:** Carousel owl-carousel idéntico al de `course_detail_district.html`.

**Estructura:** Copiar exactamente la sección "Testimonial" de `course_detail_district.html` líneas 346-373.

**Clase del carousel:** `owl-carousel testimonial-carousel` — `main.js` la inicializa automáticamente, no re-inicializar.

**Variables consumidas:** `list_testimony` (context processor global, siempre disponible).

**Envolver en:** `{% if list_testimony %}`.

**Validación:** Carousel funcional sin errores de consola JS.

---

## Fase F7 — Sección de FAQs

**Qué construir:** Accordion de preguntas frecuentes del curso.

**Posición:** Construir **antes** de la Fase F5 (grid de cursos) para que la variable `course` no esté sobreescrita por el loop.

**Estructura:**
- `container-xxl py-4`
- `<h2 class="custom-h2 color-cafe">Preguntas Frecuentes sobre las clases de salsa en Miraflores</h2>`
- Accordion ID: `faqAccordion_miraflores` (evita colisión)
- Loop: `{% for faq in course.faqs.all %}`
- IDs de ítems: `headingMf{{ forloop.counter }}`, `collapseMf{{ forloop.counter }}`

**Validación:** Click en una pregunta expande la respuesta. Solo una abierta a la vez.

---

## Fase F8 — Barra móvil inferior

**Qué construir:** Barra fija en el fondo, solo en mobile, con acceso directo a WhatsApp.

**Decisión de diseño:** A diferencia de `course_detail_district.html` (que abre el modal), en la landing la barra va **directo a WhatsApp** porque el formulario inline ya está visible en la página.

**Estructura:**
- `id="mobileContactBar"`, `class="mobile-contact-bar d-block d-md-none"`
- Botón: `id="ld_openWhatsApp"`, **sin** `data-bs-toggle` ni `data-bs-target`
- Texto: "¡Escríbenos por WhatsApp!" con ícono `fa-whatsapp`
- El comportamiento lo asigna el JS en Fase F9.2

**Validación:** En viewport 375px la barra aparece fija en el fondo. Click → abre WhatsApp directo sin modal.

---

## Fase F9 — JavaScript (`{% block javascript %}`)

Este bloque se inyecta después de todos los scripts de `_base.html`.

### F9.1 — Override del botón WhatsApp flotante

**Cuándo:** `DOMContentLoaded`

**Lógica:**
1. Seleccionar `document.querySelector('.whatsapp-icon button')`
2. `removeAttribute('data-bs-toggle')`
3. `removeAttribute('data-bs-target')`
4. Agregar `addEventListener('click', () => window.open('https://wa.me/51933275831', '_blank'))`
5. GTag event: `gtag('event', 'whatsapp_direct_landing_miraflores', {...})`

**Por qué remover los atributos:** Bootstrap 5 interpreta `data-bs-toggle="modal"` en el evento click y abre el modal antes de que el listener personalizado ejecute. Sin `removeAttribute`, el modal se abre Y WhatsApp se abre simultáneamente.

### F9.2 — Override del botón móvil inferior

**Cuándo:** `DOMContentLoaded`

**Lógica:**
- `document.getElementById('ld_openWhatsApp')`
- `addEventListener('click', () => window.open('https://wa.me/51933275831?text=...', '_blank'))`

### F9.3 — Ajuste de posición del ícono WhatsApp flotante

Cuando la barra móvil inferior está visible, elevar el ícono flotante a `bottom: 80px` para que no se solapen. Reutilizar la lógica de `course_detail_district.html` líneas 422-428.

### F9.4 — Submit del formulario de la landing

**Flujo completo:**
1. `document.getElementById('ld_submitForm').addEventListener('click', function() {...})`
2. Llamar `assignUTMsToAllForms()`
3. `document.getElementById('leadForm_miraflores').checkValidity()` — si inválido: agregar `was-validated` y retornar
4. Mostrar `processingOverlay_miraflores` (remover `d-none`)
5. `grecaptcha.ready(() => grecaptcha.execute('{{ RECAPTCHA_SITE_KEY }}', { action: 'submit' }).then(token => {...}))`
6. Construir `FormData` del form, agregar `recaptcha_token: token`
7. `fetch('/create-lead/', { method: 'POST', body: formData, headers: { 'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value } })`
8. En éxito (`data.success === true`):
   - Leer valores con `getElementById('ld_first_name').value`, `getElementById('ld_last_name').value`, etc.
   - Construir `whatsappMessage` con los datos
   - `gtag('event', 'whatsapp_send_landing_miraflores', { categoria: 'lead', accion: 'enviar', etiqueta: 'landing_miraflores_ads' })`
   - `window.open('https://wa.me/51933275831?text=' + encodeURIComponent(whatsappMessage), '_blank')`
   - Ocultar form: `leadForm_miraflores.classList.add('d-none')`
   - Mostrar gracias: `thankYouMessage_miraflores.classList.remove('d-none')`
9. En error: `alert('Error al crear el lead.')`
10. En `finally`: ocultar `processingOverlay_miraflores`

**Nota crítica:** Los valores se leen con `getElementById('ld_first_name')`, NO con `getElementById('name')` como hace el modal global.

### F9.5 — Ocultar barra móvil al abrir modales del navbar

Reutilizar la lógica de `course_detail_district.html` líneas 396-416 para ocultar `#mobileContactBar` cuando se abre `#exampleModal` o `#successModal`.

---

## Orden de Construcción Recomendado

```
F1 → F3 → F2 → F7 → F5 → F6 → F4 → F8 → F9
```

- **F1 primero**: permite verificar bloques desde el inicio
- **F3 antes que F2**: el formulario es el componente más crítico; conviene validarlo solo antes de integrarlo en el layout
- **F7 antes que F5**: FAQs usan la variable `course`, que el loop de F5 sobreescribiría
- **F9 al final**: construir JS cuando todos los elementos del DOM ya existen

---

## Riesgos Frontend

| Riesgo | Severidad | Mitigación |
|--------|-----------|------------|
| IDs duplicados con modal global (`name`, `email`, etc.) | Alta | Prefijo `ld_` en todos los IDs. Verificar: `document.querySelectorAll('[id="email"]').length === 1` |
| Bootstrap abre el modal al click del WhatsApp flotante | Alta | `removeAttribute('data-bs-toggle')` y `removeAttribute('data-bs-target')` en F9.1 |
| Formulario oculto en mobile (bug del template original) | Alta | Sin `d-none d-md-block` en el contenedor del formulario |
| Variable `course` sobreescrita por el loop de cursos | Media | Usar `{% for c in list_courses %}` en F5 |
| `processingOverlay` queda visible si el fetch falla | Media | Bloque `finally` garantizado en la Promise chain |
| Barra móvil tapa el botón submit del formulario | Baja | `padding-bottom: 80px` en el contenedor principal en mobile |
| `assignUTMsToAllForms()` no llena campos `ld_*` | Baja | La función busca por `name` attribute, no por ID — funcionará si los `name` son correctos |

---

## Checklist de QA

- [ ] `<meta name="robots" content="noindex, nofollow">` presente en el head
- [ ] Formulario visible en viewport 375px sin scroll horizontal
- [ ] `document.querySelectorAll('[id="email"]').length === 1` en consola
- [ ] Click en botón WhatsApp flotante → abre `wa.me` directo, NO el modal
- [ ] Submit vacío → muestra validación Bootstrap (campos en rojo), NO envía request
- [ ] Submit con datos válidos → muestra overlay → desaparece overlay → muestra div de gracias → abre WhatsApp
- [ ] `{% if video_embed_url %}` — con URL vacía la sección no aparece en el DOM
- [ ] Grid de cursos: 3 columnas en desktop (1280px), 2 en tablet (768px), 1 en mobile (375px)
- [ ] Carousel de testimonios funcional (sin errores JS)
- [ ] FAQs: accordion abre y cierra correctamente
- [ ] Barra móvil en 375px: fija en el fondo, click → WhatsApp directo
