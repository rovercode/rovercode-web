/*----- MISC GLOBALS -----*/
var sidebarVisible = true;
var runningEnabled = false;
var blocksToHide = ["always", "initially","whenRightEyeSeesSomething", "whenLeftEyeSeesSomething"];
//var blocksToHide = [];
var hiddenBlocks = [];
var highlightPause = false;
var blocklyArea = document.getElementById('blocklyArea');
var blocklyDiv = document.getElementById('blocklyDiv');
var eventQueue = [];

/*----- SENSOR VALUES CACHE -----*/
/** Keep track of the last-known value of a sensor locally. Update
* it according to events. This keeps us from having to do a synchronous
* poll when the blockly code requests the value.
*/
var sensorStateCache = new Array();
sensorStateCache["SENSORS_leftIr"] = false;
sensorStateCache["SENSORS_rightIr"] = false;

/*----- INIT CODE -----*/
var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
});

/* Set overall Blockly colors */
Blockly.HSV_SATURATION = 0.85;
Blockly.HSV_VALUE = 0.9;
Blockly.Flyout.prototype.CORNER_RADIUS = 0;
Blockly.BlockSvg.START_HAT = true;

/* Socket for for sensor events */
function connectToSocket() {
  socket = io.connect(roverResource(''));
  socket.on('connect', function () {
    socket.emit('status', {data: 'Connected'});
  });
  socket.on('binary_sensors', function(msg) {
    writeToConsole(msg.data);
    updateLocalStateAfterEvent(msg.data);
    eventQueue.push(msg.data);
  });
  socket.on('status', function(msg) {
    writeToConsole(msg.data);
  });
}

/* Inject Blockly */
var workspace = Blockly.inject(blocklyDiv,
  {toolbox: document.getElementById('toolbox'),
  css: false,
  zoom:
  {controls: true,
    wheel: false,
    startScale: 1.0,
    maxScale: 3,
    minScale: 0.3,
    scaleSpeed: 1.2},
    trashcan: true,
  }
);
workspace.addChangeListener(updateCode);
workspace.addChangeListener(saveDesign);
if (bdToLoad) {
  console.log("Loading design " + bdToLoad);
  loadDesign(bdToLoad);
} else {
  loadDesignByName('event_handler_hidden');
  $('#nameModal').modal();
}
writeToConsole("rovercode console started");

/* Handle Blockly resizing */
var onresize = function(e) {
  console.log("Resizing");
  var element = blocklyArea;
  var x = 0;
  var y = 0;
  do {
    x += element.offsetLeft;
    y += element.offsetTop;
    element = element.offsetParent;
  } while (element);
  blocklyDiv.style.left = x + 'px';
  blocklyDiv.style.top = y + 'px';
  blocklyDiv.style.width = blocklyArea.offsetWidth + 'px';
  blocklyDiv.style.height = blocklyArea.offsetHeight + 'px';
};
window.addEventListener('resize', onresize, false);
onresize();

/* Prevent default right-click menu from getting in the way of ours */
document.addEventListener("contextmenu", function(e){
  e.preventDefault();
}, false);

/* Bind key shortcuts */
document.onkeydown = keyEvent;
function keyEvent(e) {
  var evtobj = window.event ? event : e;
  //Ctrl-Shift-7 to run code
  if (evtobj.keyCode == 55 && evtobj.ctrlKey && evtobj.shiftKey)
  {
    goToRunningState();
  }
  //Ctrl-Shift-8 to stop code
  if (evtobj.keyCode == 56 && evtobj.ctrlKey && evtobj.shiftKey)
  {
    goToStopState();
  }
  //Ctrl-Shift-9 to step code
  if (evtobj.keyCode == 57 && evtobj.ctrlKey && evtobj.shiftKey)
  {
    stepCode();
  }
  //Ctrl-Shift-0 to reset code
  if (evtobj.keyCode == 48 && evtobj.ctrlKey && evtobj.shiftKey)
  {
    resetCode();
  }
}

/* Add video stream */
/* videoSource = 'http://' + window.location.hostname + ':8080/?action=stream'; */
/* $('#videoBackground').append('<img src=' + videoSource + ' />'); */
/* $('#videoBackground').find('img').on("error", function() { */
  $('#videoBackground').empty();
  $('#videoBackground').append("[no Rover webcam detected]");
/* }); */

