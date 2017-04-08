/*----- MISC GLOBALS -----*/
var roverDomain = ''; //Later, if the rover is not hosting the webpage, its address will go here
var roverApiPath = '/api/v1/';
var bdId = null;

/*----- HELPER FUNCTIONS -----*/
function roverResource(resource) {
  return roverDomain + roverApiPath + (Array.isArray(resource) ? resource.join('/') : resource);
}

/*----- ROVER API FUNCTIONS -----*/
function sendMotorCommand(command, pin, speed) {
  $.post(roverResource('sendcommand'),
  {
    command: command,
    pin: pin,
    speed: Number(speed)
  }, function (response) {
    //writeToConsole(response);
  });
}
