#!/bin/bash

start_api () {
  source env/scripts/activate
  cd web_portal
  python manage.py runserver
} 

start_client () {
  sleep 3s
  source env/scripts/activate
  cd interface
  python app.py
}

if [ "$1" == "client" ]; then
  start_client
elif [ "$1" == "api" ]; then
  start_api
else
  start_api & start_client
fi




