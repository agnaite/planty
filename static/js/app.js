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
    $http.get('/search/?search=' + $scope.searchText)
      .then(function(results){
        // if server sends back none string, send empty string to view
        // else, send dictionary of plant objects to view
        if (results.data === 'None') {
          $scope.foundPlants = '';
        } else {
          $scope.foundPlants = results.data;
          console.log($scope.foundPlants);
        }
      });
  };
});

// ADD PLANT ***************************************************************

app.controller('addPlantCtrl', function($scope, $http, $location) {
  $scope.master = {};

  $scope.update = function(plant) {
    $scope.master = angular.copy(plant);
    console.log($scope.master);
  };

  $scope.reset = function() {
    $scope.plant = angular.copy($scope.master);
  };

  $scope.reset();
});

})(window.angular);