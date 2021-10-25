#!/bin/bash
aws ecr get-login-password | docker login --username AWS --password-stdin 795223264977.dkr.ecr.us-east-2.amazonaws.com

if [ "$DEPLOYMENT_GROUP_NAME" == "beta-rovercode-web" ]; then
  export TAG=beta
elif [ "$DEPLOYMENT_GROUP_NAME" == "alpha-rovercode-web" ]; then
  export TAG=alpha
else
  export TAG=prod
fi

cd /home/ubuntu/rovercode-web && docker-compose --project-name=rovercode build && docker-compose --project-name=rovercode up -d
