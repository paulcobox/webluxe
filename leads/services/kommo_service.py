import logging
import os
import re

import requests
from django.utils import timezone

logger = logging.getLogger(__name__)

KOMMO_BASE_URL = 'https://cubangroovepe.kommo.com/api/v4'

# Mapeo de valores del formulario a opciones configuradas en Kommo
EXPERIENCIA_MAP = {
    'Nunca he bailado':       'Nunca he bailado salsa',
    'Menos de 6 meses':       'Menos de 6 meses',
    'Entre 6 meses y 1 año':  '6 meses a 1 año',
    'Mas de 1 año':           'Más de 1 año',
    'Clases privadas':        'Prefiero clases privadas',
}

OBJETIVO_MAP = {
    'Aprender desde cero y ganar ritmo y confianza':                               'ritmo',
    'Bailar salsa en pareja — pasos, vueltas y conexión':                          'pareja',
    'Desarrollar mi estilo femenino — expresión, elegancia y movimiento corporal': 'femenino',
    'Entrenar con más técnica — coordinación, musicalidad y control':              'tecnico',
    'Timba Fusion y Reparto — flow urbano cubano':                                 'timba_fusion',
}

# IDs de campos personalizados en Kommo
FIELD_CURSO          = 2435160
FIELD_EXPERIENCIA    = 2430740
FIELD_OBJETIVO       = 2430750
FIELD_SEDE_HORARIO   = 2430754
FIELD_UTM_CAMPAIGN   = 2430760
FIELD_UTM_SOURCE     = 2430756
FIELD_UTM_CONTENT    = 2430758
FIELD_ORIGEN_LEAD    = 2430762
FIELD_RANGO_EDAD     = 2430792

KOMMO_PIPELINE_ID = 13762387
KOMMO_STATUS_ID   = 106182731  # Etapa: Lead nuevo


def _get_headers() -> dict:
    """Retorna los headers de autenticación. El token no se loggea nunca."""
    token = os.environ.get('KOMMO_TOKEN', '')
    return {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }


def normalize_phone(phone: str) -> str:
    """
    Limpia el teléfono y asegura prefijo +51 (Perú).
    Elimina espacios, guiones y paréntesis; si no empieza con +51, lo agrega.
    """
    cleaned = re.sub(r'[\s\-\(\)]', '', phone)
    if not cleaned.startswith('+51'):
        # Si empieza con 51 (sin +) lo dejamos como está con el +
        if cleaned.startswith('51'):
            cleaned = '+' + cleaned
        else:
            cleaned = '+51' + cleaned
    return cleaned


def _append_if_value(fields_list: list, field_id: int, value, field_code: str = None) -> None:
    """
    Agrega un campo a fields_list solo si value no es None ni string vacío.
    Usa field_code si está definido, si no usa field_id.
    """
    if value is None or value == '':
        return
    entry = {
        'values': [{'value': value}],
    }
    if field_code:
        entry['field_code'] = field_code
    else:
        entry['field_id'] = field_id
    fields_list.append(entry)


def build_basic_contact_payload(data: dict) -> list:
    """
    Construye el payload completo para POST /contacts.
    Incluye todos los campos disponibles al momento de creación del lead.
    Retorna [] si el teléfono está vacío (el caller debe abortar).
    """
    phone = (data.get('phone') or '').strip()
    if not phone:
        logger.warning('[KOMMO] Teléfono vacío — no se puede crear contacto.')
        return []

    full_name = (data.get('full_name') or '').strip()
    email     = (data.get('email') or '').strip()

    custom_fields = []

    custom_fields.append({
        'field_code': 'PHONE',
        'values': [{'value': normalize_phone(phone), 'enum_code': 'WORK'}],
    })

    if email:
        custom_fields.append({
            'field_code': 'EMAIL',
            'values': [{'value': email, 'enum_code': 'WORK'}],
        })

    _append_if_value(custom_fields, FIELD_CURSO,        data.get('curso'))
    _append_if_value(custom_fields, FIELD_SEDE_HORARIO, data.get('sede_horario'))

    experiencia_raw = data.get('experiencia') or ''
    _append_if_value(custom_fields, FIELD_EXPERIENCIA, EXPERIENCIA_MAP.get(experiencia_raw, experiencia_raw))

    objetivo_raw = data.get('objetivo') or ''
    _append_if_value(custom_fields, FIELD_OBJETIVO, OBJETIVO_MAP.get(objetivo_raw, objetivo_raw))

    _append_if_value(custom_fields, FIELD_UTM_CAMPAIGN, data.get('utm_campaign'))
    _append_if_value(custom_fields, FIELD_UTM_SOURCE,   data.get('utm_source'))
    _append_if_value(custom_fields, FIELD_UTM_CONTENT,  data.get('utm_content'))
    _append_if_value(custom_fields, FIELD_RANGO_EDAD,   data.get('rango_edad'))

    custom_fields.append({
        'field_id': FIELD_ORIGEN_LEAD,
        'values': [{'value': 'Landing Web'}],
    })

    return [{'name': full_name or phone, 'custom_fields_values': custom_fields}]


