# SPEC 05 — Integración Kommo CRM: Análisis Arquitectónico y Plan Mejorado

**Proyecto:** webluxe — Cuban Groove Peru
**Fecha:** 2026-06-07
**Agente:** architect
**Estado:** Pendiente implementación

---

## Diagnóstico del Plan Original

El plan propuesto funciona, pero tiene varios puntos débiles que conviene corregir antes de implementar. El análisis detallado de cada punto sigue abajo. La conclusión de alto nivel es: **la arquitectura correcta es async vía Celery, no sync en la vista**, y el modelo de datos necesita un campo adicional que el plan ya identifica correctamente (`kommo_contact_id`).

---

## Análisis Punto a Punto

### 1. Riesgo de latencia en la vista

**Diagnóstico:** El plan propone llamar `sync_contact_to_kommo(lead_instance)` directamente dentro de `create_lead()`, después de guardar el lead. Esto significa que el usuario espera la respuesta HTTP hasta que Kommo responda (o falle con timeout).

**Contexto actual del proyecto:**
- El email al admin usa `threading.Thread` — reconoce el problema de latencia.
- Meta CAPI usa `send_capi_lead_event.apply_async()` — patrón Celery correcto.
- `schedule_email_sequence()` usa `apply_async` con countdowns.

La vista ya tiene dos patrones distintos de async: threading (para email admin, patrón antiguo) y Celery tasks (para CAPI y secuencia de emails, patrón moderno). Agregar Kommo sync rompe la coherencia y añade latencia real.

**Datos concretos del impacto:** Una request HTTP a Kommo con `timeout=10` puede tardar entre 200ms y 3000ms en condiciones normales desde Lima (Kommo corre en AWS, sus servidores están en Europa o EEUU). Si Kommo tiene un pico de latencia, el usuario del formulario percibe el formulario "colgado" durante varios segundos. Si Kommo está caído, la vista espera hasta el timeout antes de responder.

**Recomendación:** Usar `sync_lead_to_kommo.apply_async(args=[lead.id])` exactamente igual que Meta CAPI. La vista responde en <100ms independiente del estado de Kommo.

---

### 2. Estructura del servicio: `leads/services/kommo_service.py`

**Diagnóstico:** El directorio `leads/services/` ya existe (contiene `meta_capi.py`). La decisión de ponerlo ahí es correcta y consistente con el patrón establecido.

**Evaluación del patrón actual:** `meta_capi.py` es un módulo de servicio puro que:
- No importa modelos en el nivel de módulo (los importa dentro de funciones para evitar circular imports con Celery)
- Recibe la instancia del lead como argumento
- Hace el request HTTP y actualiza el lead
- Registra logs con prefijo de contexto (`[CAPI]`)

El nuevo `kommo_service.py` debe seguir exactamente el mismo patrón. La diferencia clave es que Kommo tiene un flujo de dos llamadas (crear + actualizar), mientras que CAPI es una sola llamada.

**Un detalle que el plan no menciona:** `meta_capi.py` importa modelos dentro de la función `send_lead_event()`, no al inicio del archivo. Esto es intencional para evitar importación circular cuando Celery arranca. `kommo_service.py` debe hacer lo mismo.

---

### 3. Manejo de reintentos

**Diagnóstico:** El plan menciona "capturar errores HTTP y de conexión" pero no especifica un mecanismo de reintento estructurado. Omnisend tampoco tiene reintentos automáticos en el proyecto (el management command simplemente falla y registra).

**El patrón correcto para este proyecto** es el mismo que `send_capi_lead_event`:

```python
@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def sync_lead_to_kommo(self, lead_id):
    ...
    except Exception as exc:
        raise self.retry(exc=exc)
```

Con 3 reintentos y 60 segundos de delay, si Kommo tiene un downtime transitorio de <3 minutos, el contacto eventualmente se sincroniza sin intervención manual.

**Caso especial:** Si los 3 reintentos fallan (Kommo caído por horas), el lead queda en BD con `kommo_contact_id=None` y `kommo_last_error` con el mensaje. El management command de resync (ver más abajo) puede recuperarlos.

---

### 4. Campo `kommo_contact_id`: modelo Lead vs. tabla separada

**Diagnóstico:** El plan propone agregar `kommo_contact_id` directamente al modelo Lead, igual que `omnisend_synced_at`, `omnisend_last_status`, `omnisend_last_error` ya están en el modelo Lead.

