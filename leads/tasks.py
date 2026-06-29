import logging
import secrets
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from celery import shared_task

logger = logging.getLogger(__name__)

SEQUENCE_TEMPLATES = {
    0: 'emails/sequence/00_immediate.html',
    1: 'emails/sequence/01_day1.html',
    2: 'emails/sequence/02_day3.html',
    3: 'emails/sequence/03_day7.html',
    4: 'emails/sequence/04_day14.html',
    5: 'emails/sequence/05_day21.html',
    6: 'emails/sequence/06_day30.html',
    7: 'emails/sequence/07_day45.html',
    8: 'emails/sequence/08_day60.html',
}

SEQUENCE_SUBJECTS = {
    0: '¡Bienvenido/a a Cuban Groove, {first_name}!',
    1: '{first_name},🌀 ¿Por qué tu baile no se ve natural? Aquí la razón!',
    2: '🌀 ¿Tu postura te está frenando al bailar? Descubre cómo mejorar hoy',
    3: '🌀 ¿Respiras bien cuando bailas? Esto podría estar afectando tu postura',
    4: '🌀 Domina el paso, la marcha cubana: peso, postura y ritmo.',
    5: '🌀 ¿Tus caderas no fluyen al bailar? Este truco lo cambia todo',
    6: '🌀 ¿Tus caderas se ven rígidas al bailar? Prueba esta técnica simple',
    7: '🌀 ¿Tu torso y tus caderas se mueven juntos? Esta técnica lo corrige',
    8: '🌀 ¿Tus brazos se ven rígidos al bailar? Estos 3 niveles lo cambian todo',
}

EMAIL_FROM = 'Cuban Groove <info@cubangrooveperu.com>'

EMAIL_CONTEXT_BASE = {
    'whatsapp_url': 'https://wa.me/51933275831',
    'instagram_url': 'https://www.instagram.com/cubangroove/',
    'facebook_url': 'https://www.facebook.com/cubangrooveperu',
    'tiktok_url': 'https://www.tiktok.com/@cubangrooveperu',
    'youtube_url': 'https://www.youtube.com/channel/UCaq2Wn80PzEnji0ccpuqtHA',
    'site_url': 'https://cubangrooveperu.com',
    'video_url': 'https://youtu.be/c4qIyVqGqOk',
    'video_thumbnail': 'https://img.youtube.com/vi/c4qIyVqGqOk/maxresdefault.jpg',
}


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_sequence_email(self, lead_id: int, sequence_position: int):
    from leads.models import Lead, EmailSequenceLog

    try:
        lead = Lead.objects.get(pk=lead_id)
    except Lead.DoesNotExist:
        logger.error(f'[EMAIL_SEQ] Lead {lead_id} not found. Aborting.')
        return

    if lead.unsubscribed:
        EmailSequenceLog.objects.filter(
            lead=lead,
            sequence_position=sequence_position
        ).update(status='SKIPPED')
        logger.info(f'[EMAIL_SEQ] Lead {lead_id} unsubscribed. Skipping pos {sequence_position}.')
        return

    log_entry, _ = EmailSequenceLog.objects.get_or_create(
        lead=lead,
        sequence_position=sequence_position,
        defaults={'status': 'PENDING', 'celery_task_id': self.request.id}
    )

    if log_entry.status == 'SENT':
        logger.info(f'[EMAIL_SEQ] Already sent pos {sequence_position} to lead {lead_id}. Skipping.')
        return

    template_name = SEQUENCE_TEMPLATES.get(sequence_position)
    if not template_name:
        logger.error(f'[EMAIL_SEQ] No template for position {sequence_position}.')
        return

    subject = SEQUENCE_SUBJECTS.get(sequence_position, 'Mensaje de Cuban Groove').format(
        first_name=lead.first_name
    )

    context = {
        **EMAIL_CONTEXT_BASE,
        'lead': lead,
        'first_name': lead.first_name,
        'last_name': lead.last_name,
        'email': lead.email,
        'course_of_interest': lead.course_of_interest.title if lead.course_of_interest else None,
        'unsubscribe_token': lead.unsubscribe_token,
        'sequence_position': sequence_position,
    }

    try:
        html_message = render_to_string(template_name, context)
        plain_message = strip_tags(html_message)

        send_mail(
            subject=subject,
            message=plain_message,
            from_email=EMAIL_FROM,
            recipient_list=[lead.email],
            html_message=html_message,
            fail_silently=False,
        )

        log_entry.status = 'SENT'
        log_entry.sent_at = timezone.now()
        log_entry.celery_task_id = self.request.id
        log_entry.save(update_fields=['status', 'sent_at', 'celery_task_id'])

        logger.info(f'[EMAIL_SEQ] Sent pos {sequence_position} to lead {lead_id} ({lead.email})')

    except Exception as exc:
        log_entry.status = 'FAILED'
        log_entry.error_message = str(exc)[:500]
        log_entry.save(update_fields=['status', 'error_message'])
        logger.error(f'[EMAIL_SEQ] FAILED pos {sequence_position} lead {lead_id}: {exc}')
        raise self.retry(exc=exc)


