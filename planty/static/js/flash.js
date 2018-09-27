module.exports = function flash(flashMsg) {
  $('.flash').html(flashMsg);
  setTimeout(function() {
    $('.flash').empty();
  }, 3000);
};