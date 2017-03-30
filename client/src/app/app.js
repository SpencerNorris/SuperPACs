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
    var w = 1200, h = 900;
    vis.attr("width", w).attr("height", h).transition().style("background-color", "white");

    var nodes = [];
    var links = [];
    var representatives = [];

    //nodes
    Object.keys(data.committees).forEach(function(rep) {
        nodes.push({id:"c_"+data.committees[rep].id, name: data.committees[rep].name, _x: 300, _y: 400});
    });

    Object.keys(data.representatives).forEach(function(rep) {
        nodes.push({id:"r_"+data.representatives[rep].id, name: data.representatives[rep].name,party:data.representatives[rep].party, _x: 600, _y: 400});
    });

    //uncomment when bills are added
    /*Object.keys(data.bills).forEach(function(rep) {
        nodes.push({id:"b_"+data.bills[rep].id, name: data.bills[rep].name, _x: 700, _y: 200});
    });*/

    //links
    Object.keys(data.donations).forEach(function(rep) {
        if(data.donations[rep].from in data.committees && data.donations[rep].to in data.representatives){
            links.push({source:"c_"+data.donations[rep].from, target: "r_"+data.donations[rep].to,thickness:data.donations[rep].amount,support:data.donations[rep].support});
        }
    });

    //uncomment when votes are added
    /*Object.keys(data.votes).forEach(function(rep) {
        links.push({source:"r_"+data.votes[rep].from, target: "b_"+data.votes[rep].to});
    });*/
    
    var y = d3.scaleLinear().domain([0,d3.max(data.donations,function(d){return d.amount;})]).range([2, 20]);
    /* Draw the node labels first */

    /* Establish the dynamic force behavor of the nodes */
    var force = d3.forceSimulation(nodes)
                    .force("charge", d3.forceManyBody().strength(function() {return -500;}))
                    .force('link', d3.forceLink(links).distance(0).strength(0.005).id(function(d) {return d.id;}))
                    .force('X', d3.forceX().x(function(d) { return d._x }).strength(function() {return 8;}))
                    .force('Y', d3.forceY().y(function(d) { return d._y }).strength(function() {return .05;}))
                    .force("collide", d3.forceCollide().radius(function(d) { return 20 + 5; }).iterations(2));
    /* Draw the edges/links between the nodes */
    var edges = vis.selectAll("line")
                    .data(links)
                    .enter()
                    .append("line")
                    .style("stroke-width", function(d) { return y(d.thickness); })
                    .style("stroke",function(d){
                        if(d.support == "S"){
                            return "Green";
                        }else if(d.support=="O"){
                            return "Purple";
                        }
                    })
                    .attr("marker-end", "url(#end)");
    /* Draw the nodes themselves */
    var circles = vis.selectAll("circle")
                    .data(nodes)
                    .enter()
                    .append("circle")
                    .attr("r", 20)
                    .style("stroke", "black")
                    .style("fill",function(d){
                        if(d.party == "R"){
                            return d.color = "#E64A19";
                        } else if(d.party=="D"){
                            return d.color = "#1976D2";
                        } else {
                            return d.color = "#795548";
                        }
                    });
    /* Draw text for all the nodes */
    var texts = vis.selectAll("text")
                    .data(nodes)
                    .enter()
                    .append("text")
                    .attr("fill", "black")
                    .attr("font-family", "sans-serif")
                    .attr("font-size", "10px")
                    .text(function(d) { return d.name; })
                    .each(function(d) { d.bbox = this.getBBox(); });
    /* Draw text background for all the nodes */
    var textBGs = vis.selectAll("rect")
                    .data(nodes)
                    .enter()
                    .insert("rect", "text")
                    .attr("fill", function(d){return d.color;})//d3.rgb(d.color).darken(1);})
                    .attr("width", function(d){return d.bbox.width+10})
                    .attr("height", function(d){return d.bbox.height+10});
    /* Run the Force effect */
    force.on("tick", function() {
        edges.attr("x1", function(d) { return d.source.x; })
                .attr("y1", function(d) { return d.source.y; })
                .attr("x2", function(d) { return d.target.x; })
                .attr("y2", function(d) { return d.target.y; });
        circles.attr("cx", function(d) { return d.x; })
                .attr("cy", function(d) { return d.y; })
        texts.attr("transform", function(d) { return "translate(" + (d.party ? d.x : d.x-d.bbox.width) + "," + (d.y+(d.bbox.height/2)) + ")"; });
        textBGs.attr("transform", function(d) { return "translate(" + (d.party ? d.x-5 : d.x-d.bbox.width-5) + "," + (d.y-(d.bbox.height*.5)-5) + ")"; });
    }); // End tick func
}


const MODULE_NAME = 'app';

angular.module(MODULE_NAME, [])
  .directive('app', app)
  .controller('AppCtrl', /*@ngInject*/ ($http) => {
      $http.get('/api/datademo').then((response) => {
          drawGraph(response.data);
      });
  });

export default MODULE_NAME;