def schedule_email_sequence(lead):
    from leads.models import EmailSequenceLog

    if not lead.unsubscribe_token:
        lead.unsubscribe_token = secrets.token_urlsafe(32)
        lead.email_sequence_started_at = timezone.now()
        lead.save(update_fields=['unsubscribe_token', 'email_sequence_started_at'])

    delays = settings.EMAIL_SEQUENCE_DELAYS

    try:
        for position, delay_seconds in delays.items():
            task = send_sequence_email.apply_async(
                args=[lead.id, position],
                countdown=delay_seconds,
            )
            EmailSequenceLog.objects.get_or_create(
                lead=lead,
                sequence_position=position,
                defaults={
                    'status': 'PENDING',
                    'celery_task_id': task.id,
                }
            )
        logger.info(f'[EMAIL_SEQ] Scheduled 9-email sequence for lead {lead.id} ({lead.email})')
    except Exception as exc:
        # Si el broker (Redis) no está disponible, registramos el error pero
        # no rompemos la respuesta al usuario — el lead ya quedó guardado en BD.
        logger.error(f'[EMAIL_SEQ] No se pudo encolar secuencia para lead {lead.id}: {exc}')


@shared_task(bind=True, max_retries=2, default_retry_delay=30)
def send_capi_lead_event(self, lead_id, ip='', user_agent=''):
    from leads.models import Lead
    from leads.services.meta_capi import send_lead_event
    try:
        lead = Lead.objects.get(id=lead_id)
        if not lead.capi_sent:
            send_lead_event(lead, ip=ip, user_agent=user_agent)
    except Lead.DoesNotExist:
        logger.error(f'[CAPI] Lead {lead_id} no encontrado. Abortando.')
    except Exception as exc:
        logger.error(f'[CAPI] Error enviando evento para lead {lead_id}: {exc}')
        raise self.retry(exc=exc)


@shared_task
def kommo_fallback_sync(lead_id: int):
    """
    Corre 10 minutos después de crear el lead.
    - Si la persona ya escribió por WA (kommo_deal_id presente) → no enviar plantilla.
    - Si no escribió por WA → enviar plantilla WA para iniciar la conversación.
    """
    from leads.models import Lead
    from leads.services.whatsapp_service import send_whatsapp_template

    logger.warning(f'[KOMMO_FALLBACK] ▶ Iniciando | lead_id={lead_id}')

    try:
        lead = Lead.objects.get(pk=lead_id)
    except Lead.DoesNotExist:
        logger.error(f'[KOMMO_FALLBACK] ❌ Lead {lead_id} no encontrado en BD — abortando')
        return

    logger.warning(
        f'[KOMMO_FALLBACK] Lead {lead_id} | {lead.first_name} {lead.last_name} | '
        f'phone={lead.phone_number} | kommo_contact_id={lead.kommo_contact_id} | kommo_deal_id={lead.kommo_deal_id}'
    )

    phone = (lead.phone_number or '').strip()

    # Si ya tiene deal → la persona escribió por WA → Kommo lo procesó → no enviar plantilla
    if lead.kommo_deal_id:
        logger.warning(
            f'[KOMMO_FALLBACK] ✅ Persona ya escribió por WA | lead_id={lead_id} | '
            f'phone={phone} | deal_id={lead.kommo_deal_id} — no se envía plantilla'
        )
        return

    if not phone:
        logger.warning(f'[KOMMO_FALLBACK] ⚠️ Lead {lead_id} sin teléfono — abortando')
        return

    logger.warning(
        f'[KOMMO_FALLBACK] ⏳ Persona NO escribió por WA | lead_id={lead_id} | '
        f'phone={phone} — enviando plantilla WA'
    )

    curso = lead.form_course_raw or 'nuestros cursos'
    ok = send_whatsapp_template(phone=phone, first_name=lead.first_name, curso=curso)

    if ok:
        logger.warning(f'[KOMMO_FALLBACK] ✅ Plantilla WA enviada | lead_id={lead_id} | phone={phone}')
    else:
        logger.error(f'[KOMMO_FALLBACK] ❌ Error enviando plantilla WA | lead_id={lead_id} | phone={phone}')


