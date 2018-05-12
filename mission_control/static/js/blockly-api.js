/*----- DEFINE API -----*/

leftMotor = { FORWARD: "XIO-P0", BACKWARD: "XIO-P1" };
rightMotor = { FORWARD: "XIO-P6", BACKWARD: "XIO-P7" };
motorPins = { LEFT: leftMotor, RIGHT: rightMotor };

function initApi(interpreter, scope) {

	// Add an API function for the alert() block.
	var wrapper = function (text) {
		text = text ? text.toString() : '';
		return interpreter.createPrimitive(writeToConsole(text));
	};

	interpreter.setProperty(scope, 'alert',
		interpreter.createNativeFunction(wrapper));

	// Add an API function for highlighting blocks.
	wrapper = function (id) {
		id = id ? id.toString() : '';
		return interpreter.createPrimitive(highlightBlock(id));
	};
	interpreter.setProperty(scope, 'highlightBlock',
		interpreter.createNativeFunction(wrapper));

	// Add test API function for AJAX
	wrapper = function (text) {
		$.ajax({
			url: 'process.php',
			complete: function (response) {
				writeToConsole(response.responseText);
			},
			error: function () {
				$('#consoleArea').append('Bummer: there was an error!');
			}
		});
		return false;
	};
	interpreter.setProperty(scope, 'callMyPHP',
		interpreter.createNativeFunction(wrapper));

	// Add set motor API function
	wrapper = function (motor, direction, speed) {
		pin = motorPins[motor][direction];
		sendMotorCommand('START_MOTOR', pin, speed);
		return false;
	};
	interpreter.setProperty(scope, 'setMotor',
		interpreter.createNativeFunction(wrapper));

	// Add stop motor API function
	wrapper = function (motor) {
		/* Stop both forward and backward pins, just to be safe */
		sendMotorCommand('START_MOTOR', motorPins[motor].FORWARD, 0);
		sendMotorCommand('START_MOTOR', motorPins[motor].BACKWARD, 0);
		return false;
	};
	interpreter.setProperty(scope, 'stopMotor',
		interpreter.createNativeFunction(wrapper));

	// Add get sensor covered API function
	wrapper = function (sensor) {
		console.log("Made it to getSensorCovered");
		sensorCovered = sensorStateCache[sensor];
		return interpreter.createPrimitive(sensorCovered);
	};
	interpreter.setProperty(scope, 'getSensorCovered',
		interpreter.createNativeFunction(wrapper));

	// Add continue API function
	/* TODO: Make the highlighting stay on continue block while sleeping */
	wrapper = function (lengthInMs) {
		beginSleep(lengthInMs);
		writeToConsole("Sleeping for " + lengthInMs + "ms.");
		return false;
	};
	interpreter.setProperty(scope, 'sleep',
		interpreter.createNativeFunction(wrapper));

	// Add test API function for popping the event queue
	wrapper = function (text) {
		/* For some reason, there are serious problems when
		 * currentEvent is '' */
		currentEvent = 'nothing';
		if (eventQueue.length > 0) {
			console.log('There is something in the event queue');
			console.log('Here it is: ' + eventQueue);
			currentEvent = eventQueue.shift();
		}
		return interpreter.createPrimitive(currentEvent);
	};
	interpreter.setProperty(scope, 'popEventQueue',
		interpreter.createNativeFunction(wrapper));
}
