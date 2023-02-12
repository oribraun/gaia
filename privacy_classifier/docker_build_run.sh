docker stop privacy_classifier
docker rm privacy_classifier
docker build -t privacy_classifier .
docker run --name privacy_classifier -dp 8080:8080 privacy_classifier
#debug - docker run -it -p 8080:8080 privacy_classifier
