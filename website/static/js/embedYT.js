console.log("Youtube Embed script has been loaded")

function on(url) {
    document.getElementById("overlay").innerHTML = `<iframe id="ytplayer" type="text/html" width="960" height="540" src="http://www.youtube.com/embed/${url}" loading="lazy"></iframe>`
    document.getElementById("overlay").style.display = "block";
  }
  
  function off() {
    document.getElementById("overlay").innerHTML = ""
    document.getElementById("overlay").style.display = "none";
  } 