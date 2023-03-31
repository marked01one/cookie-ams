import requests
from .error_service import error_handler_clean

BASE_URL = "http://127.0.0.1:8000/api"


class ManufacturerService:
  '''
  Utility class encapsulating HTTP calls for manufacturer data
  '''
  def get_manufacturers(self) -> dict:
    response = requests.get(f'{BASE_URL}/manufacturer/')
    return error_handler_clean(response)  


class TransformerService:
  '''
  Utility class encapsulating HTTP calls for manufacturer data
  '''
  def get_transformers(self, params_dict: dict) -> dict:
    response = requests.get(f'{BASE_URL}/transformers', params=params_dict)
    return error_handler_clean(response)