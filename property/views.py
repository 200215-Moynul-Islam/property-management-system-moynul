from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, get_object_or_404
from django.contrib.gis.db.models.functions import Distance
from .models import Property, Location
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Property

def home_view(request):
    return render(request, "home.html")


def property_list_view(request):
    location_query = request.GET.get('location', '')
    items_per_page = int(request.GET.get('items_per_page', 6))
    page_number = request.GET.get('page', 1)

    if location_query:
        property_list = Property.objects.filter(location__name__icontains=location_query)
    else:
        property_list = Property.objects.all()

    paginator = Paginator(property_list, items_per_page)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'location_name': location_query,
        'items_per_page': items_per_page,
    }
    return render(request, 'property_list.html', context)


def property_detail_view(request, pk):
    property_obj = get_object_or_404(
        Property.objects
        .select_related("location")
        .prefetch_related("images")
        .annotate(distance_value=Distance("point", "location__point")),
        pk=pk,
    )

    distance_km = None

    if property_obj.point and property_obj.location.point:
        distance_km = round(property_obj.distance_value.km, 2)

    return render(
        request,
        "property_detail.html",
        {
            "property": property_obj,
            "distance_km": distance_km,
        },
    )