**Trade-off:**

| Opción | Pros | Contras |
|--------|------|---------|
| Campos en Lead (propuesta) | Simple, consistente con Omnisend, sin JOIN | El modelo Lead crece; si se agregan más CRMs hay contaminación |
| Tabla `LeadIntegration` separada | Limpio, extensible, un registro por integración | Dos queries en vez de uno; más complejidad para un CRUD simple |

**Recomendación para este proyecto:** Campos en Lead, por las siguientes razones:
1. El proyecto ya estableció este patrón con Omnisend (3 campos). Ser consistente tiene valor.
2. No hay evidencia de que se vayan a agregar 5+ CRMs más. Si eso cambia en el futuro, una migración de reestructuración es manejable.
3. El equipo es pequeño y sin tests — introducir una tabla de join para un caso de uso simple añade carga cognitiva sin beneficio real hoy.

**Campos a agregar:**
```python
kommo_contact_id = models.CharField(max_length=50, blank=True, null=True, db_index=True)
kommo_synced_at  = models.DateTimeField(null=True, blank=True)
kommo_last_error = models.TextField(null=True, blank=True)
```

Nota: `db_index=True` en `kommo_contact_id` porque el management command de resync (y la tarea de update) necesita hacer lookups por este campo frecuentemente.

---

### 5. Campo "Rango de edad" (field_id: 2430792)

**Diagnóstico:** El modelo Lead tiene `form_age_raw` (CharField, ya existe — visible en `models.py` línea 22 y en `views.py` línea 125). Este campo captura el rango de edad desde el wizard del formulario de la landing.

**Hallazgo importante:** El campo existe en el modelo y en la vista. El plan no lo menciona explícitamente como fuente, pero `form_age_raw` es el dato correcto para mapear a `field_id: 2430792` en Kommo.

El valor viene del wizard de 6 pasos de la landing Meta Ads (SPEC 04). Los valores posibles son rangos como "18-24", "25-34", "35-44", etc. Se envían directamente como string.

**Acción:** En `build_update_contact_payload()`, usar `lead.form_age_raw` para el campo `2430792`. Si está vacío, no incluir el campo (regla del plan: no enviar campos vacíos).

---

### 6. Seguridad del token KOMMO_TOKEN

**Diagnóstico:** El plan lee el token desde `.env` vía `os.getenv('KOMMO_TOKEN')`. Esto es correcto. Las consideraciones adicionales son:

1. **No logear el token.** El plan lo menciona pero conviene ser explícito: nunca hacer `logger.debug(f"Headers: {headers}")` porque el `Authorization: Bearer {token}` estaría en los headers.

2. **El token de Kommo es un Long-Lived Token (OAuth2).** No tiene expiración automática corta (a diferencia de Meta CAPI que sí puede expirar). Sin embargo, si el token se revoca en el panel de Kommo, todas las requests fallarán con 401. El sistema debe detectar esto:
   - Log con nivel `ERROR` cuando `response.status_code == 401`
   - Mensaje explícito: `"[KOMMO] 401 Unauthorized — verificar KOMMO_TOKEN en .env"`
   - No reintentar en caso de 401 (el reintento no va a funcionar — el token está inválido)

3. **El token no debe aparecer en logs de Django ni en Sentry** si se integra en el futuro. Usar un wrapper de logging que filtre el header `Authorization`.

**Implementación del punto 2 en la tarea Celery:**

```python
if resp.status_code == 401:
    logger.error('[KOMMO] 401 Unauthorized — KOMMO_TOKEN inválido o revocado')
    return  # No reintentar
```

---

### 7. Idempotencia

**Diagnóstico:** El plan menciona "Si ya tiene `kommo_contact_id`: no crear, solo actualizar." Esto es idempotencia a nivel de negocio, pero hay un race condition no contemplado.

**Escenario problemático:**
1. Tarea Celery se ejecuta, hace `POST /contacts`, Kommo crea el contacto y devuelve `id=12345`.
2. Antes de que la tarea pueda guardar `kommo_contact_id=12345` en BD, la tarea es terminada por Celery (timeout, reinicio de worker, OOM).
3. La tarea se reintenta. Como `kommo_contact_id` es `None` en BD, crea otro contacto en Kommo. Ahora hay dos contactos duplicados.

