app.factory('alligator', ['$http', function($http) {

    return $http.get('/api/alligator/')
        .success(function(data) {
            return data;
        })
        .error(function(err) {
            return err;
        });
}]);

app.factory('weeklyResults', ['$http', function($http) {

    var urlBase = '/api/lottery-results/';
    var dataFactory = {};


    dataFactory.getResults= function (id) {
        return $http.get(urlBase + '/' + id + '/');
    };

    return dataFactory;
}]);
