// ******************************** AJAX SEARCH ********************************
function searchPlant(results) {
  var result_urls = [];
  console.log(results);

  if (results === "None") {
    $('#search-results').html("<li>No plants found <i class='fa fa-frown-o fa-lg' aria-hidden='true'></i>" + "<li>");
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


// **************************** AJAX PLANT EDIT ****************************

function finalizeEdit(results) {
  if (results.col === 'image') {
    $('*[data-column='+results.col+']').html("<img class='plant-img col-md-4 col-sm-12' src="+results.val+"></a>");
  } else {
    $('*[data-new='+results.col+']').html(results.val);
  }
}

function submitEdit(id, col) {
  var userValue = {'plantId': id,
                   'columnToEdit': col,
                   'newValue': $('#new_edit').val()};
  
  $.post('/edit_plant', userValue, finalizeEdit);
}

function startEdit(evt) {
  $(this).unbind('click');

  var plantId = $(this).attr('data-plant');
  var tableCol = $(this).attr('data-column');

  if (tableCol === 'sun') {
    $(this).html("<select id='new_edit'>" +
                 "<option value='Full Sun'>Full Sun</option>" +
                 "<option value='Bright Light'>Bright Light</option>" +
                 "<option value='Medium Light'>Medium Light</option>" +
                 "<option value='Low Light'>Low Light</option>" +
                 "</select>" +
                 "<input type='submit' id='submit-edit-btn'>");
  } else if (tableCol === 'water') {
      $(this).html("<select id='new_edit'>" +
                 "<option value='Moderately Moist'>Moderately Moist</option>" +
                 "<option value='Drench and Let Dry'>Drench and Let Dry</option>" +
                 "<option value='Keep on the Dry Side'>Keep on the Dry Side</option>" +
                 "</select>" +
                 "<input type='submit' id='submit-edit-btn'>");
  } else if (tableCol === 'humidity') {
      $(this).html("<select id='new_edit'>" +
                 "<option value='High Humidity'>High Humidity</option>" +
                 "<option value='Moderate Humidity'>Moderate Humidity</option>" +
                 "<option value='Average Home Humidity'>Average Home Humidity</option>" +
                 "<option value='Good Air Circulation'>Good Air Circulation</option>" +
                 "</select>" +
                 "<input type='submit' id='submit-edit-btn'>");

  } else if (tableCol === 'temperature') {
    $(this).html("<select id='new_edit'>" +
                 "<option value='Normal Room Temperatures'>Normal Room Temperatures</option>" +
                 "<option value='Warm Temperatures'>Warm Temperatures</option>" +
                 "<option value='Cool Temperatures'>Cool Temperatures</option>" +
                 "<option value='Cold Temperatures'>Cold Temperatures</option>" +
                 "</select>" +
                 "<input type='submit' id='submit-edit-btn'>");
  } else {
    $(this).html("<input type='text' id='new_edit'>" +
                 "<input type='submit' id='submit-edit-btn'>");
  }

  $('#submit-edit-btn').click(function(){ return submitEdit(plantId, tableCol); });
}

$('.edit-btn').click(startEdit);


