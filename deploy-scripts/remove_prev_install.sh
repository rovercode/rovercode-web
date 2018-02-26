#!/bin/bash
if [ -d /home/ubuntu/rovercode-web ]; then
    pushd /home/ubuntu/rovercode-web > /dev/null
    docker-compose down
    popd > /dev/null
    rm -rf /home/ubuntu/rovercode-web
    set +e
    docker stop $(docker ps -a -q)
    docker rm $(docker ps -a -q)
    docker rmi $(docker images -q)
    set -e
fi
