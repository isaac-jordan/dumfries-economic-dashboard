/*jshint*/
/*global angular, drawGraph, console, alert, prompt */
'use strict';

var app = angular.module('dashboard', ['ngRoute', 'gridster']);
var GLOBAL = {};

app.run(function($rootScope, $templateCache) {
    $rootScope.$on('$routeChangeStart', function(event, next, current) {
        if (typeof(current) !== 'undefined'){
            $templateCache.remove(current.templateUrl);
        }
    });
});

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
                templateUrl : 'pages/savedConfigs'
            })

            .when('/register', {
                templateUrl : 'pages/register'
            });
    });

// create the controller and inject Angular's $scope
app.controller('mainController', function($scope) {
    $scope.widgets = GLOBAL.widgets;
    $scope.message = 'Welcome to the Dumfries Dashboard!';
    
    $scope.saveConfig = function() {
        var widgets = GLOBAL.widgets,
            data = [];
        $.ajax({
            type:"GET",
            url: '/account/checkAuthenticated',
            success: function(response){
                if (!response.is_authenticated) {
                    alert("Please log in first.");
                    return;
                }
                var name = prompt("Enter a name for the config: ");
                if (!name) return;
                for (var i=0; i<widgets.length; i++) {
                    var object = {};
                    object.visPK = widgets[i].pk;
                    object.xPosition = widgets[i].col;
                    object.yPosition = widgets[i].row;
                    object.sizeX = widgets[i].sizeX;
                    object.sizeY = widgets[i].sizeY;
                    data.push(object);
                }
                console.log(data);
                $.ajax({
                    type:"POST",
                    url: '/saveConfig',
                    data: {data: JSON.stringify(data), name: name},
                    success: function(response){
                        alert(response.message);
                    },
                    error: function(err) {
                        console.log(err);
                    }
                });
            }
        });
        
    };
});

app.controller('aboutController', function($scope) {
    $scope.message = 'Look! I am an about page.';
});

app.controller('savedConfigController', function($scope, $route) {
    $scope.deleteSavedConfig = function(id) {
        $.ajax({
            type:"POST",
            url: '/deleteSavedConfig',
            data: {id: id},
            success: function(response){
                if (response.success)
                    $route.reload();
                else
                    alert(response.message);
            },
            error: function(err) {
                console.log(err);
            }
        });
    };
    
    $scope.loadSavedConfig = function(id) {
        $.ajax({
            type:"POST",
            url: '/loadSavedConfig',
            data: {id: id},
            success: function(response){
                console.log(response);
                GLOBAL.widgets = response.widgets;
                var el = $("#config"+id);
                console.log(el);
                el.removeClass("glyphicon-import");
                el.addClass("glyphicon-saved");
                el.addClass("icon-success");
                setTimeout(function() {
                    el.removeClass("glyphicon-saved");
                    el.removeClass("icon-success");
                    el.addClass("glyphicon-import");
                }, 1000);
            },
            error: function(err) {
                console.log(err);
            }
        });
    };
});

app.controller('draggableGridController', function ($scope) {
    $scope.widgets = GLOBAL.widgets;
    $scope.drawGraph = drawGraph;
    $scope.drawAllGraphs = function () {
        if (!$scope.widgets) return;
        for(var i=0; i < $scope.widgets.length; i++) {
            drawGraph($scope.widgets[i].id, $scope.widgets[i].dataset, $scope.widgets[i].type);
        }
    };
    
    $scope.clear = function() {
        $scope.widgets.splice(0, $scope.widgets.length);
    };
    
    $scope.deleteWidget = function(index) {
        $scope.widgets.splice(index, 1);
    };
    
    if (!GLOBAL.widgets) {
        $.ajax({
            type:"GET",
            url: '/getGraphs',
            success: function(response){
                GLOBAL.widgets = response.widgets;
                $scope.widgets = GLOBAL.widgets;
                $scope.$apply();
            },
            error: function(err) {
                console.log(err);
            }
        });
    }
    
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
    
    $scope.$on('gridster-item-transition-end', function(item) {
        console.log(item);
    });
    
    $scope.$on('gridster-item-initialized', function(item) {
        console.log(item);
    });
    
    $scope.$watch('widgets', function(items){
        //$scope.drawAllGraphs();
    }, true);
    
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

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});
