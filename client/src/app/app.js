import angular from 'angular';
import ngMaterial from 'angular-material';

import Graph from './utils/graph';
import Filter from './utils/filter';

import 'font-awesome/css/font-awesome.css';
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

                for(const f of Filter.general.filter((f) => {return f.name.toLowerCase().indexOf(query.toLowerCase()) != -1})) {
                    data.push({name: f.name, type: Filter.type.GENERAL, predicate: f.predicate});
                }

                for(const rep of response.data['representatives']) {
                    data.push({name: rep.name, type: Filter.type.REPRESENTATIVE});
                }

                for(const committee of response.data['committees']) {
                    data.push({name: committee.name, type: Filter.type.COMMITTEE});
                }

                //todo add bills

                return data;
          });
      };

      $scope.$watch('searchItem', () => {
          if($scope.searchItem instanceof Object) {
              let item = $scope.searchItem;
              $scope.filters.unshift({
                  name: item.name,
                  predicate: (obj, type) => {
                      if(item.type == Filter.type.GENERAL) {
                          return item.predicate(obj, type);
                      } else if(item.type == type) {
                          return obj.name == item.name ?
                            Filter.actions.ADD : Filter.actions.PASS;
                      }
                      return Filter.actions.PASS;
                  }
              });

              $scope.searchItem = null;
              $scope.searchText = "";

              $scope.refreshGraph();
          }
      });

      $scope.removeFilter = (filter) => {
          $scope.filters.splice($scope.filters.indexOf(filter), 1);
          $scope.refreshGraph();
      }

      $scope.refreshGraph = () => {
          let filteredData = Filter.filter($scope.filters, $scope.data);
          $scope.graph.draw(filteredData);
      };

      $http.get('/api/donations').then((response) => {
          $scope.data = response.data;
          $scope.refreshGraph();
      });
  });

export default MODULE_NAME;