def build_update_contact_payload(data: dict) -> dict:
    """
    Construye el payload para PATCH /contacts/{id} con campos adicionales.
    Solo incluye campos que no estén vacíos o None.
    """
    custom_fields = []

    _append_if_value(custom_fields, FIELD_CURSO,        data.get('curso'))
    experiencia_raw = data.get('experiencia') or ''
    _append_if_value(custom_fields, FIELD_EXPERIENCIA,  EXPERIENCIA_MAP.get(experiencia_raw, experiencia_raw))
    objetivo_raw = data.get('objetivo') or ''
    _append_if_value(custom_fields, FIELD_OBJETIVO, OBJETIVO_MAP.get(objetivo_raw, objetivo_raw))
    _append_if_value(custom_fields, FIELD_SEDE_HORARIO, data.get('sede_horario'))
    _append_if_value(custom_fields, FIELD_UTM_CAMPAIGN, data.get('utm_campaign'))
    _append_if_value(custom_fields, FIELD_UTM_SOURCE,   data.get('utm_source'))
    _append_if_value(custom_fields, FIELD_UTM_CONTENT,  data.get('utm_content'))
    _append_if_value(custom_fields, FIELD_RANGO_EDAD,   data.get('rango_edad'))

    # Origen del Lead: siempre "Landing Web"
    custom_fields.append({
        'field_id': FIELD_ORIGEN_LEAD,
        'values': [{'value': 'Landing Web'}],
    })

    return {'custom_fields_values': custom_fields}


def _search_kommo_contacts(query: str, match_value: str, field_code: str) -> str | None:
    """
    Busca contactos en Kommo con el parámetro query y verifica coincidencia exacta
    en el campo indicado (PHONE o EMAIL) para evitar falsos positivos por búsqueda parcial.
    Retorna el ID del primer contacto que coincide exactamente, o None.
    """
    try:
        resp = requests.get(
            f'{KOMMO_BASE_URL}/contacts',
            headers=_get_headers(),
            params={'query': query, 'with': 'contacts'},
            timeout=10,
        )
        if resp.status_code == 204:
            return None
        if resp.status_code != 200:
            logger.warning(f'[KOMMO] search HTTP {resp.status_code} buscando {field_code}={query}')
            return None

        contacts = resp.json().get('_embedded', {}).get('contacts', [])
        for contact in contacts:
            for field in contact.get('custom_fields_values') or []:
                if field.get('field_code') != field_code:
                    continue
                for v in field.get('values') or []:
                    if v.get('value', '').strip() == match_value:
                        contact_id = str(contact['id'])
                        logger.warning(f'[KOMMO] Contacto existente encontrado por {field_code}: ID={contact_id}')
                        return contact_id
    except Exception as exc:
        logger.error(f'[KOMMO] Error buscando por {field_code}: {exc}')
    return None


def find_contact_by_phone(phone: str) -> str | None:
    """
    Busca contacto en Kommo por teléfono normalizado.
    Verifica coincidencia exacta en el campo PHONE para evitar falsos positivos.
    """
    if not phone:
        return None
    normalized = normalize_phone(phone)
    return _search_kommo_contacts(normalized, normalized, 'PHONE')


def find_contact_by_email(email: str) -> str | None:
    """
    Busca contacto en Kommo por email.
    Verifica coincidencia exacta en el campo EMAIL para evitar falsos positivos.
    """
    if not email:
        return None
    email = email.strip()
    return _search_kommo_contacts(email, email, 'EMAIL')


