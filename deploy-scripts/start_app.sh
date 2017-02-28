#!/bin/bash
cd /home/ubuntu/rovercode-web
docker-compose build
docker-compose up -d
return 0
