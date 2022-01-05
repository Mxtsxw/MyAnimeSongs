console.log("Youtube Embed script has been loaded")

function on(url) {
    document.getElementById("overlay").innerHTML = `<iframe id="ytplayer" type="text/html" src="http://www.youtube.com/embed/${url}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"></iframe>`
    document.getElementById("overlay").style.display = "block";
  }
  
  function off() {
    document.getElementById("overlay").innerHTML = ""
    document.getElementById("overlay").style.display = "none";
  } 