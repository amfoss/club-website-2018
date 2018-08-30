$(document).ready(function() {
  $(window).scroll(function(){
    var position = $(window).scrollTop();
    console.log("position is " + position);
    if(position > 70 ) {
      $('#go_to_top').show();
    } else {
      $('#go_to_top').hide();
    }
  });

  $("#go_to_top").click(function(event){
    event.preventDefault();
    $("html, body").animate({scrollTop: 0}, "slow");
    return false;
  });
});
