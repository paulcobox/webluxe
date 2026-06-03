# CLAUDE.md

Guía completa para Claude Code al trabajar en este repositorio.

## Descripción del Proyecto

**webluxe** es una aplicación Django 5.0 para una academia de baile (Cuban Groove Peru). Gestiona cursos, instructores, blog, captación de leads y una secuencia automatizada de 9 emails de nurturing.

- Framework: Django 5.0.6 + PostgreSQL + Redis + Celery
- Lenguaje: Python 3
- Producción: cubangrooveperu.com (IP: 104.248.113.83)
- Admin email: paulcofiis@gmail.com
- From email: `"Cuban Groove <info@cubangrooveperu.com>"`
- Idioma: Español (es) — Zona horaria: America/Lima

---

## Stack Tecnológico

| Capa | Tecnología |
|------|-----------|
| Framework | Django 5.0.6 |
| Base de datos | PostgreSQL |
| Cache / Broker | Redis (`redis://127.0.0.1:6379/0`) |
| Tareas async | Celery + Celery Beat (django_celery_beat) |
| Resultados Celery | django-db (django_celery_results) |
| Rich text | CKEditor |
| Frontend | Bootstrap + Bootstrap Icons + FontAwesome |
| Email | SMTP con TLS (config via .env) |
| CRM externo | Omnisend API |
| reCAPTCHA | Google reCAPTCHA v3 |

---

## Estructura de Apps (6 módulos)

```
webluxe/
├── users/          → CustomUser (AbstractUser + campo age)
├── instructors/    → Perfiles de instructores con redes sociales
├── courses/        → Catálogo de cursos de baile (con SEO)
├── blog/           → Blog geolocalizado por distrito de Lima
├── content_site/   → Home, FAQ, Testimonios, páginas estáticas, referidos
└── leads/          → Captura de leads + secuencia de 9 emails (Celery)
```

---

## Modelos y Relaciones

### users/models.py
- **CustomUser** — extiende `AbstractUser`
  - `age` (PositiveIntegerField, nullable)
  - Configurado como `AUTH_USER_MODEL`

### instructors/models.py
- **Instructors**
  - `name`, `slug` (auto desde name), `is_active`
  - `tags_about_me`, `tags_mission` (pipe-separated, se parsean en views)
  - `specialty`, `about_me` (RichTextField), `mission` (RichTextField)
  - `image`
  - Social: `facebook`, `tiktok`, `instagram`, `youtube` (URLField)
  - Relacionado a Course via `related_name='course'`
  - Cacheado 24h en context processor

### courses/models.py
- **Course**
  - `title` (unique), `slug` (auto desde title), `is_active`, `is_like`, `is_banner_home`
  - `schedule`, `price`, `place`, `district`
  - `instructor` (FK → Instructors, `related_name='course'`)
  - Imágenes: `image`, `image_banner_top`, `image_fiz`, `image_fid`
  - Video: `image_video_url`, `video_url` (URLField), `video_mp4`
  - Contenido: `body` (RichTextField), `body_title`, `technical_details` (RichTextField), `benefits` (RichTextField)
  - SEO: `seo_title`, `meta_description`, `meta_keywords`, `h1`, `h2`
  - Tipos: Virtual, Personalizada, Grupal, Coreografia
  - Propiedad `short_body` para listados
- **Feature** — FK Course (`related_name='feature'`): `description`
- **FAQ** — FK Course (`related_name='faqs'`): `question`, `answer`

### blog/models.py
- **Post**
  - `location` (Miraflores, San Isidro, Surco, Lince, General)
  - `title`, `slug` (auto desde title), `visible`
  - `author` (FK → CustomUser)
  - `excerpt`, `content` (RichTextField), `image`, `published_date`
  - Propiedad `clean_excerpt`

