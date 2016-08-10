function searchPlant(results) {
  var result_urls = [];

  if (typeof(results) === "string") {
    $('#search-results').html("<li>" + results + "<li>");
  } else {
    // for each result item, makes an href link with plant name
    for(var plant in results) {
      result_urls.push("<li><a href='/plant/" + plant + "'>" + results[plant] +
                     "</a></li>");
    }
    // appends each link in the list to the search result div
    for(var i = 0; i < result_urls.length; i++) {
      $('#search-results').append(result_urls[i]);
    }
  }
}

function startSearch(evt) {
  evt.preventDefault();

  // clears the search results div
  $('#search-results').html('');

  // makes a js object out of the data entered in search field and makes
  // ajax get request to route '/search'
  var searchTerm = {'plant-name': $('#search-field').val()};
  $.get('/search', searchTerm, searchPlant);
}

// on click of search button, calls the ajax function
$('#search-btn').click(startSearch);

