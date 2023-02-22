sudo cp /home/ubuntu/app/gaia/deploy/gaia_nginx.conf /etc/nginx/sites-available/gaia_nginx.conf
sudo ln -s /etc/nginx/sites-available/gaia_nginx.conf /etc/nginx/sites-enabled/
#sudo nano /etc/uwsgi/sites/gaia.ini
#sudo nano /etc/systemd/system/uwsgi.service
