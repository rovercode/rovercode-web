#!/bin/bash

if [ "$DEPLOYMENT_GROUP_NAME" == "beta-rovercode-web" ]; then
  find /home/ubuntu/rovercode-web/ -path /home/ubuntu/rovercode-web/.git -prune -o -path /home/ubuntu/rovercode-web/.env -prune -o -type f -print0 | xargs -0 sed -i 's/rovercode\.com/beta\.rovercode.com/g'
elif [ "$DEPLOYMENT_GROUP_NAME" == "alpha-rovercode-web" ]; then
  find /home/ubuntu/rovercode-web/ -path /home/ubuntu/rovercode-web/.git -prune -o -path /home/ubuntu/rovercode-web/.env -prune -o -type f -print0 | xargs -0 sed -i 's/rovercode\.com/alpha\.rovercode.com/g'
else
  echo "This is not the beta or alpha deployment"
fi
