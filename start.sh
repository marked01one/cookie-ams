source env/scripts/activate
if [ "$1" == "api" ]; then
  cd web_portal
  python manage.py runserver
elif [ "$1" == "client" ]; then
  cd web_portal/interface
  python app.py
elif [ "$1" == "seeder" ]; then
  cd web_portal
  python seeder.py $2
fi



