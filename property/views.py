from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.contrib.gis.db.models.functions import Distance
from .models import Property, Location

def home_view(request):
    return render(request, "home.html")

