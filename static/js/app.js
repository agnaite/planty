var app = angular.module('planty', ['ngRoute']);

app.config(function($routeProvider, $interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');

  $routeProvider
    .when('/', {
      templateUrl: 'index.html',
      controller: 'homeCtrl'
    });
});

app.controller('homeCtrl', function($scope, $http, $location) {
  $scope.searchSubmit = function() {
    $http.get('/search/?search=' + $scope.searchText)
      .then(function(results){
        if (results.data === 'None') {
          $scope.foundPlants = '';
        } else {
          $scope.foundPlants = results.data;
          console.log($scope.foundPlants);
        }
      });
    //console.log($scope.searchText);
  };
});
