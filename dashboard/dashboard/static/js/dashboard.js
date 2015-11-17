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
        dataset: 'some link'
    }, {
        name: 'Crime 2',
        dataset: 'some link'
    }, {
        name: 'Crime 3',
        dataset: 'some link'
    }, {
        name: 'Crime 4',
        dataset: 'some link'
    }, {
        name: 'Crime 5',
        dataset: 'some link'
    }, {
        name: 'Crime 6',
        dataset: 'some link'
    }, {
        name: 'Crime 7',
        dataset: 'some link'
    }, {
        name: 'Crime 8',
        dataset: 'some link'
    }, {
        name: 'Crime 9',
        dataset: 'some link'
    }];

    $scope.sortableOptions = {

    };
    
});
