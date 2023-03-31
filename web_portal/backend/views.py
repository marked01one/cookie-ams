from datetime import datetime
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets, status

from .pagination import ResultsSetPagination

from .serializers import ManufacturerSerializer, RegionSerializer, TransformerSerializer

from .models import Manufacturer, Region, Transformer

# Create your views here.
class ManufacturerViewSet(viewsets.ViewSet):
  '''
  A simple ViewSet for operating on Manufacturer data
  '''
  def list(self, request):
    queryset = Manufacturer.objects.all()
    serializer = ManufacturerSerializer(queryset, many=True)
    return Response(serializer.data)
  
  def retrieve(self, request, pk=None):
    queryset = Manufacturer.objects.get(pk=pk)
    serializer = ManufacturerSerializer(queryset)
    return Response(serializer.data)
  
  def create(self, request):
    serializer = ManufacturerSerializer(data=request.data)
    if serializer.is_valid():
      body = serializer.data
      manufacturer = Manufacturer(manufacturer_name=body['manufacturer_name'])
      manufacturer.save()
      
      return Response(body, status=status.HTTP_201_CREATED)
    
    
    
class RegionViewSet(viewsets.ViewSet):
  '''
  A simple ViewSet for operating on manufacturer data
  '''  
  def list(self, request):
    queryset = Region.objects.all()
    serializer = RegionSerializer(queryset, many=True)
    return Response(serializer.data)
  
  def retrieve(self, request, pk=None):
    queryset = Region.objects.get(pk=pk)
    serializer = RegionSerializer(queryset)
    return Response(serializer.data)
  
  def create(self, request):
    serializer = RegionSerializer(data=request.data)
    if serializer.is_valid():
      body = serializer.data
      region = Region(region_name=body['region_name'])
      region.save()
      return Response(body, status=status.HTTP_201_CREATED)
    

class TransformerViewSet(viewsets.ViewSet):
  '''
  A simple ViewSet for operating on transformer data
  
  ## Methods
  - ### `list`
    - GET method for retrieving all transformers
  - ### `retrieve`
    - GET method for retrieving only one specific transformer
  - ### `create`
    - POST method for generating an individual instance of a transformer
  '''
  queryset = Transformer.objects.all()
  serializer_class = TransformerSerializer
  pagination_class = ResultsSetPagination
  
  def list(self, request):
    params = {
      "manufacturer_id": request.query_params.get('manufacturer'),
      "region_id": request.query_params.get('region'),
      "kva": float(request.query_params.get('kva'))
              if (request.query_params.get('kva') != None)
              else None
    }
    queryset = Transformer.objects.filter(**params)
    serializer = TransformerSerializer(queryset, many=True)
    return Response(serializer.data)
  
  
  def create(self, request):
    '''
    ## Request body
    ```json
    {
      "manufacturer": "Siemens",
      "region": "Coastal",
      "serial_number": "T1234567",
      "kva": 112.5,
      "date_created": "2003-01-22"
    }
    ```
    
    '''
    body = TransformerSerializer(data=request.data).initial_data
    manufacturer_fk = Manufacturer.objects.get(
      manufacturer_name=body['manufacturer']
    )
    region_fk = Region.objects.get(region_name=body['region'])
      
    transformer = Transformer(
      manufacturer=manufacturer_fk,
      region=region_fk,
      serial_number=body['serial_number'],
      kva=body['kva'],
      date_created=datetime.strptime(body["date_created"], "%Y-%m-%d").date()
    )
    transformer.save()
    return Response(
      status=status.HTTP_201_CREATED,
      data={
        "status": "successfully added new transformer!",
        "serial_number": transformer.serial_number
      }
    )
  