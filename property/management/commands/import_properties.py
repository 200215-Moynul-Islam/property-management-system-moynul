import pandas as pd

from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point

from property.models import Location, Property, PropertyImage


class Command(BaseCommand):
    help = "Import properties from CSV"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            required=True,
            help="Path to CSV file",
        )

    def handle(self, *args, **options):
        file_path = options["file"]

        self.stdout.write(f"Reading CSV: {file_path}")

        df = pd.read_csv(file_path)

        for _, row in df.iterrows():
            location, _ = Location.objects.get_or_create(
                name=row["location_name"],
                defaults={
                    "point": Point(
                        float(row["lng"]),
                        float(row["lat"])
                    )
                }
            )

            property_obj = Property.objects.create(
                location=location,
                title=row["title"],
                description=row.get("description", ""),
                price=row["price"],
                bedrooms=row.get("bedrooms", 0),
                bathrooms=row.get("bathrooms", 0),
                point=Point(
                    float(row["lng"]),
                    float(row["lat"])
                )
            )

            image_url = row.get("image_url")

            if image_url:
                PropertyImage.objects.create(
                    property=property_obj,
                    image=image_url,
                    caption=row.get("title", "")
                )

        self.stdout.write("Import successful")
