app.controller('ProjectsController', ['$scope', 'alligator', function($scope, alligator) {
    alligator.success(function(data) {
        $scope.projects = data.projects;
    });
}]);

app.controller('LotteryController', ['$scope', '$http', 'alligator', 'bugmans', '$routeParams', function($scope, $http, alligator, bugmans, $routeParams) {
    alligator.success(function(data) {
        $scope.projects = data.projects;
        $scope.allocations = data.allocations;
        $scope.users = data.users;
        $scope.project = $scope.selectProject($routeParams.id);
        $scope.projectUsers = $scope.filterUsers(parseInt($routeParams.id));
    });

    $scope.losers = [];

    $scope.selectProject = function(projectId) {
        return $scope.projects.filter(function(project) { return projectId == project.id; })[0];
    };

    $scope.filterUsers = function(projectId) {
        var filteredAllocations = $scope.allocations.filter(function(allocation) { return allocation.project === parseInt(projectId); });
        var projectUsers = new Array();
        if (filteredAllocations) {
            angular.forEach(filteredAllocations, function(allocation) {
                var foundUser = $scope.users.filter(function(user) {
                    return user.username == allocation.user;
                })[0];
                if (projectUsers.indexOf(foundUser) === -1) {
                    projectUsers.push(foundUser);
                }
            });
        }
        return projectUsers;
    };

    $scope.progress = 0;

    $scope.allStopped = function() {
        return $scope.progress == $scope.days.length;
    };

    $scope.days = new Array("monday", "tuesday", "wednesday", "thursday", "friday");

    var getUsernamesFromUl = function(users) {
        var usernames = new Array();
        angular.forEach(users, function(user) {
            usernames.push($(user).data('id'))
        });
        return usernames;
    };

    var getRandomInt = function(min, max) {
        return Math.floor(Math.random() * (max - min)) + min;
    };

    $scope.rollIt = function(day) {
        var pick = $scope.losers[day];
        var list = $('.' + day + ' ul');
        var usersCount = list.children().length;
        var initTop = list.css('top');
        $scope.progress = 0;

        var loopsMade = 0;
        var usersUl = list.children();
        var userNames = getUsernamesFromUl(usersUl);
        var offset = usersCount - userNames.indexOf(pick) + 1;
        var loopsCount = offset + getRandomInt(5, 15) * usersCount;

        for (var i=0; i<loopsCount; i++) {
            list.animate({top: '+=40'}, i+50+2*i, 'linear', function () {
                var usersUl = list.children();
                var lastUser = usersUl[usersCount - 1];

                list.css('top', initTop);
                list.prepend(lastUser);
                loopsMade += 1;

                if (loopsCount == loopsMade) {
                    $scope.progress += 1;
                }

                if ($scope.allStopped()) {
                    $('.roll-it-btn').removeClass('disabled');
                }
            });
        }
    };

    $scope.results = new Array();

    $scope.startAll = function() {

        // get the results
        $http.get('/bugmans/' + $routeParams.id)
        .then(function(result) {
            $scope.losers = result.data;
            $('.roll-it-btn').addClass('disabled');

            bugmans.success(function(data) {
                $scope.results = data;
            });

            angular.forEach($scope.days, function(day) {
                $scope.rollIt(day.toLowerCase());
            });
        });
    };
}]);