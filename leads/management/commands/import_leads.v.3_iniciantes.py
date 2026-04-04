import csv
import re

from django.core.management.base import BaseCommand
from django.db.models import Q

from leads.models import Lead


# Perú móvil: +51 9XXXXXXXX
PERU_MOBILE_REGEX = re.compile(r'^\+519\d{8}$')

# E.164 general
E164_REGEX = re.compile(r'^\+\d{10,15}$')


def normalize_phone(raw_phone):
    if not raw_phone:
        return None

    phone = str(raw_phone).strip()

    # caso Excel científico
    if "E+" in phone.upper():
        try:
            phone = str(int(float(phone)))
        except:
            pass

    digits = re.sub(r"\D", "", phone)

    # si ya tenía +
    if phone.startswith("+"):
        return "+" + digits

    # 9XXXXXXXX
    if len(digits) == 9 and digits.startswith("9"):
        return "+51" + digits

    # 519XXXXXXXX
    if len(digits) == 11 and digits.startswith("51") and digits[2] == "9":
        return "+" + digits

    return "+" + digits if digits else None


def classify_phone(phone):
    if not phone:
        return False, False

    is_peru = bool(PERU_MOBILE_REGEX.match(phone))
    is_e164 = bool(E164_REGEX.match(phone))
    is_foreign = is_e164 and not is_peru

    return is_peru, is_foreign


class Command(BaseCommand):
    help = "Importa leads desde CSV (Meta Lead Ads)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            required=True,
            help="Ruta del CSV"
        )

    def handle(self, *args, **options):

        file_path = options["file"]

        inserted = 0
        skipped_invalid_phone = 0
        skipped_missing_email = 0
        skipped_duplicate = 0

        with open(file_path, newline="", encoding="cp1252") as csvfile:

            reader = csv.DictReader(csvfile, delimiter=";")

            required_cols = {
                "created_time",
                "campaign_name",
                "nombre_completo",
                "correo_electronico",
                "numero_de_telefono",
                "¿qué_sede_y_horario_te_interesa?",
            }

            missing = required_cols - set(reader.fieldnames or [])

            if missing:
                raise Exception(f"Faltan columnas en el CSV: {missing}")

            for row in reader:

                # -------------------------
                # NOMBRE
                # -------------------------
                nombre = (row.get("nombre_completo") or "").strip()

                if not nombre:
                    continue

                partes = nombre.split(" ", 1)

                first_name = partes[0].strip()
                last_name = partes[1].strip() if len(partes) > 1 else ""

                # -------------------------
                # EMAIL
                # -------------------------
                email = (row.get("correo_electronico") or "").strip().lower()

                if not email:
                    skipped_missing_email += 1
                    self.stdout.write(self.style.WARNING("Lead sin email omitido"))
                    continue

                # -------------------------
                # TELEFONO
                # -------------------------
                raw_phone = row.get("numero_de_telefono")

                phone = normalize_phone(raw_phone)

                is_peru, is_foreign = classify_phone(phone)

                if not is_peru and not is_foreign:
                    skipped_invalid_phone += 1
                    self.stdout.write(self.style.WARNING(f"Teléfono inválido: {raw_phone}"))
                    continue

                # -------------------------
                # HORARIO / SEDE
                # -------------------------
                interest_raw = (row.get("¿qué_sede_y_horario_te_interesa?") or "").strip()

                # -------------------------
                # DUPLICADOS
                # -------------------------
                exists = Lead.objects.filter(
                    Q(email=email) |
                    Q(phone_number=phone)
                ).exists()

                if exists:
                    skipped_duplicate += 1
                    self.stdout.write(self.style.WARNING(f"Duplicado omitido: {email} / {phone}"))
                    continue

                # -------------------------
                # CREAR LEAD
                # -------------------------
                Lead.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone_number=phone,

                    status="NEW",

                    lead_interest_raw=interest_raw,

                    utm_source="meta",
                    utm_medium="paid_social",
                    utm_campaign=(row.get("campaign_name") or "").strip(),

                    notes=f"Lead importado desde Meta Lead Ads | created_time={row.get('created_time')}",
                )

                inserted += 1

                self.stdout.write(
                    self.style.SUCCESS(f"Insertado: {email} / {phone}")
                )

        # -------------------------
        # RESUMEN FINAL
        # -------------------------
        self.stdout.write(self.style.SUCCESS("\nIMPORTACIÓN FINALIZADA"))
        self.stdout.write(f"Insertados: {inserted}")
        self.stdout.write(f"Teléfonos inválidos: {skipped_invalid_phone}")
        self.stdout.write(f"Sin email: {skipped_missing_email}")
        self.stdout.write(f"Duplicados: {skipped_duplicate}")