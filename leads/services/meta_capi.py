import hashlib
import logging
import re
import time

import requests
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)


def _sha256(value: str) -> str:
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


def _normalize_phone(phone: str) -> str:
    digits = re.sub(r'\D', '', phone)
    if not digits.startswith('51'):
        digits = '51' + digits
    return digits


def send_lead_event(lead, ip='', user_agent=''):
    pixel_id = getattr(settings, 'META_PIXEL_ID', '')
    token    = getattr(settings, 'META_CAPI_TOKEN', '')

    if not pixel_id or not token:
        logger.warning('[CAPI] META_PIXEL_ID o META_CAPI_TOKEN no configurados. Evento omitido.')
        return

    user_data = {
        'client_ip_address': ip,
        'client_user_agent': user_agent,
    }
    if lead.email:
        user_data['em'] = [_sha256(lead.email.strip().lower())]
    if lead.phone_number:
        user_data['ph'] = [_sha256(_normalize_phone(lead.phone_number))]
    if lead.first_name:
        user_data['fn'] = [_sha256(lead.first_name.strip().lower())]
    if lead.last_name:
        user_data['ln'] = [_sha256(lead.last_name.strip().lower())]

    # age_range: parsear de notes ("Edad: 25-34\n...")
    age_range = ''
    if lead.notes:
        m = re.search(r'Edad:\s*(.+)', lead.notes)
        if m:
            age_range = m.group(1).strip()

    lead_value = 150 if 'Privada' in (lead.form_course_raw or '') else 170
    custom_data = {
        'content_name': lead.form_course_raw or '',
        'content_category': lead.form_motivation_raw or '',
        'experience_level': lead.form_experience_raw or '',
        'value': lead_value,
        'currency': 'PEN',
    }
    if age_range:
        custom_data['age_range'] = age_range

    payload = {
        'data': [{
            'event_name': 'Lead',
            'event_time': int(time.time()),
            'event_id': lead.meta_event_id or str(lead.id),
            'action_source': 'website',
            'user_data': user_data,
            'custom_data': custom_data,
        }]
    }

    url    = f'https://graph.facebook.com/v23.0/{pixel_id}/events'
    params = {'access_token': token}

    try:
        resp = requests.post(url, json=payload, params=params, timeout=10)
        lead.capi_sent     = resp.status_code == 200
        lead.capi_sent_at  = timezone.now()
        lead.capi_response = resp.text[:500]
        logger.info(f'[CAPI] Lead {lead.id} → HTTP {resp.status_code}: {resp.text[:200]}')
    except Exception as e:
        lead.capi_sent     = False
        lead.capi_response = str(e)[:500]
        logger.error(f'[CAPI] Lead {lead.id} → error de red: {e}')

    lead.save(update_fields=['capi_sent', 'capi_sent_at', 'capi_response'])
