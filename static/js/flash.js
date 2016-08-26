module.exports = function flash(flashMsg) {
  $('.flash').append(flashMsg);

  setTimeout(function() {
    $('.flash').empty();
  }, 3000);
};