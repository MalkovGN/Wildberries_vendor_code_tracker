import requests
from rest_framework import generics

from wb_tracker_app.models import ProductCard
from . import serializers


class ProductCardList(generics.ListCreateAPIView):
    queryset = ProductCard.objects.all()
    serializer_class = serializers.ProductCardSerializer


class ProductCardDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductCard.objects.all()
    serializer_class = serializers.ProductCardSerializer
