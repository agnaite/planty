// CONFIG ***************************************************************

(function(angular) {
  'use strict';

var app = angular.module('planty', ['ngRoute', 'ngCookies']);

app.config(function($routeProvider, $interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');

  $routeProvider
    .when('/', {
      templateUrl: '/html_for_angular/search.html',
      controller: 'homeCtrl'
    })
    .when('/add_plant', {
      templateUrl: '/html_for_angular/new_plant_form.html',
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
    });
});


// LOGOUT &
// LOGIN ***************************************************************


app.controller('userCtrl', function($scope, $http, $location, $route, $routeParams, $rootScope, $cookies) {

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
        console.log(response.data);
        $cookies.put('logged_in', response.data['logged_in']);
        $location.path('/');
        flash('Welcome back, ' + $scope.user.username + '!');
      }
    });
  };

  $scope.isLoggedIn = function() {
    return $cookies.get('logged_in');
  };

  $scope.logout = function() {

    $cookies.put('logged_in', undefined);

    // TODO: actually invalidate session with flask
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

// NEW USER  ***************************************************************

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

// ADD PLANT ***************************************************************

app.controller('addPlantCtrl', function($scope, $http, $location, $window, getPlantSpecsService) {
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

app.controller('viewPlantCtrl', function($http, $scope, $routeParams, getPlantSpecsService, $route, $location) {
  var plant_id = $routeParams.plantId;

  $scope.editing = false;

  $http.get('/plant/' + plant_id)
  .then(function(response) {
    $scope.plant = response.data;
    $scope.plant.edited = false;

    getPlantSpecsService.getHumidity(function(response) {
      $scope.allHumid = response.data;
      $scope.humid = response.data[$scope.plant.humidity];
    });

    getPlantSpecsService.getTemp(function(response) {
      $scope.allTemp = response.data;
      $scope.temp = response.data[$scope.plant.temperature];
    });

    getPlantSpecsService.getSun(function(response) {
      $scope.allSun = response.data;
      $scope.sun = response.data[$scope.plant.sun];
    });

    getPlantSpecsService.getWater(function(response) {
      $scope.allWater = response.data;
      $scope.plant.water = response.data[$scope.plant.water];
    });

    if ($scope.plant["image"] === null) {
      $scope.plant["image"] = "/static/img/placeholder-image.png";
    }
  });

  $scope.saveEdits = function(editedPlant) {
    $scope.plant.edited = false;
    $http({
      url: '/save_plant_edits',
      method: "POST",
      data: $.param(editedPlant),
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
     }).success(function(data) {
        // on 200 status from Flask, redirect to the new plant's page
        flash("Saved!");
    });
  };

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
                  // on 200 status from Flask, redirect to the new plant's page
                  $location.path('/');
                  $route.reload();
                  flash("Plant deleted.");
                });
              }
      });
  };
});

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