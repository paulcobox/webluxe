import csv
import re

from django.core.management.base import BaseCommand
from django.db.models import Q
import unicodedata
from leads.models import Lead


# Perú móvil: +51 9XXXXXXXX
PERU_MOBILE_REGEX = re.compile(r'^\+519\d{8}$')

# E.164 general (extranjero): + y 10 a 15 dígitos
E164_REGEX = re.compile(r'^\+\d{10,15}$')


def normalize_phone(raw_phone):
    """
    Limpia teléfono:
    p:+519XXXXXXXX -> +519XXXXXXXX
    """
    if not raw_phone:
        return None

    phone = raw_phone.strip()

    if phone.startswith("p:"):
        phone = phone[2:].strip()

    phone = (
        phone.replace(" ", "")
             .replace("-", "")
             .replace("(", "")
             .replace(")", "")
    )

    return phone or None


def classify_phone(phone):
    """
    Retorna (is_peru, is_foreign)
    """
    if not phone:
        return False, False

    if phone == "000000000":
        return False, False

    is_peru = bool(PERU_MOBILE_REGEX.match(phone))
    is_e164 = bool(E164_REGEX.match(phone))
    is_foreign = is_e164 and not is_peru

    return is_peru, is_foreign


def normalize_key(value: str) -> str:
    if not value:
        return ""
    v = value.strip().lower()

    # quita tildes
    v = unicodedata.normalize("NFKD", v)
    v = "".join(c for c in v if not unicodedata.combining(c))

    # normaliza guion largo
    v = v.replace("–", "-")

    # deja solo letras/numeros -> _
    v = re.sub(r"[^a-z0-9]+", "_", v)
    v = re.sub(r"_+", "_", v).strip("_")
    return v


def get_row_value(row: dict, key: str) -> str:
    # por si viene con espacios raros
    return (row.get(key) or "").strip()


class Command(BaseCommand):
    help = "Importa leads desde CSV (Meta Lead Ads) con validación Perú + extranjero y deduplicación"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            default="leads_instagram_verano_2026.csv",
            help="Ruta del CSV",
        )

    def handle(self, *args, **options):
        file_path = options["file"]

        inserted = 0
        skipped_invalid_phone = 0
        skipped_missing_email = 0
        skipped_duplicate = 0

        # ✅ Tu CSV usa ';' y Windows suele venir como latin-1
        with open(file_path, newline="", encoding="cp1252") as csvfile:

            reader = csv.DictReader(csvfile, delimiter=";")
            reader.fieldnames = [h.strip() for h in (reader.fieldnames or [])]

            # ✅ Columnas reales de TU CSV
            required_cols = {
                "created_time",
                "campaign_name",
                "nombre_completo",
                "correo_electronico",
                "numero_de_telefono",
                "¿qué_curso_te_interesa_más?",
                "¿has_tomado_clases_de_salsa_o_danza_antes?",
                "¿en_qué_horario_podrías_asistir_de_forma_constante?",
                "para_tomar_clases_de_danza,_¿con_cuál_de_estas_opciones_te_identificas_más?",
            }
            print(reader.fieldnames)

            missing = required_cols - set(reader.fieldnames or [])
            if missing:
                raise Exception(f"Faltan columnas en el CSV: {missing}")

            for row in reader:
                # -----------------
                # NOMBRE
                # -----------------
                nombre = (row.get("nombre_completo") or "").strip()
                if not nombre:
                    continue

                partes = nombre.split(" ", 1)
                first_name = partes[0].strip()
                last_name = partes[1].strip() if len(partes) > 1 else ""

                # -----------------
                # EMAIL
                # -----------------
                email = (row.get("correo_electronico") or "").strip().lower()
                if not email:
                    skipped_missing_email += 1
                    self.stdout.write(self.style.WARNING("⚠ Lead sin email, omitido"))
                    continue

                # -----------------
                # TELÉFONO
                # -----------------
                raw_phone = row.get("numero_de_telefono")
                phone = normalize_phone(raw_phone)
                is_peru, is_foreign = classify_phone(phone)

                if not is_peru and not is_foreign:
                    skipped_invalid_phone += 1
                    self.stdout.write(self.style.WARNING(f"❌ Teléfono inválido: {raw_phone}"))
                    continue

                # -----------------
                # DUPLICADOS (email o phone)
                # -----------------
                exists = Lead.objects.filter(Q(email=email) | Q(phone_number=phone)).exists()
                if exists:
                    skipped_duplicate += 1
                    self.stdout.write(self.style.WARNING(f"⚠ Duplicado omitido: {email} / {phone}"))
                    continue

                # -----------------
                # CREAR LEAD
                # -----------------
                tag = "Perú" if is_peru else "Extranjero"
                
                form_course_raw = get_row_value(row, "¿qué_curso_te_interesa_más?")
                form_experience_raw = get_row_value(row, "¿has_tomado_clases_de_salsa_o_danza_antes?")
                form_schedule_raw = get_row_value(row, "¿en_qué_horario_podrías_asistir_de_forma_constante?")
                form_motivation_raw = get_row_value(row, "para_tomar_clases_de_danza,_¿con_cuál_de_estas_opciones_te_identificas_más?")

                form_course_key = normalize_key(form_course_raw)
                form_experience_key = normalize_key(form_experience_raw)
                form_schedule_key = normalize_key(form_schedule_raw)
                form_motivation_key = normalize_key(form_motivation_raw)

                Lead.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone_number=phone,
                    course_of_interest=None,
                    status="NEW",
                    utm_source="instagram",
                    utm_medium="paid_social",
                    utm_campaign=(row.get("campaign_name") or "").strip(),

                    # 👇 NUEVO (requiere que ya existan en tu modelo)
                    form_course_raw=form_course_raw,
                    form_experience_raw=form_experience_raw,
                    form_schedule_raw=form_schedule_raw,
                    form_motivation_raw=form_motivation_raw,

                    form_course_key=form_course_key,
                    form_experience_key=form_experience_key,
                    form_schedule_key=form_schedule_key,
                    form_motivation_key=form_motivation_key,

                    notes=f"Lead importado desde Meta Lead Ads ({tag}) | created_time={row.get('created_time')}",
                )


                inserted += 1
                self.stdout.write(self.style.SUCCESS(f"✔ Insertado: {email} / {phone} ({tag})"))

        # -----------------
        # RESUMEN
        # -----------------
        self.stdout.write(self.style.SUCCESS("\n🚀 IMPORTACIÓN FINALIZADA"))
        self.stdout.write(f"✅ Insertados: {inserted}")
        self.stdout.write(f"❌ Teléfonos inválidos: {skipped_invalid_phone}")
        self.stdout.write(f"⚠ Leads sin email: {skipped_missing_email}")
        self.stdout.write(f"⚠ Duplicados omitidos: {skipped_duplicate}")
