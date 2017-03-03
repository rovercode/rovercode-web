#!/bin/bash
pushd /home/ubuntu/rovercode-web > /dev/null
docker-compose down
popd > /dev/null
rm -rf /home/ubuntu/rovercode-web
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker rmi $(docker images -q)
