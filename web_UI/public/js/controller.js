"use strict";

angular.module("app").controller("appCtrl", ["$scope", "appService","$interval","$rootScope", function ($scope, appService, $interval, $rootScope) {

		$scope.clickStart = false

		$scope.startClicking = function(data){
			if (data.grayscale){
				var grayscale = 'true'
				appService.clickPhoto(grayscale ,function(response){
				alert(response.message)
				});
			}else{
				var grayscale = 'false'
				appService.clickPhoto(grayscale ,function(response){
				alert(response.message)
				});
			}	
		}


		$scope.startTimer=function(data){

			$scope.clickStart = true
			
			var calculate_interval = data.time + '000'
			var interval_time = Number(calculate_interval)
			$rootScope.promise = $interval( function(){ $scope.startClicking(data); }, interval_time);
		}

		$scope.cancel = function () {
				$scope.clickStart = false
                $interval.cancel($rootScope.promise);
				
				$scope.counter = "Cancelled!";
		};
		

	}]);