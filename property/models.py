from django.db import models
from django.contrib.gis.db import models as gis_models
from pgvector.django import VectorField


class Location(models.Model):
    name = models.CharField(max_length=255)
    point = gis_models.PointField(
        geography=True,
        srid=4326,
    )
    embedding = VectorField(
        dimensions=1536,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class Property(models.Model):
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name="properties",
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=14,
        decimal_places=2,
    )
    bedrooms = models.PositiveSmallIntegerField(default=0)
    bathrooms = models.PositiveSmallIntegerField(default=0)
    point = gis_models.PointField(
        geography=True,
        srid=4326,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title


class PropertyImage(models.Model):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="images",
    )

    image = models.ImageField(
        upload_to="properties/%Y/%m/"
    )

    caption = models.CharField(
        max_length=255,
        blank=True,
    )

    def __str__(self):
        return self.image.name