def create_kommo_contact(data: dict) -> str | None:
    """
    Crea un nuevo contacto en Kommo con los datos básicos.
    Retorna el contact_id (string) o None si falla.
    No reintenta en caso de 401 (token inválido).
    """
    payload = build_basic_contact_payload(data)
    if not payload:
        return None

    import json
    logger.warning(f'[KOMMO] POST create payload: {json.dumps(payload, ensure_ascii=False)}')

    try:
        resp = requests.post(
            f'{KOMMO_BASE_URL}/contacts',
            headers=_get_headers(),
            json=payload,
            timeout=10,
        )

        if resp.status_code == 401:
            logger.error('[KOMMO] 401 Unauthorized — verificar KOMMO_TOKEN en .env')
            return None

        if not (200 <= resp.status_code < 300):
            logger.error(f'[KOMMO] create_contact HTTP {resp.status_code}: {resp.text[:300]}')
            return None

        body = resp.json()
        embedded = body.get('_embedded', {})
        contacts = embedded.get('contacts', [])
        if contacts:
            contact_id = str(contacts[0]['id'])
            logger.info(f'[KOMMO] Contacto creado con ID={contact_id}')
            return contact_id

        logger.warning('[KOMMO] Contacto creado pero no se recibió ID en la respuesta.')
        return None

    except requests.exceptions.ConnectionError as exc:
        logger.error(f'[KOMMO] Error de conexión al crear contacto: {exc}')
        return None
    except Exception as exc:
        logger.error(f'[KOMMO] Error inesperado al crear contacto: {exc}')
        return None


def update_kommo_contact(contact_id: str, data: dict) -> bool:
    """
    Actualiza campos adicionales de un contacto existente en Kommo.
    Retorna True si fue exitoso, False si falla.
    """
    payload = build_update_contact_payload(data)
    if not payload.get('custom_fields_values'):
        logger.info(f'[KOMMO] Sin campos adicionales para actualizar en contacto {contact_id}.')
        return True

    import json
    logger.warning(f'[KOMMO] PATCH payload para contacto {contact_id}: {json.dumps(payload, ensure_ascii=False)}')

    try:
        resp = requests.patch(
            f'{KOMMO_BASE_URL}/contacts/{contact_id}',
            headers=_get_headers(),
            json=payload,
            timeout=10,
        )

        if resp.status_code == 401:
            logger.error('[KOMMO] 401 Unauthorized — verificar KOMMO_TOKEN en .env')
            return False

        if not (200 <= resp.status_code < 300):
            logger.error(f'[KOMMO] update_contact HTTP {resp.status_code}: {resp.text[:300]}')
            return False

        logger.info(f'[KOMMO] Contacto {contact_id} actualizado correctamente.')
        return True

    except requests.exceptions.ConnectionError as exc:
        logger.error(f'[KOMMO] Error de conexión al actualizar contacto {contact_id}: {exc}')
        return False
    except Exception as exc:
        logger.error(f'[KOMMO] Error inesperado al actualizar contacto {contact_id}: {exc}')
        return False


def create_kommo_deal(contact_id: str, deal_name: str) -> str | None:
    """
    Crea un deal en Kommo vinculado al contacto por su ID.
    No duplica datos del contacto — solo referencia el ID.
    Retorna el deal_id (string) o None si falla.
    """
    payload = [{
        'name':        deal_name,
        'pipeline_id': KOMMO_PIPELINE_ID,
        'status_id':   KOMMO_STATUS_ID,
        '_embedded': {
            'contacts': [{'id': int(contact_id)}],
        },
    }]

    try:
        resp = requests.post(
            f'{KOMMO_BASE_URL}/leads',
            headers=_get_headers(),
            json=payload,
            timeout=10,
        )

        if resp.status_code == 401:
            logger.error('[KOMMO] 401 Unauthorized al crear deal — verificar KOMMO_TOKEN')
            return None

        if not (200 <= resp.status_code < 300):
            logger.error(f'[KOMMO] create_deal HTTP {resp.status_code}: {resp.text[:300]}')
            return None

        leads = resp.json().get('_embedded', {}).get('leads', [])
        if leads:
            deal_id = str(leads[0]['id'])
            logger.info(f'[KOMMO] Deal creado con ID={deal_id} para contacto {contact_id}')
            return deal_id

        logger.warning('[KOMMO] Deal creado pero no se recibió ID en la respuesta.')
        return None

    except requests.exceptions.ConnectionError as exc:
        logger.error(f'[KOMMO] Error de conexión al crear deal: {exc}')
        return None
    except Exception as exc:
        logger.error(f'[KOMMO] Error inesperado al crear deal: {exc}')
        return None


