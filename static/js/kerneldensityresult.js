/**
 * Created by manikandan.nagarajan on 7/17/16.
 */
var app = angular.module('kdensityResultApp', [])
app.controller('KernelDensityResultController', function($scope, $http) {

    console.log("get_results - kernel denisty")

    var url = "http://localhost:5000/kdensity/result"
    var input = new Object();
    $http.post(url, JSON.stringify(input)).success(function (response) {
        $scope.results = response.results
        $scope.points = response.estimationPoints

        console.log("results::", $scope.results)
        console.log("points::", $scope.points)
        console.log("result in kdensity::", response)

        new Chartist.Line('.ct-chart', {
            labels: response.estimationPoints,
            series: [response.results]
        }, {
            fullWidth: true,
            chartPadding: {
                right: 40
            }
        });

    })

});
