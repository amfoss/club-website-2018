$(document).ready(function() {
  if($(window).width() < 900)
  {
    $('#sidebar').addClass('fadeOutLeft');
    $(".wrapper").css("margin-left", "0");
  }
  else {
    $('#toggle_button').removeClass('fa-bars');
    $('#toggle_button').addClass('fa-times');
  }
  $('#toggle_button').click(function(){
      if($('#sidebar').hasClass("fadeOutLeft"))
      {
        $('#toggle_button').removeClass('fa-bars');
        $('#toggle_button').addClass('fa-times');
        $('#sidebar').removeClass('fadeOutLeft');
        $('#sidebar').addClass('fadeInLeft');
        $(".wrapper").css("margin-left", "250px");

      }
      else {
        $('#toggle_button').addClass('fa-bars');
        $('#toggle_button').removeClass('fa-times');
        $('#sidebar').removeClass('fadeInLeft');
        $('#sidebar').addClass('fadeOutLeft');
        $(".wrapper").css("margin-left", "0");
      }
  });
  $('#open-inside-foss').click(function(){
      if($('#open-inside-foss ul').hasClass("fadeOut"))
      {
        $('#open-inside-foss ul').removeClass('fadeOut').addClass('fadeIn').css('display','block');
        $('#open-inside-foss span').removeClass('fa-chevron-down').addClass('fa-chevron-up');
      }
      else {
        $('#open-inside-foss ul').removeClass('fadeIn').addClass('fadeOut').delay(500).css('display','none');
        $('#open-inside-foss span').addClass('fa-chevron-down').addClass('fa-chevron-down');
      }
  });
  $(window).scroll(function(){
    var position = $(window).scrollTop();
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
