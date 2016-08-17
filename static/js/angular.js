 var planty = angular.module('planty', []);

  planty.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
  });


  planty.controller('addPlantController', function($scope, $http) {
    $scope.click = function(userId, plantId) {

      var ids = { 'plant': plantId,
                  'user': userId
      };
      console.log(ids);

      var response = $http.post('/add_plantuser', ids);

      console.log(response);

    };

  });