@shared_task
def kommo_tag_no_response(lead_id: int):
    """
    Corre 3 días después de crear el lead.
    Si la persona nunca respondió WA ni la plantilla (kommo_deal_id sigue en None),
    agrega el tag 'Sin respuesta' al contacto en Kommo.
    """
    from leads.models import Lead
    from leads.services.kommo_service import add_tag_to_contact

    logger.warning(f'[KOMMO_TAG] ▶ Iniciando | lead_id={lead_id}')

    try:
        lead = Lead.objects.get(pk=lead_id)
    except Lead.DoesNotExist:
        logger.error(f'[KOMMO_TAG] ❌ Lead {lead_id} no encontrado en BD — abortando')
        return

    phone = (lead.phone_number or '').strip()

    logger.warning(
        f'[KOMMO_TAG] Lead {lead_id} | {lead.first_name} {lead.last_name} | '
        f'phone={phone} | kommo_contact_id={lead.kommo_contact_id} | kommo_deal_id={lead.kommo_deal_id}'
    )

    # Si tiene deal → persona respondió en algún momento → no marcar como sin respuesta
    if lead.kommo_deal_id:
        logger.warning(
            f'[KOMMO_TAG] ✅ Persona respondió WA | lead_id={lead_id} | phone={phone} | '
            f'deal_id={lead.kommo_deal_id} — no se agrega tag'
        )
        return

    # Sin contacto en Kommo → sync falló → no hay nada que taggear
    if not lead.kommo_contact_id:
        logger.warning(f'[KOMMO_TAG] ⚠️ Lead {lead_id} | phone={phone} | sin kommo_contact_id — no se puede agregar tag')
        return

    logger.warning(
        f'[KOMMO_TAG] 🏷 Persona nunca respondió | lead_id={lead_id} | phone={phone} | '
        f'contact_id={lead.kommo_contact_id} — agregando tag "Sin respuesta"'
    )

    ok = add_tag_to_contact(lead.kommo_contact_id, 'Sin respuesta')

    if ok:
        logger.warning(f'[KOMMO_TAG] ✅ Tag agregado | lead_id={lead_id} | phone={phone} | contact_id={lead.kommo_contact_id}')
    else:
        logger.error(f'[KOMMO_TAG] ❌ Error agregando tag | lead_id={lead_id} | phone={phone} | contact_id={lead.kommo_contact_id}')



@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def sync_lead_to_kommo(self, lead_id: int):
    """
    Crea o actualiza el contacto en Kommo CRM.
    Reintenta hasta 3 veces con delay de 60s salvo en errores 401.
    """
    from leads.models import Lead
    from leads.services.kommo_service import sync_contact_to_kommo

    logger.warning(f'[KOMMO_SYNC] ▶ Iniciando | lead_id={lead_id} | intento={self.request.retries + 1}/3')

    try:
        lead = Lead.objects.get(pk=lead_id)
    except Lead.DoesNotExist:
        logger.error(f'[KOMMO_SYNC] ❌ Lead {lead_id} no encontrado en BD — abortando')
        return

    phone = (lead.phone_number or '').strip()
    logger.warning(f'[KOMMO_SYNC] Lead {lead_id} | {lead.first_name} {lead.last_name} | phone={phone}')

    try:
        sync_contact_to_kommo(lead)
        lead.refresh_from_db()
        logger.warning(f'[KOMMO_SYNC] ✅ Completado | lead_id={lead_id} | phone={phone} | kommo_contact_id={lead.kommo_contact_id}')
    except Exception as exc:
        error_msg = str(exc)
        if '401' in error_msg:
            logger.error(f'[KOMMO_SYNC] ❌ 401 Unauthorized | lead_id={lead_id} | phone={phone} — no se reintentará')
            return
        logger.error(f'[KOMMO_SYNC] ❌ Error | lead_id={lead_id} | phone={phone} | {exc} — reintentando...')
        raise self.retry(exc=exc)