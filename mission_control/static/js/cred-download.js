$("#download-env").click(function() {
    if ('Blob' in window) {
        var textToSave = "CLIENT_ID="+clientId+"\nCLIENT_SECRET="+clientSecret+"\n";
        var textToSaveAsBlob = new Blob([textToSave], {type:"text/plain"});
        var textToSaveAsURL = window.URL.createObjectURL(textToSaveAsBlob);
        var fileNameToSaveAs = "rovercode_"+name+".env";
        var downloadLink = document.createElement("a");
        downloadLink.download = fileNameToSaveAs;
        downloadLink.href = textToSaveAsURL;
        downloadLink.onclick = destroyClickedElement;
        downloadLink.style.display = "none";
        document.body.appendChild(downloadLink);
        downloadLink.click();
    } else {
        console.error("No blob support");
        alert('Sorry, your browser does not support HTML5 Blobs. Please try using a newer browser.');
    }
})

function destroyClickedElement(event)
{
    document.body.removeChild(event.target);
}