### content_site/models.py
- **Testimony** — `name`, `profession`, `description` (RichTextField), `video`, `imagen`, `is_active`, `google_url` — cacheado 24h
- **Invitated** — sistema de referidos: `student_name`, `student_email`, `friend_name`, `friend_phone`, `notes` — previene duplicados por teléfono
- **FAQ** — global: `question`, `answer` (RichTextField), `category` (principiantes/adultos/modalidades/ubicacion/ropa/general), `is_active`

### leads/models.py
- **Lead**
  - Contacto: `first_name`, `last_name`, `email`, `phone_number`
  - Interés: `course_of_interest` (FK → Course, nullable, `related_name='lead'`), `status` (NEW/PROSPECT/CUSTOMER), `notes`
  - Form raw: `form_course_raw`, `form_experience_raw`, `form_schedule_raw`, `form_motivation_raw`
  - Form normalizado: `form_course_key`, `form_experience_key`, `form_schedule_key`, `form_motivation_key`, `lead_interest_raw`
  - UTM tracking: `utm_source`, `utm_medium`, `utm_campaign`, `utm_term`, `utm_content`, `referer`, `user_agent`
  - Omnisend: `omnisend_synced_at`, `omnisend_last_status`, `omnisend_last_error`
  - Email sequence: `email_sequence_started_at`, `unsubscribed` (bool), `unsubscribe_token` (unique, 64 chars)
- **EmailSequenceLog**
  - FK Lead (`related_name='email_logs'`)
  - `sequence_position` (0-8): Inmediato, Día 1, 3, 7, 14, 21, 30, 45, 60
  - `status` (PENDING/SENT/FAILED/SKIPPED)
  - `celery_task_id`, `sent_at`, `error_message`, `created_at`
  - Unique constraint: `(lead, sequence_position)`
- **CastingRegistration** — formulario de audición multi-step
  - Contacto: `full_name`, `phone`, `email`
  - Info: `occupation`, `district`, `dancing_experience`, `genres`, `experience_competing_teaching`
  - Personal: `motivation`, `goals`, `practice_time_commitment`, `investment_willingness`, `long_term_commitment` (bool), `other_commitments`, `availability` (bool)
  - Omnisend: `omnisend_synced_at`, `omnisend_last_status`, `omnisend_last_error`

---

## URLs por App

### webluxe/urls.py (raíz)
- Incluye todas las apps
- Redirects 301 para URLs legacy (underscores → hyphens, rutas antiguas de cursos y blog)
- Sirve media en desarrollo

### courses/urls.py
- `/clases-baile/` — todos los cursos
- `/clases-baile/online/` — cursos virtuales
- `/clases-baile/particulares/` — clases privadas
- `/coreografia-de-boda-lima/` — coreografía de boda
- `/clases-de-salsa-en-surco/`, `/en-miraflores/`, `/en-san-isidro/`, `/en-lince/`, `/en-lima/`
- `/clases-de-salsa-cerca-de-mi/`
- `/academia-de-salsa-en-lima/`
- `/clases-baile/<slug:course_slug>/` — detalle de curso

### instructors/urls.py
- `/instructor/` — lista de instructores
- `/instructor/<slug:instructor_slug>/` — detalle de instructor

### content_site/urls.py
- `/` — Homepage
- `/contact/`, `/privacy-policies/`, `/terms-conditions/`, `/thankyou/`
- `/invite-friend/`, `/invite-success/`
- `/preguntas-frecuentes/`
- `/enviar-correo/` — endpoint de prueba de email
- `/sitemap.xml`, `/sitemap-blog.xml`, `/sitemap-general.xml`, `/sitemap-miraflores.xml`
- `/robots.txt`, `/favicon.ico`, `/favicon.png`

### leads/urls.py
- `/create-lead/` — crear lead (AJAX, respuesta JSON)
- `/casting/` — paso 1 del formulario (BasicInfoForm)
- `/casting/additional-info/` — paso 2 (AdditionalInfoForm, session-based)
- `/casting/thank-you/` — confirmación
- `/unsubscribe/<str:token>/` — desuscripción de emails

