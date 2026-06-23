from rest_framework.generics import ListAPIView
from pgvector.django import CosineDistance
from sentence_transformers import SentenceTransformer
from property.models import Location
from .serializers import LocationSerializer

model = SentenceTransformer('all-MiniLM-L6-v2')

class LocationAutocomplete(ListAPIView):
    serializer_class = LocationSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', '').strip()
        if not query:
            return Location.objects.none()
        
        query_vector = model.encode(query).tolist()
        
        return (
            Location.objects
            .annotate(distance=CosineDistance('embedding', query_vector))
            .filter(distance__lt=0.6)
            .order_by('distance')[:10]
        )