def extract_phone_from_webhook_payload(post_data: dict) -> str | None:
    """
    Extrae el teléfono del payload form-encoded que envía Kommo en el webhook.
    Itera contacts[add][0][custom_fields][N] buscando code=PHONE.
    Retorna el teléfono normalizado o None.
    """
    i = 0
    while True:
        code_key = f'contacts[add][0][custom_fields][{i}][code]'
        if code_key not in post_data:
            break
        if post_data[code_key] == 'PHONE':
            value = post_data.get(f'contacts[add][0][custom_fields][{i}][values][0][value]', '')
            if value:
                return normalize_phone(value)
        i += 1
    return None


def get_contact_phone(contact_id: str) -> str | None:
    """
    Consulta un contacto en Kommo por su ID y retorna el teléfono (PHONE).
    Retorna None si no se encuentra o hay error.
    """
    try:
        resp = requests.get(
            f'{KOMMO_BASE_URL}/contacts/{contact_id}',
            headers=_get_headers(),
            timeout=10,
        )
        if resp.status_code != 200:
            logger.warning(f'[KOMMO] get_contact_phone HTTP {resp.status_code} para contact_id={contact_id}')
            return None

        data = resp.json()
        for field in data.get('custom_fields_values') or []:
            if field.get('field_code') == 'PHONE':
                values = field.get('values') or []
                if values:
                    return values[0].get('value')
    except Exception as exc:
        logger.error(f'[KOMMO] Error al obtener teléfono de contacto {contact_id}: {exc}')
    return None


def sync_contact_to_kommo(lead) -> None:
    """
    Sincroniza un Lead con Kommo CRM.

    - Contacto nuevo: POST con todos los campos disponibles (una sola llamada).
    - Contacto existente (encontrado por email o kommo_contact_id): PATCH con datos actuales.
    - El campo sede_horario llega en un PATCH posterior desde update_lead_sede.
    """
    phone = (lead.phone_number or '').strip()
    if not phone:
        logger.warning(f'[KOMMO] Lead {lead.id} sin teléfono — sync abortado.')
        return

    all_data = {
        'full_name':    f'{lead.first_name} {lead.last_name}'.strip(),
        'phone':        phone,
        'email':        lead.email or '',
        'curso':        lead.form_course_raw or '',
        'experiencia':  lead.form_experience_raw or '',
        'objetivo':     lead.form_motivation_raw or '',
        'sede_horario': lead.form_schedule_raw or '',
        'utm_campaign': lead.utm_campaign or '',
        'utm_source':   lead.utm_source or '',
        'utm_content':  lead.utm_content or '',
        'rango_edad':   lead.form_age_raw or '',
    }

    deal_name = f"{all_data['full_name'] or phone} — {all_data['curso'] or 'Consulta'}".strip(' —')

    try:
        contact_id = lead.kommo_contact_id

        if not contact_id:
            # Buscar por teléfono primero, luego por email
            contact_id = find_contact_by_phone(phone)
            if not contact_id and lead.email:
                contact_id = find_contact_by_email(lead.email)

            if contact_id:
                # Contacto existente encontrado: guardar ID y actualizar campos
                lead.kommo_contact_id = contact_id
                lead.save(update_fields=['kommo_contact_id'])
                update_kommo_contact(contact_id, all_data)
            else:
                # Contacto nuevo: POST con payload completo
                contact_id = create_kommo_contact(all_data)
                if not contact_id:
                    lead.kommo_last_error = 'No se pudo crear el contacto en Kommo.'
                    lead.save(update_fields=['kommo_last_error'])
                    return
                lead.kommo_contact_id = contact_id
                lead.save(update_fields=['kommo_contact_id'])
        else:
            # Ya tiene ID: actualizar con todos los datos actuales
            update_kommo_contact(contact_id, all_data)

        # Crear deal vinculado solo si aún no existe
        if not lead.kommo_deal_id:
            deal_id = create_kommo_deal(contact_id, deal_name)
            if deal_id:
                lead.kommo_deal_id = deal_id
                lead.save(update_fields=['kommo_deal_id'])

        lead.kommo_synced_at  = timezone.now()
        lead.kommo_last_error = None
        lead.save(update_fields=['kommo_synced_at', 'kommo_last_error'])

        logger.info(f'[KOMMO] Lead {lead.id} sincronizado. Contact ID={contact_id} | Deal ID={lead.kommo_deal_id}')

    except Exception as exc:
        error_msg = str(exc)[:500]
        logger.error(f'[KOMMO] Error inesperado sincronizando lead {lead.id}: {exc}')
        lead.kommo_last_error = error_msg
        lead.save(update_fields=['kommo_last_error'])