/*----- BD NAME FUNCTIONS -----*/
function acceptName() {
  designName = $('input[name=designName]').val();

  if (!designName) {
    $('#nameErrorArea').text('Please enter a name for your design in the box');
  } else {
    $.get("/api/v1/block-diagrams/?user=" + userId, function(json){
      var duplicate = json.indexOf(designName) > -1;
      if (duplicate) {
        $('#nameErrorArea').text('This name has already been chosen. Please pick another one.');
      } else {
        saveDesign();
        $('#nameErrorArea').empty();
        $('a#designNameArea').text(designName);
        $('a#downloadLink').attr("onclick", "return downloadDesign(\""+designName+".xml\")");
        $('#nameModal').modal('hide');
      }
    });
  }

}
testString = "more stuff";

/*----- UI EVENT HANDLING -----*/
function updateLocalStateAfterEvent(event){
  switch(event) {
    case 'leftEyeCovered':
    sensorStateCache.SENSORS_leftIr = true;
    $(".leftEyeIndicator").css("background-color", "#43AC6A");
    break;
    case 'leftEyeUncovered':
    sensorStateCache.SENSORS_leftIr = false;
    $(".leftEyeIndicator").css("background-color", "#BBBBBB");
    break;
    case 'rightEyeCovered':
    sensorStateCache.SENSORS_rightIr = true;
    $(".rightEyeIndicator").css("background-color", "#43AC6A");
    break;
    case 'rightEyeUncovered':
    sensorStateCache.SENSORS_rightIr = false;
    $(".rightEyeIndicator").css("background-color", "#BBBBBB");
    break;
    default:
    break;

  }
}

/*----- ROVER CONNECTION FUNCTIONS -----*/
function getRovers() {
  $('#registeredRoversArea').empty();
  $('#connectModal').modal('toggle');
  $.getJSON("/api/v1/rovers", function(result){
      $.each(result, function(i, field){
        console.log(field.name);
        $(document.createElement('a')).addClass('btn btn-primary')
        .html(field.name + " | " + field.owner)
        .attr('href', '#')
        .css('margin', '10px')
        .appendTo($("#registeredRoversArea"))
        .click(function() {
          setRoverIp(field.local_ip);
          $('#connectModal').modal('hide');
        });
      });
  });
}

function setRoverIp(ip) {
  writeToConsole('Talking to rover at ' + ip);
  roverDomain = ip;
  connectToSocket();
}

/*----- DESIGN SAVING/LOADING FUNCTIONS -----*/

function chooseDesign(userId) {
  $('#nameModal').modal('hide');
  $('#loadModal').modal('show');
  refreshSavedBds(userId);
}

$('#uploadForm #fileToUpload').change(function(){
  var file = this.files[0];
  var type = file.type;
  if(type == "text/xml")
  $('#loadErrorArea').empty();
  else
  $('#loadErrorArea').text("Please select a .xml file");
});

$('#uploadForm input[name=button]').click(uploadDesign);

/*----- RUNNING SANDBOXED CODE FUNCTIONS -----*/

function updateCode() {
  code = Blockly.JavaScript.workspaceToCode(workspace);
  Blockly.JavaScript.STATEMENT_PREFIX = 'highlightBlock(%1);\n';
  Blockly.JavaScript.addReservedWords('highlightBlock');
  myInterpreter = new Interpreter(code, initApi);
  highlightPause = false;
  workspace.traceOn(true);
  workspace.highlightBlock(null);
  runningEnabled = false;
  sleeping = false;
}

