from django.contrib import admin
from django.contrib.gis import admin as gis_admin
from django.utils.html import format_html

from .models import Location, Property, PropertyImage


@admin.register(Location)
class LocationAdmin(gis_admin.GISModelAdmin):
    list_display = ("id", "name", "point")
    search_fields = ("name",)


class PropertyImageInline(admin.StackedInline):
    model = PropertyImage
    extra = 0
    fields = (("image", "image_preview"), "caption")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 120px; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />',
                obj.image.url,
            )
        return "-"

    image_preview.short_description = "Current Preview"


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "price",
        "location",
        "bedrooms",
        "bathrooms",
    )
    search_fields = ("title",)
    list_filter = ("location", "bedrooms", "bathrooms", "price")
    inlines = [PropertyImageInline]


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ("id", "property", "image_preview", "caption")

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="80" height="60" style="object-fit:cover;" />',
                obj.image.url,
            )
        return "-"

    image_preview.short_description = "Preview"
    