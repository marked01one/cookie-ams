from dataclasses import field
from rest_framework import serializers

from .models import Manufacturer, Region, Transformer, Failure


class ManufacturerSerializer(serializers.ModelSerializer):
  class Meta:
    model = Manufacturer
    fields = ['id', 'manufacturer_name']
    

class RegionSerializer(serializers.ModelSerializer):
  class Meta:
    model = Region
    fields = ['id', 'region_name']


class TransformerSerializer(serializers.ModelSerializer):
  class Meta:
    model = Transformer
    fields = ['id', 'manufacturer', 'region', 'serial_number', 'kva', 'date_created']


class FailureSerializer(serializers.ModelSerializer):
  class Meta:
    model = Failure
    fields = ['id', 'transformer', 'failure_cause', 'description', 'date_failed']