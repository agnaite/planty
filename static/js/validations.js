angular.module("planty")

// Is plant name unique ********************************************************
  .directive('plantName', function($q, $timeout, $http) {
  return {
    require: 'ngModel',
    link: function(scope, elm, attrs, ctrl) {

      ctrl.$asyncValidators.plantName = function(modelValue, viewValue) {

        if (ctrl.$isEmpty(modelValue)) {
          // consider empty model valid
          return $q.when();
        }
        var def = $q.defer();

        $timeout(function() {
          // Mock a delayed response
            $http.get('/is_plant/'+ modelValue)
              .then(function(results) {
                if (results.data == 'False') {
                  def.resolve();
                } else {
                  def.reject();
                }
            });
        }, 500);
        return def.promise;
      };
    }
  };
})

// Does URL endwith .jpg or .png ***********************************************
.directive('imgUrl', function($q, $timeout, $http) {
  return {
    require: 'ngModel',
    link: function(scope, elm, attrs, ctrl) {

      ctrl.$asyncValidators.imgUrl = function(modelValue, viewValue) {

        if (ctrl.$isEmpty(modelValue)) {
          // consider empty model valid
          return $q.when();
        }

        var def = $q.defer();

        $timeout(function() {
          // Mock a delayed response

          if (modelValue.toLowerCase().endsWith('.jpg')  ||
              modelValue.toLowerCase().endsWith('.jpeg') ||
              modelValue.toLowerCase().endsWith('.png')) {
            def.resolve();
          } else {
            def.reject();
          }

        }, 500);

        return def.promise;
      };
    }
  };
})

// Is username taken ***********************************************
.directive('username', function($q, $timeout, $http) {
  return {
    require: 'ngModel',
    link: function(scope, elm, attrs, ctrl) {

      ctrl.$asyncValidators.username = function(modelValue, viewValue) {

        if (ctrl.$isEmpty(modelValue)) {
          // consider empty model valid
          return $q.when();
        }

        var def = $q.defer();

        $timeout(function() {
          // Mock a delayed response

          $http.get('/is_username/' + modelValue)
              .then(function(results) {
                if (results.data == 'False') {
                  def.resolve();
                } else {
                  def.reject();
                }
            });
        }, 500);

        return def.promise;
      };
    }
  };
})

// Is valid phone number ***********************************************
.directive('phone', function($q, $timeout, $http) {
  return {
    require: 'ngModel',
    link: function(scope, elm, attrs, ctrl) {

      ctrl.$asyncValidators.phone = function(modelValue, viewValue) {

        if (ctrl.$isEmpty(modelValue)) {
          // consider empty model valid
          return $q.when();
        }

        var def = $q.defer();

        $timeout(function() {
          // Mock a delayed response

          if ((modelValue.length == 10) && (/^[0-9]+$/.test(modelValue))) {
            def.resolve();
          } else {
            def.reject();
          }
        }, 500);

        return def.promise;
      };
    }
  };
})

// Is email in use ***********************************************

.directive('email', function($q, $timeout, $http) {
  return {
    require: 'ngModel',
    link: function(scope, elm, attrs, ctrl) {

      ctrl.$asyncValidators.email = function(modelValue, viewValue) {

        if (ctrl.$isEmpty(modelValue)) {
          // consider empty model valid
          return $q.when();
        }

        var def = $q.defer();

        $timeout(function() {
          // Mock a delayed response

          $http.get('/is_email/' + modelValue)
              .then(function(results) {
                if (results.data == 'False') {
                  def.resolve();
                } else {
                  def.reject();
                }
            });
        }, 500);

        return def.promise;
      };
    }
  };
});