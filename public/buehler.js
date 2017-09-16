angular.module('buehlerApp', []).controller ('buehlerController', ['$scope', '$http', function ($scope, $http) {    
     $scope.gettingResult = true;
    $scope.currentContamination = "clean";
    $scope.getResult = function() {
        $scope.gettingResult = true;
        $http.get('/result').then(function(response){
            $scope.result = response.data;
            console.log($scope.result);
            $scope.gettingResult = false;
        });
        $('#sample').mousemove(function(e){
            //console.log(e.pageX - this.offsetLeft);
            //console.log(e.pageY - this.offsetTop);
            mouseX = e.pageX - this.offsetLeft;
            mouseY = e.pageY - this.offsetTop;
            sizing = $scope.result.slicing.size;
            $.each($scope.result.slices, function(i, slice){
                if(mouseX >= slice.x && mouseX < (slice.x + sizing) && mouseY >= slice.y && mouseY < slice.y + sizing) {
                    $scope.currentContamination = slice.category;
                    $scope.$apply();
                }
            })
        }); 
    };
    $scope.getResult();
}]).filter('percentage', ['$filter', function ($filter) {
  return function (input, decimals) {
    return $filter('number')(input * 100, decimals) + '%';
  };
}]).filter('contamination', ['$filter', function ($filter) {
  return function (input, decimals) {
    return $filter('number')(input * 100, decimals) + '%';
  };
}]);