#!/bin/bash
if [ "$DEPLOYMENT_GROUP_NAME" == "beta-rovercode-web" ]; then
  export TAG=beta
elif [ "$DEPLOYMENT_GROUP_NAME" == "alpha-rovercode-web" ]; then
  export TAG=alpha
else
  export TAG=prod
fi

if [ -d /home/ubuntu/rovercode-web ]; then
    pushd /home/ubuntu/rovercode-web > /dev/null
    TAG=$TAG docker-compose down --rmi all
    popd > /dev/null
    rm -rf /home/ubuntu/rovercode-web
fi
