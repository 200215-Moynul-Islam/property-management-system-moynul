from django.urls import path
from .views import LocationAutocomplete

urlpatterns = [
    path('location-autocomplete/', LocationAutocomplete.as_view(), name='api_autocomplete'),
]