console.log("Scripts has been loaded");

if (document.getElementById("desc-text").offsetHeight < 130){
    console.log('need to be ');
    document.getElementById("readmore-link").style.display = "none";
}

$(".readmore-link").click( function(e) {
    console.log("Function expansion");
    // record if our text is expanded
    var isExpanded =  $(e.target).hasClass("expand");
    
    //close all open paragraphs
    $(".readmore.expand").removeClass("expand");
    $(".readmore-link.expand").removeClass("expand");
    
    // if target wasn't expand, then expand it
    if (!isExpanded){
      $( e.target ).parent( ".readmore" ).addClass( "expand" );
      $(e.target).addClass("expand");
      document.getElementById("desc-text").classList.add("expand");
      // document.getElementById("desc-text").style.maxHeight = "130px";
    }
});