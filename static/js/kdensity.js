/**
 * Created by manikandan.nagarajan on 7/16/16.
 */
var app = angular.module('kdensityApp', [])
app.controller('KernelDensityController', function($scope, $http) {
    
    $scope.submitForm = function() {
        $scope.loading = true;
        console.log("submit called in kernel density")
        console.log("new-name::", $scope.name)
        console.log("new-bandwidth::", $scope.bandwidth)
        console.log("new-points::", $scope.points)
        var url = "http://localhost:5000/kdensity"
        var input = new Object();
        input.column = $scope.name
        input.bandwidth = $scope.bandwidth
        input.points = $scope.points
        $http.post(url, JSON.stringify(input)).success(function (response) {
            $scope.loading = false;
            console.log("response::", response)
            console.log("response::", response.message)
            var resultsUrl = "http://localhost:5000/kdensity/result"
            window.location = resultsUrl
        })
    }
});