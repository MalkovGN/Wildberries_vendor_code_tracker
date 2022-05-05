from django.db import models
from django.core.validators import RegexValidator


class ProductCard(models.Model):
    """
    Product's card model
    """
    vendor_code = models.IntegerField()
    product_name = models.CharField(max_length=200)
    price = models.FloatField()
    sale_price = models.FloatField()
    brand = models.CharField(max_length=100)
    supplier = models.CharField(max_length=200)

    def __str__(self):
        return self.product_name


class VendorCode(models.Model):
    """
    Model for input
    a vendor code
    and time interval
    """
    date_validate = RegexValidator(regex=r'^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$')
    vendor_code = models.IntegerField()
    date_from = models.CharField(max_length=10, blank=True, validators=[date_validate])
    date_to = models.CharField(max_length=10, blank=True, validators=[date_validate])
