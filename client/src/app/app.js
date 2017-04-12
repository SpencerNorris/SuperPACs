import angular from 'angular';
import ngMaterial from 'angular-material';
import ngSortable from 'angular-legacy-sortablejs-maintained';

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
angular.module(MODULE_NAME, [ngMaterial, 'ng-sortable'])
  .directive('app', app)
  .controller('AppCtrl', /*@ngInject*/ ($scope, $http) => {
      //init some inital data
      $scope.filters = [];
      $scope.searchItem = null;
      $scope.data = {};
      //configuration for the sortable filter list
      $scope.sortableConf = {
          animation: 150,
          ghostClass: "ghost",
          onUpdate: (evt) => {
              //refresh our graph when the list get rearranged
              $scope.refreshGraph();
          }
      };
      //setup the graph
      $scope.graph = new Graph("#graph");

      //this function gets called whenever someone types in the search box, with their query so far
      $scope.searchQuery = (query) => {
          //make a call to our api with the query
          return $http
            .get('/api/search', {params: { query: query }})
            .then(function(response) {
                // Map the server's response to a format we can use.
                let data = [];

                //add matching special filters we have client size
                for(const f of Filter.general.filter((f) => {return f.name.toLowerCase().indexOf(query.toLowerCase()) != -1})) {
                    data.push({name: f.name, type: Filter.type.GENERAL, predicateFactory: f.predicateFactory});
                }

                //add matching representatives as filters
                for(const rep of response.data['representatives']) {
                    data.push({name: rep.name, type: Filter.type.REPRESENTATIVE});
                }

                //add matching committees as filters
                for(const committee of response.data['committees']) {
                    data.push({name: committee.name, type: Filter.type.COMMITTEE});
                }

                //todo add bills

                return data;
          });
      };

      //this gets called whenever the user selects a filter with the search box
      $scope.$watch('searchItem', () => {
          //make sure its a valid object
          if($scope.searchItem instanceof Object) {
              //get the item and its respective filter factory
              let item = $scope.searchItem;
              let predicateFactory = item.type == Filter.type.GENERAL ?
                          item.predicateFactory : Filter.nodeFilterFactory(item);

              //add the filter to our list of filters, initially in additive mode
              $scope.filters.unshift({
                  name: item.name,
                  type: item.type,
                  predicate: predicateFactory(true),
                  predicateFactory,
                  additive: true
              });

              //clear the user's selected item
              $scope.searchItem = null;
              $scope.searchText = "";

              //refresh our graph
              $scope.refreshGraph();
          }
      });

      //removes the given filter from the filter list and refreshes the graph
      $scope.removeFilter = (filter) => {
          $scope.filters.splice($scope.filters.indexOf(filter), 1);
          $scope.refreshGraph();
      };

      //flips the given filter's additive mode and refreshes the graph
      $scope.flipFilter = (filter) => {
          filter.additive = !filter.additive;
          filter.predicate = filter.predicateFactory(filter.additive);
          $scope.refreshGraph();
      };

      //refreshes the graph
      $scope.refreshGraph = () => {
          let filteredData = Filter.filter($scope.filters, $scope.data);
          $scope.graph.draw(filteredData);
      };

      //get our entire donation dataset from the server
      $http.get('/api/donations').then((response) => {
          $scope.data = response.data;
          $scope.refreshGraph();
      });
  });

export default MODULE_NAME;
