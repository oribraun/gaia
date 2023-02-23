sudo cp /home/ubuntu/app/gaia/deploy/gaia_nginx.conf /etc/nginx/sites-available/gaia_nginx.conf
sudo ln -s /etc/nginx/sites-available/gaia_nginx.conf /etc/nginx/sites-enabled/
sudo cp /home/ubuntu/app/gaia/deploy/gaia.ini /etc/uwsgi/sites/gaia.ini
sudo systemctl restart nginx
#sudo nano /etc/uwsgi/sites/gaia.ini
#sudo nano /etc/systemd/system/uwsgi.service

sudo cp /home/ubuntu/app/gaia/deploy/gaia_nginx.conf /etc/nginx/sites-available/gaia_nginx_https.conf
sudo ln -s /etc/nginx/sites-available/gaia_nginx_https.conf /etc/nginx/sites-enabled/
sudo cp /home/ubuntu/app/gaia/deploy/gaia.ini /etc/uwsgi/sites/gaia.ini
sudo systemctl restart nginx
