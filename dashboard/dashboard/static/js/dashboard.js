/*jshint*/
/*global angular, drawGraph, console */
'use strict';

var app = angular.module('dashboard', ['ngRoute', 'gridster']);
var GLOBAL = {};

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
            
            .when('/savedconfigs', {
                templateUrl : 'pages/savedConfigs',
                controller  : 'savedConfigController'
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

app.controller('savedConfigController', function($scope, $route) {
    
});

app.controller('draggableGridController', function ($scope) {
    $scope.widgets = GLOBAL.widgets;
    $scope.drawGraph = drawGraph;
    
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

    $scope.clear = function() {
        $scope.widgets.splice(0, $scope.widgets.length);
    };
    
    $scope.deleteWidget = function(index) {
        $scope.widgets.splice(index, 1);
    };
    
});

function logoutUser() {
    $.ajax({
    type:"POST",
    url: '/account/login',
    data: $('#login_form').serialize(),
    success: function(response){
        $("#message").html();
     }
});
}
