var ALLIGATOR_BASE = 'https://alligator.p.ota.to/api/v2/'


app.factory('alligator', ['$http', function($http) {

    return $http.get('/api/alligator/')
        .success(function(data) {
            return data;
        })
        .error(function(err) {
            return err;
        });
}]);
