#!/bin/bash
pushd /home/ubuntu/rovercode-web > /dev/null
docker-compose stop
popd > /dev/null
rm -rf /home/ubuntu/rovercode-web
