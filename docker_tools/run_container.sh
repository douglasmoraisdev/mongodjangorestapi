#docker run -it -d -p 81:80 --name=c9webserver -v $PWD:/workspace/ douglasmorais/c9-php-dev:beta2
docker run -it -d -p 81:80 --name=$2 -v $PWD:/workspace/ douglasmorais/$1
