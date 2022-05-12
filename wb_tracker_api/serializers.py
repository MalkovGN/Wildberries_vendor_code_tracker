from rest_framework import serializers

from wb_tracker_app.models import ProductCard


class ProductCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCard
        fields = [
            'id',
            'vendor_code',
            'product_name',
            'brand',
            'price',
            'sale_price',
            'supplier'
        ]
