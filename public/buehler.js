angular.module('buehlerApp', []).controller ('buehlerController', ['$scope', '$http', function ($scope, $http) {
  $http.get('http://localhost:5000/result').then(function(response){
        $scope.result = response.data;
    });
}]);