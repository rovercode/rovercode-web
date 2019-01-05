#!/bin/bash

pushd /home/ubuntu/rovercode-web/mission_control/static > /dev/null
rm -rf blockly > /dev/null
git clone https://github.com/aninternetof/blockly.git
pushd blockly > /dev/null
if [ "$DEPLOYMENT_GROUP_NAME" == "beta-rovercode-web" ]; then
  git checkout development
elif [ "$DEPLOYMENT_GROUP_NAME" == "alpha-rovercode-web" ]; then
  git checkout alpha
else
  git checkout master
fi
popd > /dev/null
git clone https://github.com/NeilFraser/JS-Interpreter.git
popd > /dev/null
