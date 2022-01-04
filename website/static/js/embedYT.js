console.log("Youtube Embed script has been loaded")

function on() {
    document.getElementById("overlay").innerHTML = '<iframe id="ytplayer" width="560" height="315" src="https://www.youtube.com/embed/qAYWw67yiN0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
    document.getElementById("overlay").style.display = "block";
  }
  
  function off() {
    document.getElementById("overlay").style.display = "none";
  } 