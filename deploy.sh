#!/bin/bash

#git pull
docker build .
sleep 5
docker-compose up -d
sleep 100
docker exec -it admissiontask_admissiontask_1 python manage.py migrate
