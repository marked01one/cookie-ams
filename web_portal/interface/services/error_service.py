from requests import Response

def error_handler_clean(response: Response) -> dict:
  body = {
      "response_code": response.status_code,
      "content": response.json(),
    }
    
  match str(response.status_code)[0]:
    case '2':
      body['status'] = 'success!'
    # Client side errors
    case '4':
      body['status'] = 'client-side error!'
    case '5':
      body['status'] = 'server-side error!'
    case _:
      body['status'] = 'unexpected error!'
  
  return body  