### blog/urls.py
- `/blog/` — listado
- `/clases-de-salsa-en-miraflores/<slug>/`
- `/clases-de-salsa-en-san-isidro/<slug>/`
- `/clases-de-salsa-en-surco/<slug>/`
- `/blog/<slug>/` — post general

---

## Vistas por App

### courses/views.py — todas CBV (TemplateView)
- `CoursesGroupAllTemplateView` — prioridad: Principiantes primero, "Próximamente" al final
- `CoursesDetailOnlineTemplateView`, `CoursesDetailParticularTemplateView`, `CoursesDetailEventsTemplateView`
- `SurcoDetailTemplateView`, `MirafloresDetailTemplateView`, `LinceDetailTemplateView`, `SanIsidroDetailTemplateView`, `LimaDetailTemplateView`
- `SalsaCercaDeMiTemplateView`, `AcademiaSalsaLimaTemplateView`
- `CoursesDetailTemplateView` — detalle por slug
- Contexto común: `course`, `list_course_you_might_like`, `course_title_zone`

### instructors/views.py — CBV
- `InstructorsTemplateView`, `InstructorsDetailTemplateView`
- Parsea `tags_about_me` (pipe-separated) en lista en la vista

### content_site/views.py
- `HomePageView` — cursos en banner, recomendaciones
- `FAQListView` — FAQs agrupadas por categoría
- `ContactTemplateView`, `PrivacyPoliciesTemplateView`, `TermsConditionsTemplateView`, `ThankYouTemplateView`
- `InvitatedTemplateView` (GET/POST), `InvitatedSuccessTemplateView`
- `test_email()` — función para probar envío de email
- `sitemap_view()`, `sitemap_blog_view()`, etc. — archivos XML estáticos

### leads/views.py — funciones
- `create_lead()` — flujo completo: validar reCAPTCHA → honeypot → rate limit → guardar Lead → thread email admin → programar secuencia Celery
- `validate_recaptcha()` — reCAPTCHA v3, score ≥ 0.5
- `get_client_ip()` — detecta IP real (proxy-aware)
- `send_async_email()` — envío en thread separado (para notificación admin)
- `casting_registration()`, `additional_info()`, `thank_you()` — formulario multi-step
- `unsubscribe()` — desuscripción por token

### blog/views.py — CBV
- `PostListView` (ListView) — agrupa por ubicación
- `PostDetailByLocationView` (DetailView) — filtra por location

---

## Sistema de Email Sequences (Celery)

### Flujo completo
```
Lead creado → schedule_email_sequence(lead)
                    ↓
             Genera unsubscribe_token (si no existe)
                    ↓
             9 tareas Celery programadas:
             pos 0: countdown=0        (inmediato)
             pos 1: countdown=86400    (1 día)
             pos 2: countdown=259200   (3 días)
             pos 3: countdown=604800   (7 días)
             pos 4: countdown=1209600  (14 días)
             pos 5: countdown=1814400  (21 días)
             pos 6: countdown=2592000  (30 días)
             pos 7: countdown=3888000  (45 días)
             pos 8: countdown=5184000  (60 días)
                    ↓
             Cada tarea: send_sequence_email(lead_id, sequence_position)
             → Verifica lead.unsubscribed
             → Crea/actualiza EmailSequenceLog
             → Renderiza template HTML
             → Envía email SMTP
             → Marca SENT o FAILED (max 3 retries, delay 60s)
```

### Templates de email sequence
```
templates/emails/sequence/
├── 00_immediate.html   → Bienvenida
├── 01_day1.html        → Movimiento natural
├── 02_day3.html        → Postura
├── 03_day7.html        → Respiración
├── 04_day14.html       → Marcha cubana
├── 05_day21.html       → Flujo de cadera
├── 06_day30.html       → Cadera rígida
├── 07_day45.html       → Coordinación torso-cadera
└── 08_day60.html       → Rigidez de brazos
```

