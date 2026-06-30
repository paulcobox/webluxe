import logging
import re

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

GRAPH_API_VERSION = 'v25.0'


def _normalize_phone_for_wa(phone: str) -> str:
    """Elimina el + y espacios — Meta API espera solo dígitos: 51962345841."""
    return re.sub(r'[^\d]', '', phone)


def send_whatsapp_template(phone: str, first_name: str, curso: str) -> bool:
    """
    Envía la plantilla de WhatsApp al lead.
    Retorna True si fue exitoso, False si falla.
    """
    token       = settings.WHATSAPP_API_TOKEN
    number_id   = settings.WHATSAPP_PHONE_NUMBER_ID
    template    = settings.WHATSAPP_TEMPLATE_NAME

    if not token or not number_id or not template:
        logger.error('[WA] Faltan variables de entorno WHATSAPP_* — abortando envío.')
        return False

    phone_clean = _normalize_phone_for_wa(phone)
    if not phone_clean:
        logger.error('[WA] Teléfono vacío — abortando envío.')
        return False

    url = f'https://graph.facebook.com/{GRAPH_API_VERSION}/{number_id}/messages'

    payload = {
        'messaging_product': 'whatsapp',
        'to': phone_clean,
        'type': 'template',
        'template': {
            'name': template,
            'language': {'code': 'es'},
            'components': [
                {
                    'type': 'body',
                    'parameters': [
                        {'type': 'text', 'text': first_name or 'amigo/a'},
                    ],
                }
            ],
        },
    }

    try:
        resp = requests.post(
            url,
            headers={
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json',
            },
            json=payload,
            timeout=10,
        )

        if resp.status_code == 200:
            logger.info(f'[WA] Plantilla enviada a {phone_clean} | resp: {resp.text[:200]}')
            return True
        else:
            logger.error(f'[WA] Error HTTP {resp.status_code} enviando a {phone_clean}: {resp.text[:300]}')
            return False

    except requests.exceptions.ConnectionError as exc:
        logger.error(f'[WA] Error de conexión enviando a {phone_clean}: {exc}')
        return False
    except Exception as exc:
        logger.error(f'[WA] Error inesperado enviando a {phone_clean}: {exc}')
        return False


def has_kommo_conversation(deal_id: str) -> bool:
    """
    Verifica si el deal en Kommo tiene mensajes de WhatsApp (entrantes o salientes).
    Consulta las notas del deal buscando note_type=33 (mensajes WA en Kommo).
    Retorna True si hay conversación activa, False si no.
    """
    from leads.services.kommo_service import _get_headers, KOMMO_BASE_URL

    try:
        resp = requests.get(
            f'{KOMMO_BASE_URL}/leads/{deal_id}/notes',
            headers=_get_headers(),
            params={'limit': 50},
            timeout=10,
        )

        if resp.status_code == 204:
            return False

        if resp.status_code != 200:
            logger.warning(f'[WA] Error consultando notas del deal {deal_id}: HTTP {resp.status_code}')
            return False

        notes = resp.json().get('_embedded', {}).get('notes', [])
        for note in notes:
            # note_type 33 = mensaje de WhatsApp en Kommo
            if note.get('note_type') == 33:
                logger.info(f'[WA] Conversación WA encontrada en deal {deal_id}')
                return True

        return False

    except Exception as exc:
        logger.error(f'[WA] Error verificando conversación en deal {deal_id}: {exc}')
        return False
