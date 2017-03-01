#!/bin/bash
if [ -z ${ROVERCODE_WEB_BETA+x} ]; then
  echo "This is not the beta deployment"
else
  find /home/ubuntu/rovercode-web/ -path /home/ubuntu/rovercode-web/.git -prune -o -path /home/ubuntu/rovercode-web/.env -prune -o -type f -print0 | xargs -0 sed -i 's/rovercode\.com/beta\.rovercode.com/g'
fi
