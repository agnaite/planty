function flash(flashMsg) {
  
  $('.flashes').append(flashMsg);

  setTimeout(function() {
    $('.flashes').empty();
  }, 3000);
}