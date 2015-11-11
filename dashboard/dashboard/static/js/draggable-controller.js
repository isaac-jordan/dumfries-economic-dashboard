/*jshint*/
/* global app */
'use strict';

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
  }];

  $scope.sortableOptions = {
    
  };
});