uwsgi --socket /run/uwsgi/gaia.sock --chdir /home/ubuntu/app/gaia --module main_app.wsgi --chmod-socket=666

# https
uwsgi --socket /run/uwsgi/gaia_https.sock --chdir /home/ubuntu/app/gaia --module main_app.wsgi --chmod-socket=667

python manage.py crontab add