// CONFIG ***************************************************************

(function(angular) {
  'use strict';

var app = angular.module('planty', ['ngRoute']);

app.config(function($routeProvider, $interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');

  $routeProvider
    .when('/', {
      templateUrl: 'index.html',
      controller: 'homeCtrl'
    })
    .when('/new_plant', {
      templateUrl: 'new_plant_form.html',
      controller: 'addPlantCtrl'
    });
});

// SEARCH ***************************************************************

app.controller('homeCtrl', function($scope, $http, $location) {
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

app.controller('addUserCtrl', function($scope, $http, $window) {
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
        $window.location.href = '/user_profile/' + data;
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

  //$scope.reset();
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
        $window.location.href = '/plant/' + data;
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