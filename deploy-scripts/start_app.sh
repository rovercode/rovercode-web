#!/bin/bash
echo "In the start_app.sh"
pushd /home/ubuntu/rovercode-web > /dev/null
cp env.example .env
docker-compose build
docker-compose up
popd > /dev/null
