# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**webluxe** is a Django 5.0 web application for a dance instruction business (Cuban Groove Peru). It manages courses, instructors, blog content, and lead generation with an integrated admin interface.

- Framework: Django 5.0.6 with PostgreSQL
- Language: Python 3
- Type: Multi-app Django project
- URL: cubangrooveperu.com

## Project Structure

### Core Apps

The project uses a modular app structure with 6 main Django apps:

- **courses**: Dance course management (models: Course)
  - Views: Class-based views for course listings, detail pages, and district-specific filtering
  - Features: SEO fields, course types (Virtual, Personalizada, Grupal, Coreografia), pricing
  
- **instructors**: Instructor profiles (models: Instructors)
  - Manages instructor bios, specialties, social media links
  - Integrated with courses via FK relationship
  
- **leads**: Lead capture and management (models: Lead, CastingRegistration)
  - Lead form handling with UTM tracking
  - Omnisend CRM integration with API sync
  - Management commands for lead imports and Omnisend syncing
  
- **blog**: Blog post management (models: Post)
  - Location-based posts (Miraflores, San Isidro, Surco, Lince, General)
  - RichTextField content with CKEditor
  
- **content_site**: Static content and testimonials (models: Testimony, Invitated, FAQ)
  - Cached instructor and testimony data in global context
  - File-based caching with 1-hour TTL
  
- **users**: Custom user model (models: CustomUser)
  - Extends Django's AbstractUser with age field
  - Used as AUTH_USER_MODEL

### Key Directories

- `templates/`: Django templates (base: _base.html)
- `static/`: CSS, Bootstrap icons, FontAwesome
- `media/`: User uploads (images/, videos/)
- `migrations/`: Database migrations in each app
- `leads/management/commands/`: Custom Django management commands

## Development Setup

### Prerequisites

- Python 3 with pip
- PostgreSQL database
- Virtual environment recommended

### Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Environment variables (.env file in webluxe/ directory):
   ```
   SECRET_KEY=<your-secret-key>
   DEBUG=True/False
   DB_NAME=<postgres-db-name>
   DB_USER=<postgres-user>
   DB_PASSWORD=<postgres-password>
   DB_HOST=localhost
   DB_PORT=5432
   EMAIL_BACKEND=<backend-class>
   EMAIL_HOST=<smtp-host>
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=<email>
   EMAIL_HOST_PASSWORD=<password>
   DEFAULT_FROM_EMAIL=<from-email>
   RECAPTCHA_SITE_KEY=<key>
   RECAPTCHA_SECRET_KEY=<key>
   OMNISEND_API_KEY=<key>
   ```

3. Database setup:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

4. Collect static files:
   ```bash
   python manage.py collectstatic
   ```

## Common Commands

### Development Server
```bash
python manage.py runserver
python manage.py runserver 0.0.0.0:8000
```

### Database Operations
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations
```

### Django Admin
```bash
python manage.py createsuperuser
python manage.py changepassword <username>
```

### Custom Management Commands
```bash
python manage.py import_leads
python manage.py import_leads_v2
python manage.py send_leads_to_omnisend
```

### Static Files
```bash
python manage.py collectstatic --noinput
python manage.py collectstatic --clear
```

### Inspection
```bash
python manage.py shell
python manage.py dbshell
python manage.py check
```

## Architecture Highlights

### Request Flow

1. URL routing in webluxe/urls.py handles legacy redirects first
2. Class-based views (TemplateView) in each app render templates
3. Global context processor provides: instructors, testimonies, reCAPTCHA key
4. Base template (templates/_base.html) extends to app-specific templates

### Caching

- File-based cache at /var/tmp/django_cache (1-hour TTL)
- UpdateCacheMiddleware and FetchFromCacheMiddleware enabled
- Global context processor caches instructors and testimonies

### Database Models

Key relationships:
- Course FK to Instructors
- Lead FK to Course (optional)
- Post FK to CustomUser
- All models include created_date and modified_date

### Forms & Validation

- CKEditor integration for rich text (courses, blog, FAQs)
- reCAPTCHA for lead forms
- Omnisend API integration for lead syncing

### SEO

- URL slugs for all content
- Meta fields on Course (seo_title, meta_description, keywords, h1, h2)
- Sitemap files available (blog, general, miraflores)

### Internationalization

- Language: Spanish (es)
- Timezone: America/Lima
- Locale: es_ES.UTF-8

## Common Patterns

### Adding Model Fields

1. Add field to app/models.py
2. Run: python manage.py makemigrations <app_name>
3. Run: python manage.py migrate
4. Register in app/admin.py

### Lead Management Workflow

- Forms create Lead or CastingRegistration records
- Raw values stored: form_course_raw, form_experience_raw, form_schedule_raw, form_motivation_raw
- Normalized keys stored: form_course_key, form_experience_key, form_schedule_key, form_motivation_key
- Sync to Omnisend: python manage.py send_leads_to_omnisend
- Track status: omnisend_synced_at, omnisend_last_status, omnisend_last_error

### Available Template Context

All templates receive via context processor:
- instructors: Active instructor objects
- list_testimony: Active testimony objects
- RECAPTCHA_SITE_KEY: For form validation

### URL Redirects

Legacy redirects configured in webluxe/urls.py using regex patterns with 301 permanent redirects. Examples:
- Old course paths → new paths
- Blog URLs → blog reorganized paths
- Slug normalization (underscores to hyphens)

## Important Notes

- Environment variables required in .env file
- PostgreSQL is required (hardcoded in settings)
- Media files stored in media/ directory (ensure write permissions)
- Spanish content throughout (labels, admin interface)
- URL slugs are critical for canonical URLs
- No tests detected (consider adding pytest coverage)
- Apps must be registered in webluxe/settings.py INSTALLED_APPS

## Key File Locations

- App routes: app/urls.py (register in webluxe/urls.py)
- Models: app/models.py
- Views: app/views.py (no separate forms.py files)
- Templates: templates/<app_name>/
- Settings: webluxe/settings.py (use environment variables)
- URL configuration: webluxe/urls.py
- Context processors: webluxe/config/context_processors.py
