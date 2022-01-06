console.log("Youtube Embed script has been loaded")

function on(url){
  document.getElementById("overlay").innerHTML = `<iframe id="ytplayer" type="text/html" src="http://www.youtube.com/embed/${url}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"></iframe>`
  document.getElementById("overlay").style.display = "flex";
  document.getElementById("overlay").classList.add("box-on-center");
}
  
function off(){
  document.getElementById("overlay").innerHTML = ""
  document.getElementById("overlay").style.display = "none";
  document.getElementById("overlay").classList.remove("box-on-center");
} 