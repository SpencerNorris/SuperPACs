import angular from 'angular';
import d3 from './d3-modules';
import '../style/app.css';

let app = () => {
  return {
    template: require('./app.html'),
    controller: 'AppCtrl',
    controllerAs: 'app'
  }
};

function drawGraph(data) {
    var vis = d3.select("#graph").append("svg");
    var w = 900, h = 400;
    vis.attr("width", w).attr("height", h).transition().style("background-color", "white");
    
    var nodes = [];
    var links = [];
    
    //nodes
    Object.keys(data.committees).forEach(function(rep) {
        nodes.push({id:"c_"+data.committees[rep].id, name: data.committees[rep].name, _x: 200, _y: 200});
    });
    
    Object.keys(data.representatives).forEach(function(rep) {
        nodes.push({id:"r_"+data.representatives[rep].id, name: data.representatives[rep].name, _x: 450, _y: 200});
    });
    
    Object.keys(data.bills).forEach(function(rep) {
        nodes.push({id:"b_"+data.bills[rep].id, name: data.bills[rep].name, _x: 700, _y: 200});
    });
    
    //links
    Object.keys(data.donations).forEach(function(rep) {
        links.push({source:"c_"+data.donations[rep].from, target: "r_"+data.donations[rep].to});
    });
    
    Object.keys(data.votes).forEach(function(rep) {
        links.push({source:"r_"+data.votes[rep].from, target: "b_"+data.votes[rep].to});
    });
    
    /* Draw the node labels first */
    var texts = vis.selectAll("text")
                    .data(nodes)
                    .enter()
                    .append("text")
                    .attr("fill", "black")
                    .attr("font-family", "sans-serif")
                    .attr("font-size", "10px")
                    .text(function(d) { return d.name; });
    /* Establish the dynamic force behavor of the nodes */
    var force = d3.forceSimulation(nodes)
                    .force("charge", d3.forceManyBody().strength(function() {return -50*nodes.length;}))
                    .force('link', d3.forceLink(links).distance(0).strength(0.01).id(function(d) {return d.id;}))
                    .force('X', d3.forceX().x(function(d) { return d._x }).strength(function() {return 1;}))
                    .force('Y', d3.forceY().y(function(d) { return d._y }).strength(function() {return .1;}))
    /* Draw the edges/links between the nodes */
    var edges = vis.selectAll("line")
                    .data(links)
                    .enter()
                    .append("line")
                    .style("stroke", "#ccc")
                    .style("stroke-width", 1)
                    .attr("marker-end", "url(#end)");
    /* Draw the nodes themselves */
    var nodes = vis.selectAll("circle")
                    .data(nodes)
                    .enter()
                    .append("circle")
                    .attr("r", 20)
                    .attr("opacity", 0.5)
                    .style("fill", "black");
    /* Run the Force effect */
    force.on("tick", function() {
        edges.attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });
        nodes.attr("cx", function(d) { return d.x; })
            .attr("cy", function(d) { return d.y; })
        texts.attr("transform", function(d) {
            return "translate(" + d.x + "," + d.y + ")";
        });
    }); // End tick func
}

const MODULE_NAME = 'app';

angular.module(MODULE_NAME, [])
  .directive('app', app)
  .controller('AppCtrl', ($http) => {
      $http.get('/api/demo').then((response) => {
          drawGraph(response.data);
      });
  });

export default MODULE_NAME;