**Solución:** La llamada `POST /contacts` en Kommo acepta un campo `custom_fields_values` con el email. Si el contacto ya existe por email, Kommo devuelve el ID existente (comportamiento de upsert). Verificar esto en la documentación de Kommo API v4 — si soporta búsqueda por email antes de crear, el flujo correcto es:

```
1. GET /contacts?query=email@ejemplo.com
2. Si existe: usar el ID retornado
3. Si no existe: POST /contacts para crear
```

Esta secuencia es idempotente porque el GET antes del POST previene duplicados. Es más costosa en requests (2 en vez de 1 en el camino feliz) pero elimina el race condition.

**Alternativa más simple:** Usar el campo `external_id` de Kommo (si está disponible en la API v4) para pasar el `lead.id` de Django como identificador externo. Esto permite que Kommo maneje la idempotencia nativamente.

---

### 8. Rate Limits de Kommo API

**Diagnóstico:** La API de Kommo tiene límites de rate. Según su documentación oficial:
- 7 requests por segundo por cuenta (límite estricto)
- Responde con HTTP 429 cuando se excede

**Para este proyecto en producción:** Con el volumen actual (pocos leads por día), el rate limit no es un problema en el flujo normal de creación de leads. El riesgo real es el **management command de resync** si procesa muchos leads históricos sin throttling.

**Recomendaciones:**
1. En el servicio: detectar HTTP 429 y hacer `raise self.retry(countdown=5)` — esperar 5 segundos antes de reintentar.
2. En el management command de resync: agregar `time.sleep(0.15)` entre requests (igual que `send_leads_to_omnisend.py`).
3. No agregar throttling complejo (token bucket, etc.) — el volumen no lo justifica.

---

## Riesgos Arquitecturales No Contemplados

### Riesgo A: La tarea de "create + update" como dos requests separadas puede fallar a mitad
El flujo propuesto es: crear contacto (POST) → guardar ID → actualizar con campos adicionales (PATCH). Si la tarea falla entre el POST y el PATCH, el contacto existe en Kommo con datos básicos pero sin los campos adicionales. En el siguiente reintento, la tarea debería detectar que `kommo_contact_id` ya existe y solo hacer el PATCH.

**Mitigación:** Diseñar `sync_lead_to_kommo` para que sea re-entrant:
- Si `lead.kommo_contact_id` está vacío → POST + guardar ID → PATCH
- Si `lead.kommo_contact_id` está presente → solo PATCH

Esto hace que cada reintento solo ejecute la parte que aún no completó.

### Riesgo B: Kommo no está disponible durante el onboarding del primer lead del día
El primer lead de la mañana puede encontrar Kommo con mantenimiento programado. Con async+reintentos, el lead se guarda en BD, el usuario recibe respuesta exitosa, y Kommo se sincroniza cuando vuelva a estar disponible.

Sin async, el primer lead del día podría recibir una respuesta de error o timeout si la vista no maneja correctamente el fallo de Kommo.

### Riesgo C: Falta de management command para resync
El proyecto tiene `send_leads_to_omnisend.py` para sincronizar leads históricos con Omnisend. No habrá un equivalente para Kommo a menos que se cree desde el inicio. Los leads que fallen todos los reintentos quedan "perdidos" sin una herramienta de recuperación.

**Mitigación:** Crear `sync_leads_to_kommo.py` como management command con filtro por `kommo_contact_id__isnull=True` y `--limit` para procesamiento por lotes.

---

## Arquitectura Final Recomendada

```
create_lead() view
    │
    ├── [sync] guardar Lead en BD
    ├── [thread] send_async_email (notif admin)  — patrón legacy, mantener
    ├── [async] schedule_email_sequence(lead)    — patrón Celery, correcto
    ├── [async] send_capi_lead_event.apply_async — patrón Celery, correcto
    └── [async] sync_lead_to_kommo.apply_async   ← NUEVO, mismo patrón
```

La vista responde `JsonResponse({'success': True, 'lead_id': lead.id})` en <100ms.
Kommo se sincroniza en background, con hasta 3 reintentos.

---

## Archivos a Tocar

