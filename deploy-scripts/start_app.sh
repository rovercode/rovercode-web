#!/bin/bash
pushd /home/ubuntu/rovercode-web > /dev/null
cp env.example .env
docker-compose build
docker-compose up
popd > /dev/null
