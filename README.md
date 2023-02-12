# How to Run

1. python -m venv venv
2. venv/Scripts/activate
3. pip install -R requirements.txt
4. python manage.py runserver

# run localy using angular client on localhost:4200
1. python manage.py runserver --settings=main_app.settings_dev

# when making changed in db models
1. python manage.py makemigrations
2. python manage.py migrate