| Archivo | Acción | Descripción |
|---------|--------|-------------|
| `leads/models.py` | Modificar | Agregar 3 campos Kommo al modelo Lead |
| `leads/migrations/00XX_add_kommo_fields.py` | Crear | `makemigrations leads` |
| `leads/services/kommo_service.py` | Crear | Servicio HTTP con normalize, build payloads, create, update |
| `leads/tasks.py` | Modificar | Agregar `sync_lead_to_kommo` como shared_task |
| `leads/views.py` | Modificar | Agregar `apply_async` de la tarea después de guardar lead |
| `webluxe/.env` | Modificar | Agregar `KOMMO_TOKEN=` |
| `leads/management/commands/sync_leads_to_kommo.py` | Crear | Management command para resync de leads históricos |

---

## Código del Servicio (versión mejorada)

### `leads/services/kommo_service.py`

```python
import logging
import re

import requests
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)

KOMMO_BASE_URL = 'https://cubangroovepe.kommo.com/api/v4'

KOMMO_FIELD_IDS = {
    'curso_recomendado': 2430742,
    'experiencia':       2430740,
    'objetivo':          2430750,
    'sede_horario':      2430754,
    'utm_campaign':      2430760,
    'utm_source':        2430756,
    'utm_content':       2430758,
    'origen_lead':       2430762,
    'rango_edad':        2430792,
}


def _get_headers():
    """Devuelve headers de autenticación. No loguear el retorno."""
    token = getattr(settings, 'KOMMO_TOKEN', '')
    return {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }


def normalize_phone(phone: str) -> str:
    """Normaliza teléfono peruano al formato +51XXXXXXXXX."""
    digits = re.sub(r'\D', '', phone)
    if not digits.startswith('51'):
        digits = '51' + digits
    return '+' + digits


def _append_if_value(fields_list: list, field_id: int, value):
    """Solo agrega un campo custom si tiene valor no vacío."""
    if value:
        fields_list.append({'field_id': field_id, 'values': [{'value': str(value)}]})


def build_basic_contact_payload(lead) -> list:
    """Payload para POST /contacts (creación inicial)."""
    name = f"{lead.first_name} {lead.last_name}".strip()

    custom_fields = [
        {'field_id': KOMMO_FIELD_IDS['origen_lead'], 'values': [{'value': 'Landing Web'}]},
    ]

    payload = {
        'name': name,
        'custom_fields_values': custom_fields,
    }

    # PHONE y EMAIL usan field_code, no field_id
    if lead.phone_number:
        phone_e164 = normalize_phone(lead.phone_number)
        payload.setdefault('custom_fields_values', []).append({
            'field_code': 'PHONE',
            'values': [{'value': phone_e164, 'enum_code': 'WORK'}],
        })

    if lead.email:
        payload['custom_fields_values'].append({
            'field_code': 'EMAIL',
            'values': [{'value': lead.email, 'enum_code': 'WORK'}],
        })

    return [payload]


def build_update_contact_payload(lead) -> dict:
    """Payload para PATCH /contacts/{id} (enriquecimiento de datos)."""
    custom_fields = []

    _append_if_value(custom_fields, KOMMO_FIELD_IDS['curso_recomendado'], lead.form_course_raw)
    _append_if_value(custom_fields, KOMMO_FIELD_IDS['experiencia'],       lead.form_experience_raw)
    _append_if_value(custom_fields, KOMMO_FIELD_IDS['objetivo'],          lead.form_motivation_raw)
    _append_if_value(custom_fields, KOMMO_FIELD_IDS['sede_horario'],      lead.form_schedule_raw)
    _append_if_value(custom_fields, KOMMO_FIELD_IDS['utm_campaign'],      lead.utm_campaign)
    _append_if_value(custom_fields, KOMMO_FIELD_IDS['utm_source'],        lead.utm_source)
    _append_if_value(custom_fields, KOMMO_FIELD_IDS['utm_content'],       lead.utm_content)
    _append_if_value(custom_fields, KOMMO_FIELD_IDS['origen_lead'],       'Landing Web')
    _append_if_value(custom_fields, KOMMO_FIELD_IDS['rango_edad'],        lead.form_age_raw)

    return {'custom_fields_values': custom_fields}


def find_contact_by_email(email: str) -> str | None:
    """
    Busca un contacto en Kommo por email.
    Retorna el contact_id como string, o None si no existe.
    Previene duplicados en caso de reintento.
    """
    if not email:
        return None
    try:
        resp = requests.get(
            f'{KOMMO_BASE_URL}/contacts',
            headers=_get_headers(),
            params={'query': email},
            timeout=10,
        )
        if resp.status_code == 200:
            data = resp.json()
            contacts = data.get('_embedded', {}).get('contacts', [])
            if contacts:
                return str(contacts[0]['id'])
    except Exception as e:
        logger.warning(f'[KOMMO] No se pudo buscar contacto por email: {e}')
    return None


def create_kommo_contact(lead) -> str | None:
    """
    Crea contacto en Kommo. Retorna el contact_id como string.
    Si el teléfono está vacío, no intenta crear (requerimiento del plan).
    """
    if not lead.phone_number:
        logger.warning(f'[KOMMO] Lead {lead.id} sin teléfono — omitiendo creación en Kommo')
        return None

    # Búsqueda previa para garantizar idempotencia
    if lead.email:
        existing_id = find_contact_by_email(lead.email)
        if existing_id:
            logger.info(f'[KOMMO] Lead {lead.id} ya tiene contacto en Kommo ID={existing_id} (encontrado por email)')
            return existing_id

    payload = build_basic_contact_payload(lead)
    try:
        resp = requests.post(
            f'{KOMMO_BASE_URL}/contacts',
            json=payload,
            headers=_get_headers(),
            timeout=10,
        )
    except requests.exceptions.RequestException as e:
        logger.error(f'[KOMMO] Error de red al crear contacto para lead {lead.id}: {e}')
        raise

    if resp.status_code == 401:
        logger.error('[KOMMO] 401 Unauthorized — verificar KOMMO_TOKEN en .env')
        return None  # No reintentar — el token está inválido

    if not (200 <= resp.status_code < 300):
        logger.error(f'[KOMMO] Error {resp.status_code} al crear contacto lead {lead.id}: {resp.text[:300]}')
        raise Exception(f'Kommo POST /contacts HTTP {resp.status_code}')

    data = resp.json()
    contacts = data.get('_embedded', {}).get('contacts', [])
    if not contacts:
        logger.error(f'[KOMMO] Respuesta sin contactos para lead {lead.id}: {resp.text[:300]}')
        raise Exception('Kommo no devolvió contacto creado')

    contact_id = str(contacts[0]['id'])
    logger.info(f'[KOMMO] Contacto creado para lead {lead.id} → Kommo ID={contact_id}')
    return contact_id


def update_kommo_contact(contact_id: str, lead) -> bool:
    """
    Actualiza contacto existente con datos adicionales del wizard.
    Retorna True si fue exitoso.
    """
    payload = build_update_contact_payload(lead)
    if not payload.get('custom_fields_values'):
        logger.info(f'[KOMMO] Sin campos adicionales para actualizar — lead {lead.id}')
        return True

    try:
        resp = requests.patch(
            f'{KOMMO_BASE_URL}/contacts/{contact_id}',
            json=payload,
            headers=_get_headers(),
            timeout=10,
        )
    except requests.exceptions.RequestException as e:
        logger.error(f'[KOMMO] Error de red al actualizar contacto {contact_id} lead {lead.id}: {e}')
        raise

    if resp.status_code == 401:
        logger.error('[KOMMO] 401 Unauthorized — verificar KOMMO_TOKEN en .env')
        return False

    if not (200 <= resp.status_code < 300):
        logger.error(f'[KOMMO] Error {resp.status_code} al actualizar contacto {contact_id}: {resp.text[:300]}')
        raise Exception(f'Kommo PATCH /contacts/{contact_id} HTTP {resp.status_code}')

    logger.info(f'[KOMMO] Contacto {contact_id} actualizado para lead {lead.id}')
    return True
```

