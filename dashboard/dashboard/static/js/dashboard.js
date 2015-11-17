/*jshint*/
/*global angular, drawGraph */
'use strict';

var app = angular.module('dashboard', ['ngRoute', 'gridster']);

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
    $scope.widgets = [{
        name: 'Crime 1',
        type: "bar",
        id: "crime1",
        dataset: [5,3,8,3],
        size: {
            x: 1,
            y: 1
        },
        position: [0, 0]
    }, {
        name: 'Crime 2',
        type: "bar",
        id: "crime2",
        dataset: [4, 8, 15, 16, 23, 42],
        size: {
            x: 1,
            y: 1
        },
        position: [0, 1]
    }, {
        name: 'Crime 3',
        type: "bar",
        id: "crime3",
        dataset: [4, 8, 15, 16, 23, 42],
        size: {
            x: 1,
            y: 1
        },
        position: [0, 2]
    }, {
        name: 'Crime 4',
        type: "bar",
        id: "crime4",
        dataset: [4, 8, 15, 16, 23, 42],
        size: {
            x: 1,
            y: 1
        },
        position: [1, 0]
    }, {
        name: 'Crime 5',
        type: "bar",
        id: "crime5",
        dataset: [4, 8, 15, 16, 23, 42],
        size: {
            x: 1,
            y: 1
        },
        position: [1, 1]
    }, {
        name: 'Crime 6',
        type: "bar",
        id: "crime6",
        dataset: [4, 8, 15, 16, 23, 42],
        size: {
            x: 1,
            y: 1
        },
        position: [1, 2]
    }, {
        name: 'Crime 7',
        type: "bar",
        id: "crime7",
        dataset: [4, 8, 15, 16, 23, 42],
        size: {
            x: 1,
            y: 1
        },
        position: [2, 0]
    }, {
        name: 'Crime 8',
        type: "bar",
        id: "crime8",
        dataset: [4, 8, 15, 16, 23, 42],
        size: {
            x: 1,
            y: 1
        },
        position: [2, 1]
    }, {
        name: 'Crime 9',
        type: "line",
        id: "crime9",
        dataset: [{
                y: "152",
                x: "2000"
            }, {
                y: "189",
                x: "2002"
            }, {
                y: "179",
                x: "2004"
            }, {
                y: "199",
                x: "2006"
            }, {
                y: "134",
                x: "2008"
            }, {
                y: "176",
                x: "2010"
            }],
        size: {
            x: 1,
            y: 2
        },
        position: [2, 2]
    }];
    
    $scope.gridsterOpts = {
        margins: [20, 20],
        outerMargin: false,
        draggable: {
            enabled: true
        },
        resizable: {
            enabled: false
        },
        swapping: true, // whether or not to have items of the same size switch places instead of pushing down if they are the same size
        width: 'auto', // can be an integer or 'auto'. 'auto' scales gridster to be the full width of its containing element
        colWidth: 'auto', // can be an integer or 'auto'.  'auto' uses the pixel width of the element divided by 'columns'
        rowHeight: 'match',
    };

    
    $scope.drawGraph = drawGraph;
    
});