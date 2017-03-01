#!/bin/bash

our_ip=$(dig +short myip.opendns.com @resolver1.opendns.com)
beta_ip=$(dig +short beta.rovercode.com)

if [ "$our_ip" == "$beta_ip" ]; then
  find /home/ubuntu/rovercode-web/ -path /home/ubuntu/rovercode-web/.git -prune -o -path /home/ubuntu/rovercode-web/.env -prune -o -type f -print0 | xargs -0 sed -i 's/rovercode\.com/beta\.rovercode.com/g'
else
  echo "This is not the beta deployment"
fi
