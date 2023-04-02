if [ "$1" == "api" ]; then
  source env/scripts/activate
  cd web_portal
  python manage.py runserver
elif [ "$1" == "client" ]; then
  source env/scripts/activate
  cd web_portal/interface
  python app.py
fi



