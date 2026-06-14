---
name: project-integrations-pattern
description: Patrón establecido para integraciones externas en webluxe — async Celery task + servicio en leads/services/
metadata:
  type: project
---

El proyecto tiene un patrón establecido para integraciones con APIs externas que debe respetarse en toda nueva integración.

**Patrón:** Celery `@shared_task` con `apply_async` desde la vista, servicio HTTP puro en `leads/services/<nombre>.py`.

**Evidencia en el codebase:**
- `leads/services/meta_capi.py` → integración Meta CAPI, llamada desde `send_capi_lead_event` en `tasks.py`
- `leads/management/commands/send_leads_to_omnisend.py` → integración Omnisend, solo via management command (patrón antiguo, no replicar)

**Campos de tracking en modelo Lead (patrón Omnisend):** `{integration}_synced_at`, `{integration}_last_status`, `{integration}_last_error`. Para Kommo se agrega también `kommo_contact_id` porque es necesario para updates posteriores.

**Reglas del patrón:**
1. Servicio en `leads/services/` — no importar modelos al nivel de módulo (solo dentro de funciones, para evitar circular imports con Celery)
2. Tarea Celery con `bind=True, max_retries=3, default_retry_delay=60`
3. En la vista: `task.apply_async(args=[lead.id])` — nunca sync
4. Detectar HTTP 401 y no reintentar (token inválido no se recupera solo)
5. `time.sleep(0.15)` en management commands de resync para respetar rate limits

**Por qué async y no sync en vista:** Kommo, Meta CAPI y Omnisend son servicios externos con latencia variable (200ms-3000ms) y disponibilidad < 100%. Una llamada sync en `create_lead()` crea dependencia de disponibilidad entre la captura de leads (función crítica) y el servicio externo.

**Integración Kommo pendiente de implementar (2026-06-07):** Ver SPEC 05 — `spec/05_integracion_kommo_crm.md`.

**How to apply:** Cuando se discuta cualquier integración nueva con API externa, recomendar este patrón desde el inicio y citar los archivos de referencia.
