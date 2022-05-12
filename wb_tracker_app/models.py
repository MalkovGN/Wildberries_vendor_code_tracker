from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


class ProductCard(models.Model):
    """
    Product's card model
    """
    vendor_code = models.IntegerField()
    product_name = models.CharField(max_length=200, blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    sale_price = models.FloatField(blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    supplier = models.CharField(max_length=200, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_validate = RegexValidator(regex=r'^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$')
    date_from = models.CharField(max_length=10, blank=True, validators=[date_validate], null=True)
    date_to = models.CharField(max_length=10, blank=True, validators=[date_validate], null=True)

    def __str__(self):
        return self.product_name
