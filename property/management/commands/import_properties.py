import os
import pandas as pd
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from django.core.files import File
from django.conf import settings
from sentence_transformers import SentenceTransformer
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
        
        model = SentenceTransformer('all-MiniLM-L6-v2')

        for _, row in df.iterrows():
            loc_name = row["location_name"].strip()
            name_vector = model.encode(loc_name).tolist()

            location, created = Location.objects.get_or_create(
                name=loc_name,
                defaults={
                    "point": Point(
                        float(row["lng"]),
                        float(row["lat"])
                    ),
                    "embedding": name_vector
                }
            )

            if not created and location.embedding is None:
                location.embedding = name_vector
                location.save(update_fields=['embedding'])

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
                source_image_path = os.path.join(settings.BASE_DIR, "property", "data", "images", image_url)
                if os.path.exists(source_image_path):
                    with open(source_image_path, "rb") as local_file:
                        img_instance = PropertyImage(
                            property=property_obj,
                            caption=row.get("title", "")
                        )
                        img_instance.image.save(image_url, File(local_file), save=True)

        self.stdout.write("Import successful")
