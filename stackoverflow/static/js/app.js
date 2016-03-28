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

app.controller('searchController', function($scope, $rootScope, $state) {
    console.log('Testing Search');
    $scope.questions = [{title: 'Is angular better than react ?', tags: ['C++', 'Java'], answers: [{title: 'No not at all', comments: [{text: 'Is it really ?'}]}, {title: 'Yes it is right'}]}, 
        {title: 'Is java better than C++ ?', tags: ['C++', 'Java'], answers: [{title: 'No not at all'}, {title: 'Yes it is right'}]}, 
        {title: 'Is javascript a better language ?', tags: ['C++', 'Java'], answers: [{title: 'No not at all'}, {title: 'Yes it is right'}]}, 
        {title: 'Is angular better than react ?', tags: ['C++', 'Java'], answers: [{title: 'No not at all'}, {title: 'Yes it is right'}]},
        {title: 'Is javascript a better language ?', tags: ['C++', 'Java'], answers: [{title: 'No not at all'}, {title: 'Yes it is right'}]}, 
        {title: 'Is angular better than react ?', tags: ['C++', 'Java'], answers: [{title: 'No not at all'}, {title: 'Yes it is right'}]},
        {title: 'Is javascript a better language ?', tags: ['C++', 'Java'], answers: [{title: 'No not at all'}, {title: 'Yes it is right'}]}, 
        {title: 'Is angular better than react ?', tags: ['C++', 'Java'], answers: [{title: 'No not at all'}, {title: 'Yes it is right'}]},
        {title: 'Is javascript a better language ?', tags: ['C++', 'Java'], answers: [{title: 'No not at all'}, {title: 'Yes it is right'}]}, 
        {title: 'Is angular better than react ?', tags: ['C++', 'Java'], answers: [{title: 'No not at all'}, {title: 'Yes it is right'}]}];
    console.log($scope.questions);
    
    $scope.viewQuestion = function(index) {
        $rootScope.selectedQuestion = $scope.questions[index];
        $state.go('question');
    };
    
    $scope.search = function(queryString) {
        
    }
});

app.controller('createQuestionController', function($scope) {
    $scope.allTags = [{id: 1, label:"C++"}, {id: 2, label: "Java"}];
    $scope.selectedTags = [];
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