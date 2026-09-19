import json
import os
import uuid
from pathlib import Path
from django.core.management.base import BaseCommand
from django.db import transaction
from dictionary.models.sign import Sign
from dictionary.models.word import Word
from dictionary.models.choices import Categories, Status, GrammaticalCategories
from representations.models.representation import Representation
from representations.models.choices import Extensions
from users.models.user import User


class Command(BaseCommand):
    help = "Poblar base de datos con las 2,427 señas vectoriales SVG de LSRD usando bulk_create de alta velocidad"

    def add_arguments(self, parser):
        parser.add_argument(
            "--json-path",
            type=str,
            default=None,
            help="Ruta al archivo JSON maestro del diccionario SVG",
        )

    def handle(self, *args, **options):
        if options["json_path"]:
            json_path = Path(options["json_path"])
        else:
            base_dir = Path(__file__).resolve().parent.parent.parent.parent.parent
            json_path = base_dir / "ETL" / "output_svg_v2" / "diccionario_matrices_svg_v2.json"

        if not json_path.exists():
            self.stderr.write(self.style.ERROR(f"No se encontró el archivo JSON en: {json_path}"))
            return

        admin_user = User.objects.filter(is_active=True).first()
        if not admin_user:
            admin_user = User.objects.first()
        if not admin_user:
            self.stderr.write(self.style.ERROR("No existe ningún usuario en la base de datos para asociar los registros."))
            return

        self.stdout.write(self.style.NOTICE(f"Usuario asociado: {admin_user.username} ({admin_user.email})"))
        self.stdout.write(self.style.NOTICE(f"Cargando señas desde: {json_path}"))

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        total_items = len(data)
        self.stdout.write(f"Total de registros a procesar: {total_items}")

        with transaction.atomic():
            # 1. Obtener señas existentes para no duplicar
            existing_signs = {s.sign_name: s for s in Sign.objects.all()}
            signs_to_create = []
            
            # Mapeo temporal para asociar palabras con representaciones
            items_to_insert = []

            for index, item in enumerate(data, 1):
                palabra = item.get("palabra_clave", "").strip()
                if not palabra:
                    continue

                descripcion = item.get("descripcion", "").strip() or None
                svg_path = item.get("svg_individual", "")
                svg_file = os.path.basename(svg_path) if svg_path else f"sena_{index:04d}.svg"
                url_rep = f"assets/senias_svg/{svg_file}"

                if palabra not in existing_signs:
                    new_id = uuid.uuid4()
                    sign_obj = Sign(
                        id=new_id,
                        sign_name=palabra,
                        description=descripcion,
                        sign_category=Categories.SIGN,
                        is_active=Status.ACTIVE,
                        created_by=admin_user,
                    )
                    signs_to_create.append(sign_obj)
                    items_to_insert.append((sign_obj, palabra, descripcion, url_rep))
                else:
                    sign_obj = existing_signs[palabra]
                    items_to_insert.append((sign_obj, palabra, descripcion, url_rep))

            if signs_to_create:
                self.stdout.write(f"Insertando {len(signs_to_create)} señas en bulto...")
                Sign.objects.bulk_create(signs_to_create, batch_size=500)
                self.stdout.write("Señas insertadas exitosamente.")

            # Recargar mapa completo de señas
            all_signs = {s.sign_name: s for s in Sign.objects.all()}

            # 2. Bulk create de Words
            existing_words = set(Word.objects.values_list("word_name", flat=True))
            words_to_create = []
            seen_words = set()

            for sign_obj, palabra, descripcion, _ in items_to_insert:
                word_name = palabra[:50]
                if word_name not in existing_words and word_name not in seen_words:
                    seen_words.add(word_name)
                    words_to_create.append(
                        Word(
                            id=uuid.uuid4(),
                            word_name=word_name,
                            description=descripcion,
                            grammatical_category=GrammaticalCategories.NOUN,
                            is_active=Status.ACTIVE,
                            created_by=admin_user,
                        )
                    )

            if words_to_create:
                self.stdout.write(f"Insertando {len(words_to_create)} palabras asociadas en bulto...")
                Word.objects.bulk_create(words_to_create, batch_size=500)

            # 3. Bulk create de Representations
            existing_rep_sign_ids = set(
                Representation.objects.filter(extension=Extensions.SVG).values_list("sign_id_id", flat=True)
            )
            reps_to_create = []

            for _, palabra, _, url_rep in items_to_insert:
                sign_in_db = all_signs.get(palabra)
                if sign_in_db and sign_in_db.id not in existing_rep_sign_ids:
                    reps_to_create.append(
                        Representation(
                            id=uuid.uuid4(),
                            sign_id=sign_in_db,
                            extension=Extensions.SVG,
                            url=url_rep,
                            is_primary=True,
                            order=1,
                            is_active=True,
                            create_by=admin_user,
                        )
                    )

            if reps_to_create:
                self.stdout.write(f"Insertando {len(reps_to_create)} representaciones SVG en bulto...")
                Representation.objects.bulk_create(reps_to_create, batch_size=500)

        total_signs = Sign.objects.count()
        total_reps = Representation.objects.filter(extension=Extensions.SVG).count()
        total_words = Word.objects.count()

        self.stdout.write(
            self.style.SUCCESS(
                f"\nSincronización masiva de alta velocidad completada:\n"
                f"  - Señas en Base de Datos: {total_signs}\n"
                f"  - Palabras en Base de Datos: {total_words}\n"
                f"  - Representaciones SVG en Base de Datos: {total_reps}"
            )
        )
