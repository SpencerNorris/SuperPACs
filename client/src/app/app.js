import angular from 'angular';
import ngMaterial from 'angular-material';
import ngSortable from 'angular-legacy-sortablejs-maintained';
import cgBusy from '@cgross/angular-busy';
import $ from 'jquery';

import Graph from './utils/graph';
import Filter from './utils/filter';

import 'font-awesome/css/font-awesome.css';
import 'angular-material/angular-material.css';
import '@cgross/angular-busy/dist/angular-busy.css';
import '../style/app.css';

let app = () => {
  return {
    template: require('./app.html'),
    controller: 'AppCtrl',
    controllerAs: 'app'
  }
};

const MODULE_NAME = 'app';
angular.module(MODULE_NAME, [ngMaterial, 'ng-sortable', cgBusy])
  .directive('app', app)
  .controller('AppCtrl', /*@ngInject*/ ($scope, $http) => {
      //init some inital data
      $scope.filters = [];
      $scope.searchItem = null;
      $scope.data = {};
      $scope.ctxMenu = {top: 0, left: 0, show: false, items: []};
      $scope.sidebarHidden = false;
      $scope.legendHidden = false;//Legend setup

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
      $scope.graph = new Graph("#graph", (d, e) => {
          //context menu handler, this function shows our context menu for nodes
          //set menu position
          $scope.ctxMenu.top = e.clientY;
          $scope.ctxMenu.left = e.clientX;

          if(d.id.startsWith("r_")) { //menu for representatives
              $scope.ctxMenu.items = [
                {name: "Add Donating SuperPACs", action: () => {
                    //a menu item that adds all the superpacs that donated to this representative
                    let names = [];
                    let id = d.id.substring(2);
                    //loop over all the donations getting matches
                    Object.keys($scope.data.donations || {}).forEach((key) => {
                        if($scope.data.donations[key].destination == id) {
                            names.push($scope.data.committees[$scope.data.donations[key].source].name);
                        }
                    });

                    //create a multi node filter
                    let predicateFactory = Filter.multiNodeFilterFactory(names, Filter.type.COMMITTEE);

                    //add the filter to our list of filters, initially in additive mode
                    $scope.filters.unshift({
                        name: d.name+"'s SuperPACs",
                        type: Filter.type.COMMITTEE,
                        predicate: predicateFactory(true),
                        predicateFactory,
                        additive: true
                    });

                    //refresh our graph
                    $scope.refreshGraph();
                }}
              ];
          } else if(d.id.startsWith("c_")) {//menu for committees
              $scope.ctxMenu.items = [
                {name: "Add Politicians Donated To", action: () => {
                    //a menu item that adds all the representatives that superpac donated to
                    let names = [];
                    let id = d.id.substring(2);
                    //loop over all the donations getting matches
                    Object.keys($scope.data.donations || {}).forEach((key) => {
                        if($scope.data.donations[key].source == id) {
                            names.push($scope.data.representatives[$scope.data.donations[key].destination].name);
                        }
                    });

                    //create a multi node filter
                    let predicateFactory = Filter.multiNodeFilterFactory(names, Filter.type.REPRESENTATIVE);

                    //add the filter to our list of filters, initially in additive mode
                    $scope.filters.unshift({
                        name: d.name+"'s Recipents",
                        type: Filter.type.REPRESENTATIVE,
                        predicate: predicateFactory(true),
                        predicateFactory,
                        additive: true
                    });

                    //refresh our graph
                    $scope.refreshGraph();
                }}
              ];
          }

          //show the menu
          $scope.ctxMenu.show = true;
          $scope.$apply();
      });

      //gets rid of our context menu when the user clicks elsewhere or presses escape
      let hideCtxMenu = (e) => {
          if($scope.ctxMenu.show) {
              if(e && e.target && (e.target.id == "ctxMenu" || $(e.target).parents("#ctxMenu").length)) {
                  return;
              }
              $scope.ctxMenu.show = false;
              $scope.$apply();
          }
      };
      $(document).mousedown(hideCtxMenu);
      $(window).blur(hideCtxMenu);
      $(document).keyup((e) => {
          if (e.keyCode == 27) { // escape key maps to keycode `27`
              hideCtxMenu();
          }
      });

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

      //this gets triggered whenever the sidebar gets hidden, it causes the graph to resize
      $scope.$watch('sidebarHidden', () => {
          setTimeout(() => {
              $scope.graph.resize();
          }, 10);
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
      $scope.donationPromise = $http.get('/api/donations').then((response) => {
          $scope.data = response.data;
          $scope.refreshGraph();
      });
  });

export default MODULE_NAME;
