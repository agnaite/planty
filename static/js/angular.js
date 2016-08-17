 var planty = angular.module('planty', []);

  planty.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});

planty.controller('addPlantController', function($scope, $http) {
  $scope.click = function(userId, plantId) {
    // check if removing or adding based on some scope variable
    var ids = { 'plant': plantId,
                'user': userId
    };
    console.log(ids);

    var response = $http.post('/add_plantuser', ids).then();

    console.log(response);
  };
});

// planty.controller('userPlantsCtrl', function($scope, $http, $location) {

//   $scope.getUserPlants = function(userId) {
//     $http.get('/user_plants/' + userId)
//       .success(function(data) {
//         $location.url('user_plants.html');
//         $scope.userPlants = data;
//       });
//     };
// });

