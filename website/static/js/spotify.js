console.log("Spotify script has been loaded")

const launcher = (url) => {
    // Function - Set and display the Spotify embed
    // Add 'margin' to the bottom
    adjustFrame = document.getElementById("bottom-pad-frame");
    adjustFrame.style.height = '0';
    frame = document.getElementById("spotify-frame");
    frame.innerHTML = `<iframe class='spotify-embed' src="${url}" width="100%" height="80" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>`

    
    adjustFrame.style.minHeight = `80px`;
}