### Otros templates de email
```
templates/emails/
├── new_lead_notification.html   → Notificación admin (paulcofiis@gmail.com)
├── lead_confirmation.html       → Confirmación al lead (template existe, no activo en views)
├── invitation_email.html        → Email de referido
└── unsubscribe_confirm.html     → Confirmación de desuscripción
```

### Configuración Celery (webluxe/celery.py)
- `CELERY_BROKER_URL`: Redis (env var `REDIS_URL`, default `redis://127.0.0.1:6379/0`)
- `CELERY_RESULT_BACKEND`: `'django-db'`
- Scheduler: `DatabaseScheduler` (django_celery_beat)
- Dev mode: `CELERY_TASK_ALWAYS_EAGER = True` si no hay Redis
- Zona horaria: `America/Lima`

### Arrancar servicios en desarrollo
```bash
# Terminal 1: Django
python manage.py runserver

# Terminal 2: Celery worker
celery -A webluxe worker --loglevel=info

# Terminal 3: Celery beat (tareas periódicas)
celery -A webluxe beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

---

## Caching (Dos niveles)

### Nivel 1 — Middleware HTTP
- `UpdateCacheMiddleware` (posición 1) + `FetchFromCacheMiddleware` (posición 9)
- TTL: `CACHE_MIDDLEWARE_SECONDS = 3600`
- Backend: Redis si `REDIS_URL` env var presente, sino FileCache (`C:\django_cache` en dev, `/var/tmp/django_cache` en prod)
- Max entries (file cache): 1000

### Nivel 2 — Context Processor
- `webluxe/config/context_processors.py` → `global_context()`
- Cachea durante 24h: instructores activos, testimonios activos
- Disponible en todos los templates: `instructors`, `list_testimony`, `RECAPTCHA_SITE_KEY`

---

## Seguridad en Leads

```
1. reCAPTCHA v3          → score ≥ 0.5 requerido
2. Honeypot field        → campo "website" debe estar vacío
3. Rate limiting         → 2 intentos por IP cada 60s (via Django cache)
4. Bot protection log    → /var/log/cubangroove/bot_protection.log
5. CSRF middleware        → activo en todas las vistas
6. Unsubscribe token     → 64 chars UUID-based, único por lead
```

---

## Admin Interface

### leads/admin.py
- **LeadAdmin**: progreso de secuencia color-coded (verde=9/9, naranja=parcial, gris=0)
- Inline `EmailSequenceLogInline` (read-only) para ver estado de cada email
- **CastingRegistrationAdmin**: acción "Exportar Excel" con openpyxl

### courses/admin.py
- **CourseAdmin**: inline FAQs, slug auto-generado desde title
- Filtros: `is_active`, `instructor`

### blog/admin.py
- **PostAdmin**: filtros por `location` y `visible`, slug auto-generado

### content_site/admin.py
- **FAQAdmin**: filtros por `category` e `is_active`
- Registro simple de Testimony e Invitated

### instructors/admin.py, users/admin.py
- Registro simple de sus modelos

---

## Formularios

### leads/forms.py
- **BasicInfoForm** (ModelForm → CastingRegistration): `full_name`, `phone`, `email`
- **AdditionalInfoForm** (ModelForm → CastingRegistration): todos los campos restantes del casting

### Formulario de lead principal
- No usa forms.py — captura directa en `create_lead()` view desde POST data
- Campos: `first_name`, `last_name`, `email`, `phone_number`, `course`, `experience`, `schedule`, `motivation`, UTM params, `recaptcha_token`

---

## Templates

```
templates/
├── _base.html                      → Base de todos los templates
├── index.html                      → Homepage
├── 404.html
├── courses/
│   ├── courses.html
│   ├── course_detail.html
│   ├── course_detail_district.html
│   └── course_detail_otros.html
├── instructors/
│   ├── instructors.html
│   └── instructors_detail.html
├── blog/
│   ├── post_list.html
│   └── post_detail.html
├── content_site/
│   ├── contact.html, faq.html, privacy_policies.html
│   ├── terms_conditions.html, thankyou.html
│   ├── invitated.html, invitated_success.html
├── casting/
│   ├── basic_info.html
│   ├── additional_info.html
│   └── thank_you.html
└── emails/
    ├── new_lead_notification.html
    ├── lead_confirmation.html
    ├── invitation_email.html
    ├── unsubscribe_confirm.html
    └── sequence/
        └── 00_immediate.html ... 08_day60.html
