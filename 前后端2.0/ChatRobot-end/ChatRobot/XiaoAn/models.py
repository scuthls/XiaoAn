from django.db import models


class Product(models.Model):
    product_name = models.CharField(max_length=255, blank=True, null=False,primary_key=True)
    product_time = models.CharField(max_length=50, blank=True, null=True)
    issuer = models.CharField(max_length=255, blank=True, null=True)
    invest_type = models.CharField(max_length=255, blank=True, null=True)
    risk_level = models.CharField(max_length=255, blank=True, null=True)
    begin_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    return_type = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

