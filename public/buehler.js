angular.module('buehlerApp', []).controller ('buehlerController', ['$scope', '$http', function ($scope, $http) {    
    $scope.getResult = function() {
        $scope.gettingResult = true;
        $http.get('http://localhost:5000/result').then(function(response){
            $scope.result = response.data;
            console.log($scope.result);
            $scope.gettingResult = false;
        });
        $('#sample').mousemove(function(e){
            console.log(e.pageX - this.offsetLeft);
            console.log(e.pageY - this.offsetTop);
        }); 
    });
    };
    $scope.getResult();
}]).filter('percentage', ['$filter', function ($filter) {
  return function (input, decimals) {
    return $filter('number')(input * 100, decimals) + '%';
  };
}]);