```

---

## Archivos Clave

| Propósito | Ruta |
|-----------|------|
| Settings principal | `webluxe/settings.py` |
| URLs raíz | `webluxe/urls.py` |
| Config Celery | `webluxe/celery.py` |
| Context processor | `webluxe/config/context_processors.py` |
| Variables de entorno | `webluxe/.env` |
| Tareas Celery | `leads/tasks.py` |
| Formularios casting | `leads/forms.py` |
| Comandos de gestión | `leads/management/commands/` |
| Template base | `templates/_base.html` |
| Static source | `static/` |
| Media uploads | `media/` |

---

## Variables de Entorno (.env en webluxe/)

```
SECRET_KEY=
DEBUG=True/False
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=5432
REDIS_URL=redis://127.0.0.1:6379/0
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL="Cuban Groove <info@cubangrooveperu.com>"
RECAPTCHA_SITE_KEY=
RECAPTCHA_SECRET_KEY=
OMNISEND_API_KEY=
```

---

## Comandos Frecuentes

```bash
# Servidor de desarrollo
python manage.py runserver
python manage.py runserver 0.0.0.0:8000

# Base de datos
python manage.py makemigrations <app_name>
python manage.py migrate
python manage.py showmigrations

# Leads y CRM
python manage.py import_leads
python manage.py import_leads_v2
python manage.py send_leads_to_omnisend

# Static files
python manage.py collectstatic --noinput
python manage.py collectstatic --clear

# Inspección
python manage.py shell
python manage.py check
python manage.py dbshell

# Celery (en terminales separadas)
celery -A webluxe worker --loglevel=info
celery -A webluxe beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

---

## Patrones de Desarrollo

### Agregar campo a modelo
1. `app/models.py` — agregar campo
2. `python manage.py makemigrations <app_name>`
3. `python manage.py migrate`
4. Actualizar `app/admin.py` si aplica
5. Actualizar templates si aplica

### Agregar nueva vista
1. `app/views.py` — crear vista (preferir CBV para páginas, funciones para AJAX)
2. `app/urls.py` — agregar URL pattern
3. Si es nueva app: registrar en `webluxe/urls.py`
4. `templates/<app>/nombre.html` — crear template

### Agregar email a la secuencia
1. Agregar nuevo template en `templates/emails/sequence/`
2. Actualizar `EMAIL_SEQUENCE_DELAYS` en `webluxe/settings.py`
3. Actualizar `schedule_email_sequence()` en `leads/tasks.py`
4. Nueva migración si se agrega `sequence_position` al modelo

### Agregar redirect legacy
- En `webluxe/urls.py`, agregar `re_path()` con `RedirectView` antes de los includes

---

## Notas Importantes

- **PostgreSQL obligatorio** — hardcoded en settings, no SQLite
- **Redis recomendado en producción** — sin Redis, Celery corre en modo eager (síncrono)
- **Todo el contenido en español** — labels, admin, mensajes de error
- **URL slugs son críticos** — usados para URLs canónicas y SEO
- **Sin tests** — no hay suite de tests en el proyecto
- **Cache invalidation**: al cambiar instructores/testimonios en admin, el cache (24h) puede servir datos viejos — limpiar con `python manage.py clear_cache` o esperar TTL
- **Allowed hosts en producción**: `cubangrooveperu.com`, `www.cubangrooveperu.com`, `104.248.113.83`
- **Logging**: bot_protection logs en `/var/log/cubangroove/bot_protection.log`
- **Apps deben estar en** `webluxe/settings.py` → `INSTALLED_APPS`
- **El formulario principal de lead** no usa forms.py — captura directa en la view `create_lead()`
