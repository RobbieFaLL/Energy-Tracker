from django.db import models

class MeterReading(models.Model):
    date = models.DateField()
    kwh_used = models.FloatField()

class Tariff(models.Model):
    price_per_kwh = models.IntegerField(help_text="Enter price in pence (e.g., 15 for £0.15)")
