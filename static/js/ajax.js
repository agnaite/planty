!function($) {
  
  // ******************************** DELETE ALERT/AJAX ***********************************  

  function deleteRequestSubmitted(results) {
    // redirects to homepage after plant deletion
    window.location.replace("/");
  }

  function deleteWarning(evt) {
    // displays confirmatory "sweetalert" alert
    swal({title: "Are you sure?",
          text: "You will not be able to recover this plant.",
          imageSize: "120x120",
          showCancelButton: true,
          imageUrl: "/static/img/plant.svg",
          animation: false,
          confirmButtonColor: "#DD6B55",
          confirmButtonText: "Yes, delete it.",
          cancelButtonText: "No, cancel pls!",
          closeOnConfirm: true,
          closeOnCancel: true },

          function(isConfirm){
            // if user clicked confirm delete, send ajax request to flask to delete
            // plant from the db
            if (isConfirm) {
              $.post('/delete_request',
                    {'dataPlant': $('.delete-control').attr('data-plant')},
                     deleteRequestSubmitted);
            }
          });
  }

  $('.delete-control').click(deleteWarning);

  // ******************************** AJAX SEARCH ********************************
  // function searchPlant(results) {
  //   var result_urls = [];
  //   console.log(results);

  //   if (results === "None") {
  //     $('#search-results').html("<li>No plants found <i class='fa fa-frown-o fa-lg' aria-hidden='true'></i>" + "<li>");
  //   } else {
  //     // for each result item, makes an href link with plant name
  //     for(var plant in results) {
  //       result_urls.push("<li><a href='/plant/" + plant + "'>" + results[plant] +
  //                      "</a></li>");
  //     }
  //     // appends each link in the list to the search result div
  //     for(var i = 0; i < result_urls.length; i++) {
  //       $('#search-results').append(result_urls[i]);
  //     }
  //   }
  // }

  // function startSearch(evt) {
  //   evt.preventDefault();

  //   // clears the search results div
  //   $('#search-results').html('');

  //   // makes a js object out of the data entered in search field and makes
  //   // ajax get request to route '/search'
  //   var searchTerm = {'plant-name': $('#search-field').val()};
  //   $.get('/search', searchTerm, searchPlant);
  // }

  // // on click of search button, calls the ajax function
  // $('#search-btn').click(startSearch);


  // **************************** AJAX PLANT EDIT ****************************

  function finalizeEdit(results) {
    // if results from server are for image, changes the src attribute for plant image
    // else changes the html for the edited plant spec
    if (results.col === 'image') {
      $('*[data-column='+results.col+']').html("<img class='plant-img col-md-4 col-sm-12' src="+results.val+"></a>");
    } else {
      $('*[data-new='+results.col+']').html(results.val);
    }
  }

  function submitEdit(id, col) {
    // makes a js object of the plant id, column, and user entered value
    var userValue = {'plantId': id,
                     'columnToEdit': col,
                     'newValue': $('#new_edit').val()};
    // calls an ajax post request to route edit plant and sends in the dict above
    $.post('/add_to_plant', userValue, finalizeEdit);
  }

  function startEdit(evt) {
    // stops further clicks
    $(this).unbind('click');

    // gets the plant id and attribute clicked on
    var plantId = $(this).attr('data-plant');
    var tableCol = $(this).attr('data-column');

    // checks what is clicked on and replaces html with appropriate form fields
    var form_start = "<form class='form-inline'>"+
                     "<div class='form-group'>"+
                     "<select id='new_edit' class='form-control'>";

    var form_end = "</select></div>" +
                   "<input type='submit' class='btn btn-default' id='submit-edit-btn'>"+
                   "</form>";

    if (tableCol === 'sun') {
      $(this).html(form_start +
                   "<option value='Full Sun'>Full Sun</option>" +
                   "<option value='Bright Light'>Bright Light</option>" +
                   "<option value='Medium Light'>Medium Light</option>" +
                   "<option value='Low Light'>Low Light</option>" +
                   form_end
                   );

    } else if (tableCol === 'water') {
        $(this).html(form_start +
                     "<option value='Moderately Moist'>Moderately Moist</option>" +
                     "<option value='Drench and Let Dry'>Drench and Let Dry</option>" +
                     "<option value='Keep on the Dry Side'>Keep on the Dry Side</option>" +
                     form_end);

    } else if (tableCol === 'humidity') {
        $(this).html(form_start +
                     "<option value='High Humidity'>High Humidity</option>" +
                     "<option value='Moderate Humidity'>Moderate Humidity</option>" +
                     "<option value='Average Home Humidity'>Average Home Humidity</option>" +
                     "<option value='Good Air Circulation'>Good Air Circulation</option>" +
                     form_end);

    } else if (tableCol === 'temperature') {
      $(this).html(form_start +
                   "<option value='Normal Room Temperatures'>Normal Room Temperatures</option>" +
                   "<option value='Warm Temperatures'>Warm Temperatures</option>" +
                   "<option value='Cool Temperatures'>Cool Temperatures</option>" +
                   "<option value='Cold Temperatures'>Cold Temperatures</option>" +
                   form_end);

    } else if (tableCol === 'image'){
      $('#edit-img-url-field').append("<form class='form-inline col-sm-4'>"+
                     "<div class='form-group new-edit-input-field'>"+
                     "<input type='text' placeholder='Enter URL' class='form-control' id='new_edit'></div>" +
                     "<input type='submit' class='btn btn-default' id='submit-edit-btn'>"+
                     "</form>");
    } else {
      $(this).html("<form class='form-inline'>" +
                   "<div class='form-group new-edit-input-field'> " +
                   "<input type='text' class='form-control' id='new_edit'>" +
                   "<input type='submit' class='btn btn-default' id='submit-edit-btn'>"+
                   "</div></form>");
    }

    // on submit of edits calls submitEdit function and passes in plant id and column edited
    $('#submit-edit-btn').click(function(){ return submitEdit(plantId, tableCol); });
  }

  // on click of add specs button, call startEdit function
  $('.edit-btn').click(startEdit);

}(jQuery);



