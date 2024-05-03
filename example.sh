#!/bin/bash

docker-compose up -d
docker-compose exec -it app bash -c './main.py --image ./input/1.png --langs en,ru --gpu 1'
docker-compose exec -it app bash -c './main.py --image ./input/2.png --langs en,ru --gpu 1'
docker-compose exec -it app bash -c './main.py --image ./input/3.png --langs en,ru --gpu 1'
docker-compose down
