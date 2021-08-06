#!/bin/bash
docker system prune --force
docker volume prune --force
docker-compose up --build
