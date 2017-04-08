function saveDesign() {
  xml = Blockly.Xml.workspaceToDom(workspace);
  xmlString = Blockly.Xml.domToText(xml);
  if (userId === null) {
    console.log("Not logged in. In demo mode. Not saving");
  } else {
    data = {
      "user": userId,
      "name": designName,
      "content": xmlString
    };
    if (bdId === null) {
      saveFirst();
    } else {
      saveAgain();
    }
  }
}

function saveFirst() {
  $.post('/mission-control/block-diagrams/', data, function(response){
    bdId = response.id;
    console.log('Created bd ' + bdId + ' on the server server');
  })
    .fail(function(){
      console.log("Failure when creating saved bd on server.");
      writeToConsole("There was an error saving your design to the rover");
    });
}

function saveAgain() {
  $.ajax({
    method: 'PUT',
    url: '/mission-control/block-diagrams/' + bdId + '/',
    data: data,
    complete: function(e, xhr, settings) {
      if (e.status === 200 ) {
        console.log('Update save sucess');
      } else if (e.status == 405) {
        console.log('This bd id does not exist on the server. Creating it.');
        saveFirst();
      } else {
        console.log("Failure when updating saved bd. Code " + e.status);
        writeToConsole("There was an error saving your design to the rover");
      }
    },
  });
}

function refreshSavedBds(userId) {
  $.get("/mission-control/block-diagrams/?user=" + userId, function(json){
    if (!json.length){
      $('#savedDesignsArea').text("There are no designs saved.");
    } else {
      $('#savedDesignsArea').empty();
      $.each(json, function(index, entry) {
        $(document.createElement('button'))
          .addClass('btn btn-primary')
          .text(entry.name)
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
