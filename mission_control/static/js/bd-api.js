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
      createBd();
    } else {
      updateBd();
    }
  }
}

function createBd() {
  $.post('/api/v1/block-diagrams/', data, function(response){
    bdId = response.id;
    console.log('Created bd ' + bdId + ' on the server');
  })
    .fail(function(xhr, status, error){
      console.error("Failure when creating saved bd on server: " + xhr.statusText);
      writeToConsole("There was an error saving your design to the rover");
    });
}

function updateBd() {
  $.ajax({
    method: 'PUT',
    url: '/api/v1/block-diagrams/' + bdId + '/',
    data: data,
    complete: function(e, xhr, settings) {
      if (e.status === 200 ) {
        console.log('Update save sucess');
      } else if (e.status == 405) {
        console.log('This bd id does not exist on the server. Creating it.');
        createBd();
      } else {
        console.error("Failure when updating saved bd. Code " + e.status);
        writeToConsole("There was an error saving your design to the rover");
      }
    },
  });
}

function refreshSavedBds(userId) {
  $.get("/api/v1/block-diagrams/?user=" + userId, function(json){
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

function loadDesignByName(name) {
  $.get("/api/v1/block-diagrams/?name=" + name, function(json){
    if (!json.length){
      console.warn("Could not find block diagram named " + name);
      writeToConsole("Could not find block diagram named " + name);
    } else {
      /* For now, just load the first with that name */
      loadDesign(json[0]);
    }
  });
}

function loadDesign(design) {
  workspace.clear();
  xmlDom = Blockly.Xml.textToDom(design.content);
  Blockly.Xml.domToWorkspace(workspace, xmlDom);
  if (design.name == 'event_handler_hidden') {
    designName = "Unnamed_Design_" + (Math.floor(Math.random()*1000)).toString();
    /* leave bdId unassigned to that a new bd is created*/
  } else {
    designName = design.name;
    bdId = design.id;
  }
  $('a#designNameArea').text(designName);
  hideBlockByComment("MAIN EVENT HANDLER LOOP");
  var hiddenBlock;
  var allBlocksHidden = true;
  for (hiddenBlock of blocksToHide) {
    if (!hideBlock(hiddenBlock)) {
      allBlocksHidden = false;
    }
  }
  if (allBlocksHidden) {
    showBlock('always');
  }
  updateCode();
}
