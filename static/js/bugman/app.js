var app = angular.module('BugmanApp', ['ngRoute'])
.config(function($interpolateProvider) {
        $interpolateProvider.startSymbol('{$');
        $interpolateProvider.endSymbol('$}');
    })
.config(function($routeProvider) {
    $routeProvider
        .when('/:id', {
            templateUrl: '/static/js/bugman/templates/lottery.html',
            controller: 'LotteryController'
        })
        .when('/', {
            templateUrl: '/static/js/bugman/templates/lottery.html',
            controller: 'LotteryController'
        });
});