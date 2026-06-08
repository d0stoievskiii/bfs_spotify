from django.core.management.base import BaseCommand
from django.db import transaction

from webapp.models import Artist
from spotify_data.collab_search import con


class Command(BaseCommand):
    help = "Import artists from DuckDB into the Django database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--batch-size",
            type=int,
            default=10_000,
            help="Number of artists inserted per batch",
        )

        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete existing artists before importing",
        )

    def handle(self, *args, **options):
        batch_size = options["batch_size"]
        clear = options["clear"]

        if clear:
            self.stdout.write("Clearing existing artists...")
            Artist.objects.all().delete()

        total_rows = con.execute("""
            SELECT COUNT(*)
            FROM artists
        """).fetchone()[0]

        self.stdout.write(f"Found {total_rows} artists in DuckDB.")

        imported = 0
        offset = 0

        while offset < total_rows:
            rows = con.execute("""
                SELECT
                    id,
                    external_id,
                    name,
                    name_normalized,
                    followers_total,
                    popularity
                FROM artists
                ORDER BY id
                LIMIT ?
                OFFSET ?
            """, [batch_size, offset]).fetchall()

            objects = [
                Artist(
                    id=row[0],
                    external_id=row[1],
                    name=row[2],
                    name_normalized=row[3],
                    followers_total=row[4],
                    popularity=row[5],
                )
                for row in rows
            ]

            with transaction.atomic():
                Artist.objects.bulk_create(
                    objects,
                    batch_size=batch_size,
                    ignore_conflicts=True,
                )

            imported += len(objects)
            offset += batch_size

            self.stdout.write(f"Imported {imported}/{total_rows} artists")

        self.stdout.write(self.style.SUCCESS("Done."))