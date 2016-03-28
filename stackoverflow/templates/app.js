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
  .state('question', {
    templateUrl: "question.html",
    url: '/search',
    controller: "questionController"
  });
});

app.controller('navigationController', function($scope) {
    console.log("Testing Navigation");
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
});