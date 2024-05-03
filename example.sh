#!/bin/bash

docker-compose exec -it app bash -c './main.py'

exec "$@"
