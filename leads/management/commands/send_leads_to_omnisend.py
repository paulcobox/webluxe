import time
import requests
from datetime import datetime

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Q
from django.utils.timezone import make_aware, now


from leads.models import Lead


def send_to_omnisend(lead, tag="first_flow_start", timeout=20):
    url = "https://api.omnisend.com/v5/contacts"

    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": settings.OMNISEND_API_KEY,
    }

    payload = {
        "firstName": lead.first_name,
        "lastName": lead.last_name,
        "tags": [tag],
        "identifiers": [
            {
                "id": lead.email,
                "type": "email",
                "channels": {
                    "email": {
                        "status": "subscribed",
                        "statusDate": lead.created_date.isoformat(),
                    }
                },
            }
        ],
    }

    # Si tiene teléfono lo agregamos (Omnisend lo acepta en E.164)
    if lead.phone_number:
        payload["identifiers"].append(
            {
                "id": lead.phone_number,
                "type": "phone",
                "channels": {
                    "sms": {
                        "status": "subscribed",
                        "statusDate": lead.created_date.isoformat(),
                    }
                },
            }
        )

    response = requests.post(url, json=payload, headers=headers, timeout=timeout)
    return response


class Command(BaseCommand):
    help = "Envía leads existentes a Omnisend y marca synced_at / status / error."

    def add_arguments(self, parser):
        parser.add_argument("--tag", type=str, default="first_flow_start")
        parser.add_argument("--campaign", type=str, default=None, help="Filtra por utm_campaign (parcial)")
        parser.add_argument("--notes_contains", type=str, default=None, help="Filtra por texto dentro de notes")
        parser.add_argument("--created_after", type=str, default=None, help="YYYY-MM-DD (created_date >= fecha)")
        parser.add_argument("--limit", type=int, default=None, help="Límite de leads a enviar")
        parser.add_argument("--sleep", type=float, default=0.15, help="Pausa entre requests (evita rate limit)")
        parser.add_argument("--dry_run", action="store_true", help="Solo muestra cuántos enviaría, no envía")

    def handle(self, *args, **opts):
        tag = opts["tag"]
        campaign = opts["campaign"]
        notes_contains = opts["notes_contains"]
        created_after = opts["created_after"]
        limit = opts["limit"]
        sleep_s = opts["sleep"]
        dry_run = opts["dry_run"]

        # ✅ Solo los no sincronizados aún
        qs = Lead.objects.filter(omnisend_synced_at__isnull=True).order_by("id")

        if campaign:
            qs = qs.filter(utm_campaign__icontains=campaign)

        if notes_contains:
            qs = qs.filter(notes__icontains=notes_contains)

        if created_after:
            dt = datetime.strptime(created_after, "%Y-%m-%d")
            qs = qs.filter(created_date__gte=make_aware(dt))

        # Solo leads con email (Omnisend necesita email al menos)
        qs = qs.filter(email__isnull=False).exclude(email="")

        if limit:
            qs = qs[:limit]

        total = qs.count()
        self.stdout.write(self.style.SUCCESS(f"Leads a procesar: {total}"))

        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN activado: no se enviará nada."))
            return

        ok = 0
        fail = 0

        for lead in qs:
            try:
                resp = send_to_omnisend(lead, tag=tag)

                # Guardamos status siempre
                lead.omnisend_last_status = resp.status_code

                if 200 <= resp.status_code < 300:
                    ok += 1
                    lead.omnisend_synced_at = now()
                    lead.omnisend_last_error = None
                    lead.save(update_fields=["omnisend_synced_at", "omnisend_last_status", "omnisend_last_error"])
                    self.stdout.write(self.style.SUCCESS(f"✔ OK {resp.status_code} | {lead.email}"))

                else:
                    fail += 1
                    # guardamos texto de error truncado
                    lead.omnisend_last_error = (resp.text or "")[:500]
                    lead.save(update_fields=["omnisend_last_status", "omnisend_last_error"])
                    self.stdout.write(self.style.ERROR(f"✘ FAIL {resp.status_code} | {lead.email} | {lead.omnisend_last_error[:200]}"))

            except Exception as e:
                fail += 1
                # En caso de error de red/timeout, status puede quedar None
                lead.omnisend_last_status = None
                lead.omnisend_last_error = str(e)[:500]
                lead.save(update_fields=["omnisend_last_status", "omnisend_last_error"])
                self.stdout.write(self.style.ERROR(f"✘ ERROR | {lead.email} | {str(e)}"))

            time.sleep(sleep_s)

        self.stdout.write(self.style.SUCCESS("\n🚀 ENVÍO FINALIZADO"))
        self.stdout.write(f"✅ OK: {ok}")
        self.stdout.write(f"❌ FAIL: {fail}")
