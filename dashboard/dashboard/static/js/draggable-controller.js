/*jshint*/
/*global app */

app.controller('AppController', [
    '$scope',
    function ( $scope) {
        $scope.sortableList = [
            {
                id : "graph-000",
                title : "Crime 000"
            },
            {
                id : "graph-001",
                title : "Crime 001"
            },
            {
                id : "graph-002",
                title : "Employment 000"
            },
            {
                id : "graph-003",
                title : "Employment 001"
            },
            {
                id : "graph-004",
                title : "Employment 002"
            },
            {
                id : "graph-005",
                title : "Employment 003"
            },
            {
                id : "graph-006",
                title : "Crime 002"
            }

        ];

    }
]);