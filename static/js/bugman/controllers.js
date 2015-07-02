app.controller('ProjectsController', ['$scope', 'alligator', function($scope, alligator) {
    alligator.success(function(data) {
        $scope.projects = data.projects;
    });
}]);

app.controller('LotteryController', ['$scope', '$http', 'alligator', '$routeParams', 'weeklyResults', function($scope, $http, alligator, $routeParams, weeklyResults) {

    $(".button-collapse").sideNav();

    alligator.success(function(data) {
        $scope.projects = data.projects;
        $scope.allocations = data.allocations;
        $scope.users = data.users;
        $scope.allUsers = data.all_users;
        $scope.projectId = $routeParams.id;
        $scope.project = $scope.selectProject($scope.projectId);
        $scope.projectUsers = filterUsers(parseInt($scope.projectId));
        $scope.checkedUsers = $scope.projectUsers;

        if ($scope.project) {
            $scope.weeklyResults = getWeeklyResults($scope.project);
        }
    });

    $scope.updateCollapsible = function() {
        $('.collapsible').collapsible({
            accordion : false // A setting that changes the collapsible behavior to expandable instead of the default accordion style
        });
    };

    $scope.getFullname = function(username) {
        var filteredUser = $scope.allUsers.filter(function(user) {
            return username == user.username;
        });
        if (filteredUser.length > 0) {
            return filteredUser[0].fullname;
        }
        return username;
    };

    var getWeeklyResults = function(project) {
        weeklyResults.getResults(project.id)
            .success(function(data) {
                $scope.weeklyResults = angular.fromJson(data);
            });
    };

    // set first and last day of a week
    $scope.firstDay = moment().startOf('week').toDate();
    $scope.lastDay = moment().endOf('week').toDate();

    $scope.losers = false;

    $scope.selectProject = function(projectId) {
        return $scope.projects.filter(function(project) { return projectId == project.id; })[0];
    };

    $scope.getProjectUserByUserName = function(userName) {
        return $scope.projectUsers.filter(function(user) { return user.username == userName; })[0];
    };

    var filterUsers = function(projectId) {

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

    $scope.updateCheckedUsers = function() {
        var checkedUsers = new Array();
        $('.user-checkbox').each(function(idx, el) {
            if (el.checked) {
                checkedUsers.push(el.value)
            }
        });

        $scope.checkedUsers = $scope.projectUsers.filter(function(user) {
            return checkedUsers.indexOf(user.username) > -1;
        });
    };

    $scope.days = new Array("monday", "tuesday", "wednesday", "thursday", "friday");
    $scope.short_days = new Array("Mon", "Tue", "Wed", "Thu", "Fri");

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
        var usernames = getUsernamesFromUl(usersUl);
        var offset = usersCount - usernames.indexOf(pick) + 1;
        var loopsCount = offset + getRandomInt(2, 6) * usersCount;

        for (var i=0; i<loopsCount; i++) {
            list.animate({top: '+=30'}, i+25+2*i, 'linear', function () {
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
                    $('.user-checkbox').prop('disabled', false);
                    getWeeklyResults($scope.project);
                }
            });
        }
    };

    $scope.startAll = function() {

        var usernames = $scope.checkedUsers.map(function(user) { return user.username; });

        $http.post('/bugmans/' + $routeParams.id  + '/', usernames)
        .then(function(result) {
            $scope.losers = result.data;
            $('.roll-it-btn').addClass('disabled');
            $('.user-checkbox').prop('disabled', true);

            angular.forEach($scope.days, function(day) {
                $scope.rollIt(day.toLowerCase());
            });
        });
    };

    $scope.allStopped = function() {
        return $scope.progress == $scope.days.length;
    };
}]);
