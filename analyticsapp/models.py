from django.db import models

# Create your models here.


class SalesRecord(models.Model):

    date = models.DateField()

    product = models.CharField(max_length=100)

    region = models.CharField(max_length=100)

    quantity = models.IntegerField()

    price = models.FloatField()

    revenue = models.FloatField()

    def __str__(self):
        return f"{self.product} - {self.region}"