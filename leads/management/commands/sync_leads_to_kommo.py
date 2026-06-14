import time

from django.core.management.base import BaseCommand

from leads.models import Lead
from leads.services.kommo_service import sync_contact_to_kommo


class Command(BaseCommand):
    help = "Sincroniza leads sin kommo_contact_id con Kommo CRM."

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            default=50,
            help='Cantidad máxima de leads a procesar (default: 50)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Muestra cuántos leads se procesarían sin ejecutar la sincronización',
        )

    def handle(self, *args, **opts):
        limit  = opts['limit']
        dry_run = opts['dry_run']

        # Leads que aún no tienen contacto creado en Kommo
        qs = (
            Lead.objects
            .filter(kommo_contact_id__isnull=True)
            .exclude(phone_number='')
            .order_by('id')[:limit]
        )

        total = qs.count()
        self.stdout.write(self.style.SUCCESS(f'Leads a procesar: {total}'))

        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN activado: no se sincronizará nada.'))
            for lead in qs:
                self.stdout.write(
                    f'  [dry-run] ID={lead.id} | {lead.first_name} {lead.last_name} | {lead.phone_number}'
                )
            return

        ok   = 0
        fail = 0

        for lead in qs:
            try:
                sync_contact_to_kommo(lead)

                # Refrescamos desde BD para ver si se guardó el contact_id
                lead.refresh_from_db(fields=['kommo_contact_id', 'kommo_last_error'])

                if lead.kommo_contact_id:
                    ok += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'OK | ID={lead.id} | {lead.phone_number} | kommo_id={lead.kommo_contact_id}'
                        )
                    )
                else:
                    fail += 1
                    self.stdout.write(
                        self.style.ERROR(
                            f'FAIL | ID={lead.id} | {lead.phone_number} | error={lead.kommo_last_error or "desconocido"}'
                        )
                    )

            except Exception as exc:
                fail += 1
                self.stdout.write(
                    self.style.ERROR(f'ERROR | ID={lead.id} | {lead.phone_number} | {exc}')
                )

            # Pausa para respetar rate limits de la API de Kommo
            time.sleep(0.15)

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('SINCRONIZACION FINALIZADA'))
        self.stdout.write(f'OK:   {ok}')
        self.stdout.write(f'FAIL: {fail}')
