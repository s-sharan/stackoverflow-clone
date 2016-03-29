var app = angular.module('stackoverflowApp', ['ui.router']);

app.config(function($stateProvider, $urlRouterProvider) {
  $urlRouterProvider.otherwise('/login');
  
  $stateProvider.state('login', {
    templateUrl: 'login.html',
    url: '/login',
    controller: 'loginController'
  })
  .state('search', {
      templateUrl: 'search.html',
      url: '/search',
      controller: 'searchController'
  })
  .state('createQuestion', {
      templateUrl: 'createQuestion.html',
      url: '/createQuestion',
      controller: 'createQuestionController'
  })
  .state('admin', {
      templateUrl: 'admin.html',
      url: '/admin',
      controller: 'adminController'
  })
  .state('question', {
    templateUrl: 'question.html',
    url: '/search',
    controller: 'questionController'
  });
});

app.controller('navigationController', function($scope, $state) {
    console.log("Testing Navigation");
    $scope.logout = function() {$state.go('login');};
    $scope.isLoggedIn = function() {return !$state.is('login')};
});

app.controller('loginController', function($scope, $state) {
    $scope.authenticate = function() {
        /* 
            OAuth Stuff
        */
        
        $state.go('search');
    };
});

app.controller('questionController', function($scope, $rootScope, $state) {
    console.log('Testing Question');
    $scope.question = $rootScope.selectedQuestion;
    $scope.back = function() {$state.go('search')};
    
    $scope.hasComments = function(answer) {
        console.log('answer = ' + answer);
        if(answer != null && answer.comments != null && answer.comments.length > 0)
            return true;
        return false;
    };
});

app.controller('searchController', function($scope, $rootScope, $state, $http) {
    console.log('Testing Search');
    $scope.questions = {};
    
    $scope.viewQuestion = function(index) {
        $rootScope.selectedQuestion = $scope.questions[index];
        $state.go('question');
    };
    
    $scope.searchQuery = function() {
        
        if($scope.query == null || $scope.query == "") alert('test');
        else {
            $http({
                method: 'POST',
                url: '/search',
                data: {query: $scope.query},
                transformResponse: function (data, headersGetter, status) {
                    //This was implemented since the REST service is returning a plain/text response
                    //and angularJS $http module can't parse the response like that.
                    return {data: data};
                }
            }).success(function (response, status) {
                $scope.questions = JSON.parse(response.data);
            }).error(function () {
                console.log('failure');
            });
        }
    }
});

app.controller('createQuestionController', function($scope, $http) {
    $scope.question = {};
    $scope.error = "";
    $scope.allTags = [{id: 1, label:"C++"}, {id: 2, label: "Java"}];
    $scope.createQuestion = function() {
        if($scope.question.title == null) $scope.error = "Enter a title for the question";
        else if($scope.question.body == null) $scope.error = "Enter description for the question";
        else if($scope.selectedTags == null || $scope.selectedTags.length <= 0) $scope.error = "Please select atleast one Tag";
        else {
            $http.post('/insertquestion', {
                userid: "1",
                title: $scope.question.title,
                body: $scope.question.body,
                tags: $scope.selectedTags
              }).then(function (response) {
                console.log('response = ' + JSON.stringify(response));
                if (response.status == 200) {
                  $scope.error="Question Created Successfully";
                  $scope.question.title = null; $scope.question.body = null; $scope.selectedTags = null; 
                }
                else
                  $scope.createStatus = 'Error = ' + JSON.stringify(response);
              });
        }
    };
    console.log('Testing Create Question');
});

app.controller('adminController', function($scope) {
    console.log('Testing admin Page');
    $scope.user = {name: "Rakesh Yarlagadda", badges: ["Silver", "Gold"]};
    $scope.fecthUser = function() {
        alert($scope.username);
    }
    $scope.assignableBadges = ["Bronze"];
    $scope.removableBadges = ["Silver", "Gold"];
});