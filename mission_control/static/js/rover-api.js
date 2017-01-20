/*----- MISC GLOBALS -----*/
var roverDomain = ''; //Later, if the rover is not hosting the webpage, its address will go here
var roverApiPath = '/api/v1/';

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

function saveDesign() {
  xml = Blockly.Xml.workspaceToDom(workspace);
  xmlString = Blockly.Xml.domToText(xml);
  $.post(roverResource('blockdiagrams'), {bdString: xmlString, designName: designName}, function(response){
  }).error(function(){
    writeToConsole("There was an error saving your design to the rover");
  });
}

function refreshSavedBds() {
  $.get(roverResource('blockdiagrams'), function(json){
    if (!json.result.length){
      $('#savedDesignsArea').text("There are no designs saved on this rover");
    } else {
      $('#savedDesignsArea').empty();
      json.result.forEach(function(entry) {
        $(document.createElement('a')).addClass('button')
        .html(entry)
        .attr('href', '#')
        .css('margin', '10px')
        .appendTo($("#savedDesignsArea"))
        .click(function() {
          return loadDesign(entry);
        });
      });
    }
  }
);
}

function loadDesign(name) {
  $.get(roverResource(['blockdiagrams', name]), function(response){
    workspace.clear();

    xmlDom = Blockly.Xml.textToDom(response.getElementsByTagName('bd')[0].childNodes[0].nodeValue);
    Blockly.Xml.domToWorkspace(workspace, xmlDom);
    if (name == 'event_handler_hidden')
    designName = "Unnamed_Design_" + (Math.floor(Math.random()*1000)).toString();
    else
    designName = name;
    $('a#downloadLink').attr("onclick", "return downloadDesign(\""+designName+".xml\")");
    $('a#designNameArea').text(designName);

    hideBlockByComment("MAIN EVENT HANDLER LOOP");
    var hiddenBlock;
    var allBlocksHidden = true;
    for (hiddenBlock of blocksToHide) {
      if (!hideBlock(hiddenBlock))
      allBlocksHidden = false;
    }
    if (allBlocksHidden) {
      showBlock('always');
    }
  }).error(function(){
    alert("There was an error loading your design from the rover");
  });
  updateCode();
}

function acceptName() {
  designName = $('input[name=designName]').val();

  if (!designName) {
    $('#nameErrorArea').text('Please enter a name for your design in the box');
  } else {
    $.get(roverResource('blockdiagrams'), function(json){
      var duplicate = json.result.indexOf(designName) > -1;
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

function downloadDesign(name) {
  $.get(roverResource(['download', name]), function(response) {
    var blob = new Blob([new XMLSerializer().serializeToString(response)]);
    var downloadUrl = URL.createObjectURL(blob);
    $(document.createElement('a'))
    .attr( {'download': name, 'href': downloadUrl} )
    .get(0)
    .click();
  }).error(function() {
    alert("There was an error accessing your design");
  });
}

function uploadDesign() {
  var formData = new FormData();
  formData.append("fileToUpload", $('#fileToUpload').get(0).files[0]);

  $.ajax({
    url: roverResource(['upload']),
    type: 'POST',
    xhr: function() {  // Custom XMLHttpRequest
      var myXhr = $.ajaxSettings.xhr();
      return myXhr;
    },
    success: function (data) {
      refreshSavedBds();
      $("#loadStatusArea").text(data + " Look for it above.");

    },
    error: function (xhr, ajaxOptions, thrownError) {
      $("#loadStatusArea").text("There was an error uploading your design. " + thrownError);
    },
    data: formData,
    cache: false,
    contentType: false,
    processData: false
  });
}
