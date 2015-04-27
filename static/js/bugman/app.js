var app = angular.module('BugmanApp', ['ngRoute'])
.config(function($interpolateProvider) {
        $interpolateProvider.startSymbol('{$');
        $interpolateProvider.endSymbol('$}');
    })
.config(function($routeProvider) {
    $routeProvider
        .when('/', {
            templateUrl: '/static/js/bugman/templates/projects.html',
            controller: 'ProjectsController'
        })
        .when('/project/:id', {
            templateUrl: '/static/js/bugman/templates/lottery.html',
            controller: 'LotteryController'
        })
        .otherwise({
            redirecTo: '/'
        });
});