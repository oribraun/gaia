uwsgi --socket /run/uwsgi/gaia.sock --chdir /home/ubuntu/app/gaia --module main_app.wsgi --chmod-socket=666

# https
uwsgi --socket /run/uwsgi/gaia_https.sock --chdir /home/ubuntu/app/gaia --module main_app.wsgi --chmod-socket=667

#python manage.py crontab add
#cronjob -e
#/home/ubuntu/app/gaia/venv/bin/python /home/ubuntu/app/gaia/manage.py crontab run 73274fe689719bb6e19498816411605d