function showCode() {
  updateCode();
  /* Remove 'highlightBlock' code generated from Blockly */
  strippedCode = code.replace(/highlightBlock\(\'[0-9]+\'\);/g, '');
  let editor = ace.edit('editor');
  editor.setTheme('ace/theme/iplastic');
  editor.getSession().setMode('ace/mode/javascript');
  editor.setReadOnly(true);
  editor.setFontSize(14);
  editor.setValue(strippedCode);
  $('#codeViewModal').modal();
}

function beginSleep(sleepTimeInMs) {
  sleeping = true;
  window.setTimeout(endSleep, sleepTimeInMs);
}

function endSleep() {
  sleeping = false;
  if (runningEnabled)
  runCode();
}

function runCode() {
  if (stepCode() && runningEnabled && !sleeping) {
    window.setTimeout(runCode, 10);
  }
}

function stepCode() {
  var ok = myInterpreter.step();
  if (!ok) {
    // Program complete, no more code to execute.
    workspace.highlightBlock(null);
    console.log("code finished");
    goToStopState();
    return false;
  }
  if (highlightPause) {
    // A block has been highlighted.  Pause execution here.
    //console.log("code paused");
    highlightPause = false;
  } else {
    // Keep executing until a highlight statement is reached.
    stepCode();
  }
  return true;
}

function resetCode() {
  goToStopState();
  updateCode();
}

function goToRunningState() {
  $('#runButton > i').css('color', '#FFCC33');
  updateCode();
  runningEnabled = true;
  runCode();
}

function goToStopState() {
  sendMotorCommand('START_MOTOR', motorPins.LEFT.FORWARD, 0);
  sendMotorCommand('START_MOTOR', motorPins.LEFT.BACKWARD, 0);
  sendMotorCommand('START_MOTOR', motorPins.RIGHT.FORWARD, 0);
  sendMotorCommand('START_MOTOR', motorPins.RIGHT.BACKWARD, 0);
  runningEnabled = false;
  $('#runButton > i').css('color', '#FFFFFF');
}

/*----- BLOCK VISIBILITY FUNCTIONS -----*/

function toggleBlock(blockName) {
  loc = hiddenBlocks.indexOf(blockName);
  if (loc> -1)
  showBlock(blockName);
  else
  hideBlock(blockName);
}

function showBlock(blockName) {
  loc = hiddenBlocks.indexOf(blockName);
  blocks = workspace.getTopBlocks(true);
  for(var i=0; i<blocks.length; i++) {
    try {
      if (blocks[i].inputList[0].fieldRow[1].text_ == blockName) {
        blocks[i].setShadow(false);
        blocks[i].setCollapsed(false);
        blocks[i].setCommentText(null);
        blocks[i].svgGroup_.style.display = "inline";
        hiddenBlocks.splice(loc,1);
      }
    }
    catch(err) {
      /* Do nothing */
    }
  }
}

function hideBlock(blockName) {
  blocks = workspace.getTopBlocks(true);
  for(var i=0; i<blocks.length; i++) {
    try {
      if (blocks[i].inputList[0].fieldRow[1].text_ == blockName) {
        if(blocks[i].childBlocks_.length === 0)	{
          blocks[i].setShadow(true);
          blocks[i].setCollapsed(true);
          blocks[i].svgGroup_.style.display = "none";
          blocks[i].setCommentText('PASS');
          hiddenBlocks.push(blockName);
          return true;
        }	else {
          return false;
        }
      }
    } catch(err) {
      /* Do nothing */
    }
  }
}

function hideBlockByComment(comment) {
  blocks = workspace.getTopBlocks(true);
  for(var i=0; i<blocks.length; i++) {
    try {
      if (blocks[i].getCommentText().indexOf(comment) > -1) {
        blocks[i].setShadow(true);
        blocks[i].setCollapsed(true);
        blocks[i].svgGroup_.style.display = "none";
      }
    }	catch(err) {
      /* Do nothing */
    }
  }
}

/*----- PAGE ELEMENT VISIBILITY FUNCTIONS -----*/

function toggleSidebar() {
  var widthDelta = 400;
  if ($("#codeArea").is(":visible")){
    var currentWidth = $('#blocklyArea').outerWidth();
    $("#blocklyArea").css("min-width", currentWidth+widthDelta);
  } else {
    $("#blocklyArea").css("min-width", 'auto');
  }
  $("#consoleArea").fadeToggle(0);
  $("#videoBackground").fadeToggle(0);
  $("#indicatorsArea").fadeToggle(0);
  onresize();
  Blockly.fireUiEvent(window, 'resize');
}

function highlightBlock(id) {
  if (workspace.getBlockById(id).getCommentText().indexOf('PASS') > -1) {
    //console.log('not pausing');
    highlightPause = false;
  } else {
    highlightPause = true;
    workspace.highlightBlock(id);
  }
}

/*----- UTILITY FUNCTIONS -----*/

function writeToConsole(entry) {
  consoleDiv = $('#consoleArea');
  consoleDiv.append("<p>>> "+entry+"</p>");
  consoleDiv[0].scrollTop = consoleDiv[0].scrollHeight;
}
