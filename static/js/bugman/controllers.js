app.controller('ProjectsController', ['$scope', 'alligator', function($scope, alligator) {
    //alligator.success(function(data) {
    //    console.log('dupa!');
    //    $scope.project = data.projects;
    //    $scope.allocations = data.allocations;
    //    $scope.users = data.users;
    //});

    $scope.projects = PROJECTS;
    $scope.allocations = ALLOCATIONS;
    $scope.users = USERS;

    $scope.message = 'Default';
    $scope.selectedProject = false;

}]);

app.controller('LotteryController', ['$scope', 'alligator', '$routeParams', function($scope, alligator, $routeParams) {
    $scope.message = 'routing is working!';
    //alligator.success(function(data) {
    //    $scope.project = data['projects'];
    //    $scope.allocations = data['allocations'];
    //    $scope.users = data['users'];
    //});

    $scope.projects = PROJECTS;
    $scope.allocations = ALLOCATIONS;
    $scope.users = USERS;

    $scope.selectProject = function(projectId) {
        return $scope.projects.filter(function(project) { return projectId == project.id; })[0];
    };

    $scope.project = $scope.selectProject($routeParams.id);

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

    $scope.projectUsers = $scope.filterUsers(parseInt($routeParams.id));
    $scope.progress = 0;

    $scope.resultsReady = function() {
        return $scope.progress == $scope.days.length;
    };

    $scope.results = new Array();

    $scope.days = new Array("monday", "tuesday", "wednesday", "thursday", "friday");

    $scope.rollIt = function(day, loopsCount) {
        var list = $('.' + day + ' ul');
        var usersCount = list.children().length;
        var initTop = list.css('top');
        var loopsMade = 0;
        $scope.progress = 0;
        $scope.results = new Array();

        for (var i=0; i<loopsCount; i++) {
            list.animate({top: '+=40'}, i+75, 'linear', function () {
                var users = list.children();
                var lastUser = users[usersCount - 1];

                //lastUser.remove();
                list.css('top', initTop);
                list.prepend(lastUser);
                loopsMade += 1;

                if (loopsCount == loopsMade) {
                    $scope.progress += 1;
                }

                if ($scope.resultsReady()) {
                    $scope.results = $scope.getResults();
                }
            });
        }
    };

    var getRandomInt = function(min, max) {
        return Math.floor(Math.random() * (max - min)) + min;
    };

    $scope.startAll = function() {
        $('.roll-it-btn').addClass('disabled');
        angular.forEach($scope.days, function(day, idx) {
            var usersCount = $scope.projectUsers.length;
            var extraLoops = getRandomInt(0, usersCount) + usersCount * idx;
            var loopsCount = 25 + extraLoops;
            $scope.rollIt(day.toLowerCase(), loopsCount);
        });
    };

    $scope.getResultForDay = function(day) {
        var list = $('.' + day.toLowerCase() + ' ul');
        return list.children()[1].innerText;
    };

    $scope.getResults = function() {
        var results = {};
        angular.forEach($scope.days, function(day) {
            results[day] = $scope.getResultForDay(day);
        });
        $('.roll-it-btn').removeClass('disabled');
        return results;
    };

}]);