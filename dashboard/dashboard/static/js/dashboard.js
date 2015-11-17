/*jshint*/
/*global angular, drawGraph1 */
'use strict';

var app = angular.module('dashboard', ['ngRoute', 'as.sortable']);

app.config(function($routeProvider) {
        $routeProvider
            // route for the home page
            .when('/', {
                templateUrl : 'pages/home',
                controller  : 'mainController'
            })

            // route for the about page
            .when('/about', {
                templateUrl : 'pages/about',
                controller  : 'aboutController'
            })

            // route for the contact page
            .when('/contact', {
                templateUrl : 'pages/contact',
                controller  : 'contactController'
            });
    });

// create the controller and inject Angular's $scope
app.controller('mainController', function($scope) {
    // create a message to display in our view
    
    $scope.message = 'Everyone come and see how good I look!';
});

app.controller('aboutController', function($scope) {
    $scope.message = 'Look! I am an about page.';
});

app.controller('contactController', function($scope) {
    $scope.message = 'Contact us! JK. This is just a demo.';
});

app.controller('draggableGridController', function ($scope) {
    $scope.items = [{
        name: 'Crime 1',
        id: "crime1",
        dataset: [5,3,8,3]
    }, {
        name: 'Crime 2',
        id: "crime2",
        dataset: [4, 8, 15, 16, 23, 42]
    }, {
        name: 'Crime 3',
        id: "crime3",
        dataset: [4, 8, 15, 16, 23, 42]
    }, {
        name: 'Crime 4',
        id: "crime4",
        dataset: [4, 8, 15, 16, 23, 42]
    }, {
        name: 'Crime 5',
        id: "crime5",
        dataset: [4, 8, 15, 16, 23, 42]
    }, {
        name: 'Crime 6',
        id: "crime6",
        dataset: [4, 8, 15, 16, 23, 42]
    }, {
        name: 'Crime 7',
        id: "crime7",
        dataset: [4, 8, 15, 16, 23, 42]
    }, {
        name: 'Crime 8',
        id: "crime8",
        dataset: [4, 8, 15, 16, 23, 42]
    }, {
        name: 'Crime 9',
        id: "crime9",
        dataset: [4, 8, 15, 16, 23, 42]
    }];

    $scope.sortableOptions = {

    };
    
    $scope.drawGraphOne = function(id, data) { drawGraph1(id, data); };
    
});
