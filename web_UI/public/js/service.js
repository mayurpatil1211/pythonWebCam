'use strict';

angular.module('app')

.factory('appService',['$http', '$timeout', function ($http,  $timeout) {
    var service = {};

    service.listImagesService = function (callback) {

      $http.get('http://127.0.0.1:8000/app/list_images')
      .success(function (response) {
        callback(response);
      })
      .error(function(response){
        console.log(response)
      });

    };

    service.clickPhoto = function (greyScale, callback) {
        console.log(greyScale)
      $http.post('http://127.0.0.1:5000/'+greyScale)
      .success(function (response) {
        callback(response);
      })
      .error(function(response){
        console.log(response)
      });

    };

    return service;
  }]);