---

## Código de la Tarea Celery

### Agregar a `leads/tasks.py`

```python
@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def sync_lead_to_kommo(self, lead_id: int):
    """
    Sincroniza un lead con Kommo CRM.
    - Si no tiene kommo_contact_id: crea el contacto y guarda el ID.
    - Siempre actualiza los campos adicionales con PATCH.
    Re-entrant: si ya tiene kommo_contact_id, solo hace el PATCH.
    """
    from leads.models import Lead
    from leads.services.kommo_service import create_kommo_contact, update_kommo_contact

    try:
        lead = Lead.objects.get(pk=lead_id)
    except Lead.DoesNotExist:
        logger.error(f'[KOMMO] Lead {lead_id} no encontrado. Abortando.')
        return

    try:
        # Paso 1: Crear si no tiene ID
        if not lead.kommo_contact_id:
            contact_id = create_kommo_contact(lead)
            if not contact_id:
                # Sin teléfono o token inválido — no reintentar
                return
            lead.kommo_contact_id = contact_id
            lead.kommo_synced_at = timezone.now()
            lead.kommo_last_error = None
            lead.save(update_fields=['kommo_contact_id', 'kommo_synced_at', 'kommo_last_error'])

        # Paso 2: Actualizar campos adicionales (siempre)
        update_kommo_contact(lead.kommo_contact_id, lead)
        lead.kommo_synced_at = timezone.now()
        lead.kommo_last_error = None
        lead.save(update_fields=['kommo_synced_at', 'kommo_last_error'])

    except Exception as exc:
        lead.kommo_last_error = str(exc)[:500]
        lead.save(update_fields=['kommo_last_error'])
        logger.error(f'[KOMMO] Error sincronizando lead {lead_id}: {exc}')
        raise self.retry(exc=exc)
```

