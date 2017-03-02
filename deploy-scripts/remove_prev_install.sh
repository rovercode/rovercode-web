#!/bin/bash
pushd /home/ubuntu/rovercode-web > /dev/null
docker-compose down
popd > /dev/null
rm -rf /home/ubuntu/rovercode-web
docker rmi $(docker images -q)
