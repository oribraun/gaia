docker stop gaia_app
docker rm gaia_app
docker build -t gaia_app .
docker run --name gaia_app -dp 8000:8000 gaia_app
#debug - docker run -it -p 8080:8080 privacy_classifier
