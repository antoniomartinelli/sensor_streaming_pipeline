#!/bin/bash
#wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip -O drill/ngrok.zip
#unzip ngrok.zip
#rm ngrok.zip

docker system prune --force
docker volume prune --force
docker-compose up --build
