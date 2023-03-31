from django.db import models
from rest_framework.settings import api_settings


class Manufacturer(models.Model):
  manufacturer_name = models.CharField(max_length=255)
  
  def __str__(self) -> str:
    return self.manufacturer_name
  

class Region(models.Model):
  region_name = models.CharField(max_length=255)
  
  def __str__(self) -> str:
    return self.region_name


class Transformer(models.Model):
  manufacturer = models.ForeignKey(Manufacturer, on_delete=models.PROTECT)
  region = models.ForeignKey(Region, on_delete=models.PROTECT)
  serial_number = models.CharField(max_length=15, unique=True)
  kva = models.FloatField()
  date_created = models.DateField()
  
  def __str__(self) -> str:
    return self.serial_number


class Failure(models.Model):
  transformer = models.ForeignKey(Transformer, on_delete=models.SET)
  failure_cause = models.CharField(max_length=255)
  description = models.TextField()
  date_failed = models.DateField(auto_now_add=True)
  
  def __str__(self) -> str:
    return f"{self.transformer.serial_number} failure on {self.date_failed}"