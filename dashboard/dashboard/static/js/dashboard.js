/*jshint*/
/*global angular, drawGraph, console */
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
    
    $scope.message = 'Welcome to the Dumfries Dashboard!';
});

app.controller('aboutController', function($scope) {
    $scope.message = 'Look! I am an about page.';
});

app.controller('contactController', function($scope) {
    $scope.message = 'Contact us! JK. This is just a demo.';
});

app.controller('draggableGridController', function ($scope) {
    $scope.widgets = [{
        name: 'Crime',
        type: "bar",
        id: "crime",
        dataset: [32,13,45,13,12],
        sizeX: 2,
        sizeY: 1
    }, {
        name: 'Employment Nature',
        type: "bar",
        id: "employment-nature",
        dataset: [5,3,8,3],
        sizeX: 2,
        sizeY: 1
    }, {
        name: 'Unemployment',
        type: "bar",
        id: "unemployment",
        dataset: [4, 8, 15, 16, 23, 42],
        sizeX: 2,
        sizeY: 1
    }, {
        name: 'GDP Per Head (£)',
        type: "line",
        id: "gdp",
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
        sizeX: 2,
        sizeY: 2
    }, {
        name: 'Employment Rate',
        type: "line",
        id: "employment-rate",
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
        sizeX: 2,
        sizeY: 2
    }, {
        name: 'Claimant Count Numbers',
        type: "bar",
        id: "claimant",
        dataset: [4, 8, 15, 16, 23, 42],
        sizeX: 2,
        sizeY: 1
    },{
        name: 'House Prices (£1000)',
        type: "line",
        id: "house-prices",
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
        sizeX: 2,
        sizeY: 2
    }];
    
    $scope.gridsterOpts = {
        margins: [20, 20],
        outerMargin: false,
        draggable: {
            enabled: true,
            start: function(event, $element, widget) {
                // optional callback fired when drag is started
                // use this to try to stop lag
            }, 
            stop: function(event, $element, widget) {
                // optional callback fired when item is finished dragging
                // use this to try to stop lag
            } 
        },
        resizable: {
            enabled: false
        },
        swapping: true, // whether or not to have items of the same size switch places instead of pushing down if they are the same size
        width: 'auto', // can be an integer or 'auto'. 'auto' scales gridster to be the full width of its containing element
        colWidth: 'auto', // can be an integer or 'auto'.  'auto' uses the pixel width of the element divided by 'columns'
        rowHeight: 'match',
        floating: true
    };

    
    $scope.drawGraph = drawGraph;
    
});