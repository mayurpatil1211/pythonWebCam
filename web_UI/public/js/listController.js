"use strict";

angular.module("app").controller("listCtrl", ["$scope", "appService", function ($scope, appService) {

		$scope.pictures = []
		$scope.listImages = function(){
			appService.listImagesService(function(response){
				if(response.length>0){
						$scope.pictures = response
						console.log()
				
					}else{
						$scope.pictures = []
					}
			});
			
		}

		$scope.listImages()


	}]);