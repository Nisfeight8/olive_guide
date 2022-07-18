function resize() {
    if ($(window).width() < 700) {
      $('#auth_card').removeClass('col');
    }
    else{
      $('#auth_card').addClass('col');
    }
  }

  $(document).ready(function(){
    resize()
  });