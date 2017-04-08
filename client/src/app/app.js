import angular from 'angular';
import ngMaterial from 'angular-material';

import Graph from './utils/graph';
import filter from './utils/filter';

import 'angular-material/angular-material.css';
import '../style/app.css';

let app = () => {
  return {
    template: require('./app.html'),
    controller: 'AppCtrl',
    controllerAs: 'app'
  }
};

const MODULE_NAME = 'app';

angular.module(MODULE_NAME, [ngMaterial])
  .directive('app', app)
  .controller('AppCtrl', /*@ngInject*/ ($scope, $http) => {
      $scope.filters = [];
      $scope.searchItem = null;
      $scope.data = {};
      $scope.graph = new Graph("#graph");

      $scope.searchQuery = (query) => {
          return $http
            .get('/api/search', {params: { query: query }})
            .then(function(response) {
                // Map the response object to the data object.
                let data = [];

                for(const rep of response.data['representatives']) {
                    data.push({name: rep.name, type: "Representative"});
                }

                for(const committee of response.data['committees']) {
                    data.push({name: committee.name, type: "Committee"});
                }

                //todo add bills

                return data;
          });
      };

      $scope.$watch('searchItem', () => {
          if($scope.searchItem instanceof Object) {
              console.log($scope.searchItem);
              $scope.searchItem = null;
              $scope.searchText = "";
          }
      });

      $scope.refreshGraph = () => {
          let filteredData = filter($scope.filters, $scope.data);
          $scope.graph.draw(filteredData);
      };

      $http.get('/api/donationsDemo').then((response) => {
          $scope.data = response.data;
          $scope.refreshGraph();
      });
  });

export default MODULE_NAME;
