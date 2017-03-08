#!/bin/bash

our_ip=$(dig +short myip.opendns.com @resolver1.opendns.com)
beta_ip=$(dig +short beta.rovercode.com)

pushd /home/ubuntu/rovercode-web/mission_control/static > /dev/null
rm -rf blockly > /dev/null
git clone https://github.com/aninternetof/blockly.git
pushd blockly > /dev/null
if [ "$our_ip" == "$beta_ip" ]; then
  git checkout development
else
  git checkout master
fi
popd > /dev/null
git clone https://github.com/NeilFraser/JS-Interpreter.git
popd > /dev/null