---

## Cambios en la Vista

### `leads/views.py` — importar y agregar llamada

Agregar a los imports:
```python
from .tasks import schedule_email_sequence, send_capi_lead_event, sync_lead_to_kommo
```

Después del bloque de Meta CAPI (paso 9), agregar paso 10:
```python
# ===============================================
# 🔟 Sincronizar con Kommo CRM
# ===============================================
sync_lead_to_kommo.apply_async(args=[lead.id])
```

---

## Migración del Modelo

Después de agregar los campos a `Lead`, ejecutar:
```bash
python manage.py makemigrations leads --name add_kommo_fields
python manage.py migrate
```

Los tres campos a agregar en `leads/models.py`, junto al bloque de Omnisend:
```python
# --- Kommo CRM ---
kommo_contact_id = models.CharField(max_length=50, blank=True, null=True, db_index=True)
kommo_synced_at  = models.DateTimeField(null=True, blank=True)
kommo_last_error = models.TextField(null=True, blank=True)
```

---

## Management Command para Resync

### `leads/management/commands/sync_leads_to_kommo.py`

Seguir el mismo patrón de `send_leads_to_omnisend.py`:
- Filtrar `kommo_contact_id__isnull=True`
- Flag `--limit` para procesamiento por lotes
- Flag `--dry_run` para previsualizar
- `time.sleep(0.15)` entre requests para respetar rate limit
- Registrar OK/FAIL al final

---

## Cómo Probar Localmente

### Sin Redis (modo eager)
Con `CELERY_TASK_ALWAYS_EAGER = True`, las tareas se ejecutan sincronamente:
```bash
python manage.py shell
```
```python
from leads.models import Lead
from leads.tasks import sync_lead_to_kommo
lead = Lead.objects.latest('created_date')
sync_lead_to_kommo(lead.id)  # ejecuta sincrono en eager mode
lead.refresh_from_db()
print(lead.kommo_contact_id)  # debe tener un ID
```

### Con un lead real en prod
```bash
python manage.py sync_leads_to_kommo --limit 1 --dry_run
python manage.py sync_leads_to_kommo --limit 1
```

---

## Tabla de Riesgos Priorizados

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|-------------|---------|------------|
| Kommo caído al crear lead | Media | Alto (sin mitigación sync) | Async + reintentos resuelven completamente |
| Token inválido/expirado | Baja | Alto | Log explícito 401, no reintentar |
| Duplicados en Kommo por retry | Media | Medio | `find_contact_by_email` antes de POST |
| Rate limit 429 | Muy baja (vol. actual) | Bajo | `raise self.retry(countdown=5)` en 429 |
| Leads sin teléfono no se sincronizan | Media | Bajo | Expected behavior, loggeado como warning |
| form_age_raw vacío | Alta (leads sin wizard) | Muy bajo | `_append_if_value` descarta campo vacío |

---

## Recomendación Final

**Arquitectura: async vía Celery task, no sync en la vista.**

La razón no es puramente de rendimiento — es de resiliencia. Una llamada sync a Kommo en la vista crea una dependencia de disponibilidad entre la función crítica de captura de leads y un servicio externo sobre el que no se tiene control. Kommo puede estar caído durante 10 minutos por mantenimiento. Con sync, se pierden leads durante esos 10 minutos (o se muestran errores al usuario). Con async + reintentos, se capturan todos los leads y Kommo se pone al día automáticamente.

El proyecto ya tomó esta decisión correctamente con Meta CAPI. Kommo debe seguir el mismo camino.
