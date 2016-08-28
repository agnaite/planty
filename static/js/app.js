// CONFIG ***************************************************************

(function(angular) {
  'use strict';

require('bootstrap');
require('angular-route');
require('angular-cookies');
require('sweetalert');

var app = angular.module('planty', ['ngRoute', 'ngCookies']);
var flash = require('./flash');

app.config(function($routeProvider, $interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');

  $routeProvider
    .when('/', {
      templateUrl: '/html_for_angular/search.html',
      controller: 'homeCtrl'
    })
    .when('/add_plant', {
      templateUrl: '/html_for_angular/add_plant.html',
      controller: 'addPlantCtrl'
    })
    .when('/plant/:plantId', {
      templateUrl: '/html_for_angular/plant.html',
      controller: 'viewPlantCtrl'
    })
    .when('/login', {
      templateUrl: '/html_for_angular/login.html',
      controller: 'userCtrl'
    })
    .when('/register', {
      templateUrl: '/html_for_angular/register.html',
      controller: 'addUserCtrl'
    })
    .when('/user/:userId', {
      templateUrl: '/html_for_angular/user.html',
      controller: 'userProfileCtrl'
    });
});

// LOGOUT &
// LOGIN ***************************************************************

app.controller('userCtrl', function($scope, $http, $location, $route, $routeParams, $rootScope, $cookies) {
    // Verifies credentials via Flask in db and sets js cookie to logged in
    $scope.submitLogin = function() {
    $http ({
      url: '/process_login',
      method: "POST",
      data: $.param($scope.user),
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    }).then(function(response) {
      // on 200 status from Flask, redirect to the new plant's page
      if (response.data === 'error') {
        $location.path('/login');
        flash('Could not log you in. Please try again.');
      } else {
        $cookies.put('logged_in', response.data['logged_in']);
        $location.path('/');
        flash('Welcome back, ' + $scope.user.username + '!');
      }
    });
  };

  // Checks if a user is currently logged in
  $scope.isLoggedIn = function() {
    return $cookies.get('logged_in');
  };

  // Removes user_id from cookie and from from flask session
  $scope.logout = function() {
    $cookies.put('logged_in', undefined);

    $http.get('/process_logout')
    .then(function(results) {
      $scope.username = '';
      $scope.password = '';
      $location.path('/');
      flash("Bye, see you soon.");
    });
  };
});

// SEARCH ***************************************************************

app.controller('homeCtrl', function($scope, $http, $location, $routeParams) {
  
  // gets the binded input data and sends the user entered text to the server
  $scope.searchSubmit = function() {
    $http.get('/search/' + $scope.searchText)
    .then(function(results){
      // if server sends back none string, send empty string to view
      // else, send dictionary of plant objects to view
      if (results.data === 'None') {
        $scope.foundPlants = '';
      } else {
        $scope.foundPlants = results.data;
      }
    });
  };
});

// USER  ***************************************************************

app.controller('addUserCtrl', function($scope, $http, $route, $location) {
  $scope.master = {};

  // on register button click, send user filled data to Flask 
  $scope.update = function(user) {
    $scope.master = angular.copy(user);
     $http({
      url: '/process_registration',
      method: "POST",
      data: $.param(user),
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
     }).success(function(data) {
        // on 200 status from Flask, redirect to the new user's page
        $location.path('/user/' + data);
        $route.reload();
        flash("Welcome to Planty, " + user.name);
    });
  };

  // on click of reset button, clear all form fields and set to untouched
  $scope.reset = function() {
    $scope.user = angular.copy($scope.master);
    $scope.form.$setUntouched();
    $scope.user.email = '';
    $scope.user.image = '';
    $scope.user.username = '';
  };
});

app.controller('userProfileCtrl', function($scope, $http, $route, $location, $routeParams) {
  var user_id = $routeParams.userId;
  $scope.days = new Set();
  loadUserPage();

  function loadUserPage() {
    $http.get('/user/' + user_id)
    .then(function(response) {
      $scope.user = response.data;
      if ($scope.user.image === '') {
        $scope.user.image='static/img/user_placeholder.jpg';
      }
      $scope.userPlantNum = Object.keys($scope.user.plants).length;
    });
  }

  // Reminders ****************************** 

  $scope.addDay = function(day) {
    $scope.days.add(day);
  };

  // sends plant data to Flask for removal from db
  $scope.addReminder = function(plant_id) {
    $scope.reminderId = plant_id;
    $('#myModal').modal();
  };

  $scope.submitReminder = function($event) {
    var daysData = {'days': '',
                    'plant_id': $scope.reminderId,
                    'user_id': $scope.isLoggedIn()
                   };

    $scope.days.forEach(function(day) {
      daysData['days'] += day;
    });
    console.log(daysData);
    $http({
      url: '/process_new_reminder',
      method: "POST",
      data: $.param(daysData),
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
     }).success(function(data) {
        // on 200 status from Flask, redirect to the new plant's page
        flash("Reminder has been added!");
    });
    loadUserPage();
    $scope.days = new Set();
    clearModal();

  };

  $scope.removeReminder = function(plant_id) {
    $scope.reminderId = plant_id;
    var data = {'plant_id': $scope.reminderId,
                'user_id': $scope.isLoggedIn()
                };
    $http({
      url: '/delete_reminder',
      method: "POST",
      data: $.param(data),
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
     }).success(function(data) {
        // on 200 status from Flask, redirect to the new plant's page
        loadUserPage();
        flash("Reminder has been removed!");
    });
  };

  $scope.cancelReminder = function() {
    $scope.days = new Set();
    clearModal();
    console.log($scope.days);
  };

  function clearModal() {
    $('#myModal').on('hidden.bs.modal', function (e) {
      $(this)
        .find("input[type=checkbox]")
           .prop("checked", "")
           .end();
    });
  }
});
// ADD PLANT ***************************************************************

app.controller('addPlantCtrl', function($scope, $http, $location, $route, getPlantSpecsService) {
  $scope.master = {};

  // on add plant button click, send user filled data to Flask 
  $scope.update = function(plant) {
    $scope.master = angular.copy(plant);
     $http({
      url: '/process_new_plant',
      method: "POST",
      data: $.param(plant),
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
     }).success(function(data) {
        // on 200 status from Flask, redirect to the new plant's page
        $location.path('/plant/' + data);
        $route.reload();
        flash(plant.name + " has been added!");
    });
  };

  // on click of reset button, clear all form fields
  $scope.reset = function() {
    $scope.plant = angular.copy($scope.master);
    $scope.form.$setUntouched();
    $scope.plant.name = '';
  };

  // get flickr image url on click of button from Flask
  $scope.getFlickrImg = function() {
    $http.get('/get_flickr_img/' + $scope.plant.name)
    .success(function(data) {
      $scope.plant.image = data;
    });
  };

  // gets all the plant spec data from json files via getPlantSpecs Service
  getPlantSpecsService.getWater(function(response) {
    $scope.water = response.data;
  });
  getPlantSpecsService.getSun(function(response) {
    $scope._sun = response.data;
  });
  getPlantSpecsService.getHumidity(function(response) {
    $scope.humidity = response.data;
  });
  getPlantSpecsService.getTemp(function(response) {
    $scope.temp = response.data;
  });

});

// PLANT VIEW ***************************************************************

app.controller('viewPlantCtrl', function($http,
                                         $scope,
                                         $routeParams,
                                         $route,
                                         $location,
                                         $timeout,
                                         getPlantSpecsService) {
  // gets plant_id from link clicked on and gets all the data about that plant from Flask
  var plant_id = $routeParams.plantId;

  // gets data about plant specs for easy in-place editing
  $http.get('/plant/' + plant_id)
  .then(function(response) {
    $scope.plant = response.data;
    $scope.plant.edited = false;
    $scope.userHasPlant();

    getPlantSpecsService.getHumidity(function(response) {
      $scope.allHumid = response.data;
      $scope.humidity = response.data[$scope.plant.humidity];
    });

    getPlantSpecsService.getTemp(function(response) {
      $scope.allTemp = response.data;
      $scope.temperature = response.data[$scope.plant.temperature];
    });

    getPlantSpecsService.getSun(function(response) {
      $scope.allSun = response.data;
      $scope.sun = response.data[$scope.plant.sun];
    });

    getPlantSpecsService.getWater(function(response) {
      $scope.allWater = response.data;
      $scope.water = response.data[$scope.plant.water];
    });

  });


  // on click of the save button, sends all the data in the fields to flask to update db
  $scope.saveEdits = function() {
    $scope.plant.edited = false;

    $http({
      url: '/save_plant_edits',
      method: "POST",
      data: $.param($scope.plant),
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
     }).success(function(data) {
        // on 200 status from Flask, redirect to the new plant's page
        flash("Saved!");
    });
  };

  // sends plant data to Flask for removal from db
  $scope.deletePlant = function() {
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
              $http({
                url: '/process_delete',
                method: "POST",
                data: $.param($scope.plant),
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
              }).then(function(data) {
                  // on 200 status from Flask, redirect to the new plants page
                  $location.path('/');
                  $route.reload();
                  flash("Plant deleted.");
                });
              }
      });
  };

  // adds plant to logged in user
  $scope.addUserPlant = function() {
    var data = {
      'userId': $scope.isLoggedIn(),
      'plantId': $scope.plant.plant_id
    };
    $scope.plantUserStatus = true;

    $http({
      url: '/add_user_plant',
      method: 'POST',
      data: $.param(data),
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    }).then(function(response) {
      $scope.userHasPlant();
      flash("Plant added!");
    });
  };

  // removes plant from logged in user
  $scope.removeUserPlant = function() {
    var data = {
      'userId': $scope.isLoggedIn(),
      'plantId': $scope.plant.plant_id
    };
    $scope.plantUserStatus = false;

    $http({
      url: '/remove_user_plant',
      method: 'POST',
      data: $.param(data),
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    }).then(function(response) {
      $scope.userHasPlant();
      flash("Plant removed. ");
    });
  };

  // asks flask if logged in user has already added the plant 
  $scope.userHasPlant = function(){
     var data = {
        'userId': $scope.isLoggedIn(),
        'plantId': plant_id
      };

    $http({
        url: '/is_plant_user',
        method: 'POST',
        data: $.param(data),
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      }).then(function(response) {
        if (response.data == 'true') {
          $scope.plantUserStatus = true;
        } else {
          $scope.plantUserStatus = false;
        }
    });
  };
});

// gets plant spec data from JSON
app.service('getPlantSpecsService', function($http){
  // gets plant specs out of json files

  this.getWater = function(callback){
    $http.get('/static/data/specs/water_specs.json')
    .then(callback);
  };
  this.getHumidity = function(callback){
    $http.get('/static/data/specs/humidity_specs.json')
    .then(callback);
  };
  this.getSun = function(callback){
    $http.get('/static/data/specs/sun_specs.json')
    .then(callback);
  };
  this.getTemp = function(callback){
    $http.get('/static/data/specs/temp_specs.json')
    .then(callback);
  };
});

})(window.angular);