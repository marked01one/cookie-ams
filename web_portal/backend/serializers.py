from dataclasses import field
from numpy import source
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
  # Allows us to return the name of the foreign keys, instead of their IDs
  manufacturer = serializers.CharField(source='manufacturer.manufacturer_name')
  region = serializers.CharField(source='region.region_name')
  
  class Meta:
    model = Transformer
    fields = ['id', 'manufacturer', 'region', 'serial_number', 'kva', 'date_created']


class FailureSerializer(serializers.ModelSerializer):
  class Meta:
    model = Failure
    fields = ['id', 'transformer', 'failure_cause', 'description', 'date_failed']