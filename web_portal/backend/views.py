from datetime import datetime
from rest_framework.response import Response
from rest_framework import viewsets, status, mixins
from django.db.models.manager import BaseManager
from django.db.models import Model
from django.http import HttpRequest

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
    

class TransformerViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
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
  serializer = serializer_class(queryset, many=True)
  
  def list(self, request, *args, **kwargs):
    # Define query params object
    params = {
      "manufacturer_id": request.GET.get('manufacturer_id'),
      "region_id": request.GET.get('region_id'),
      "kva": float(request.GET.get('kva')) if (request.GET.get('kva') != None) else None,
      "page": request.GET.get('page'),
      "page_size": request.GET.get('page_size')
    }
    queryset = self.filter_queryset(
      self._helper_querystring_filter(Transformer.objects.all().order_by('id'), params)
    )
    serializer = TransformerSerializer(queryset, many=True)


    try: 
      paginated_queryset = self.paginate_queryset(queryset)
    except Exception:
      return Response({
        "status": status.HTTP_404_NOT_FOUND,
        "message": "Not Found error. There is no page '" + params['page'] + "' to be found.",
        "results" : []
      })

    if params['page'] != None or params['page_size'] != None:
      paginated_serializer = self.get_serializer(paginated_queryset, many=True)
      return self.get_paginated_response(paginated_serializer.data)

    return Response({
      "count": len(serializer.data),
      "message": 'All transformer records.',
      "results" : serializer.data
    })
  
  
  def create(self, request: HttpRequest) -> Response:
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
  
  
  def _helper_querystring_filter(self, queryset: BaseManager[Model], params_map: dict) -> BaseManager[Model]:
    for key in params_map.keys():
      if params_map[key] != None and key not in ['page', 'page_size']:
        param = {key: params_map[key]}
        queryset = queryset.filter(**param)
    
    return queryset