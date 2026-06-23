from rest_framework.generics import ListAPIView
from property.models import Location
from .serializers import LocationSerializer

class LocationAutocomplete(ListAPIView):
    serializer_class = LocationSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', '').strip()
        if not query:
            return Location.objects.none()
        return Location.objects.filter(name__icontains=query)[:5]