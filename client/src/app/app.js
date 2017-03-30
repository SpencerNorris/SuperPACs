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
    console.log("new graph");
		var vis = d3.select("#graph").append("svg");
		var w = 900, h = 900;
		vis.attr("width", w).attr("height", h).transition().style("background-color", "white");

		var nodes = [];
		var links = [];
		var representatives = [];

		//nodes
		Object.keys(data.committees).forEach(function(rep) {
			nodes.push({id:"c_"+data.committees[rep].id, name: data.committees[rep].name, _x: 200, _y: 400});
		});

		Object.keys(data.representatives).forEach(function(rep) {
			nodes.push({id:"r_"+data.representatives[rep].id, name: data.representatives[rep].name,party:data.representatives[rep].party, _x: 450, _y: 400});
		});


		/*Object.keys(data.bills).forEach(function(rep) {
			nodes.push({id:"b_"+data.bills[rep].id, name: data.bills[rep].name, _x: 700, _y: 200});
		});*/

		//links
		Object.keys(data.donations).forEach(function(rep) {
      if(data.donations[rep].from in data.committees && data.donations[rep].to in data.representatives){
        links.push({source:"c_"+data.donations[rep].from, target: "r_"+data.donations[rep].to,thickness:data.donations[rep].amount,support:data.donations[rep].support});
      }

		});

		/*Object.keys(data.votes).forEach(function(rep) {
			links.push({source:"r_"+data.votes[rep].from, target: "b_"+data.votes[rep].to});
		});*/
		var y = d3.scaleLinear().domain([0,d3.max(data.donations,function(d){return d.amount;})]).range([2, 20]);
		/* Draw the node labels first */

		/* Establish the dynamic force behavor of the nodes */
		var force = d3.forceSimulation(nodes)
						//.force("link", d3.forceLink(links))
						//.size([w,h])
						//.linkDistance([250])
						.force("charge", d3.forceManyBody().strength(function() {return -50*nodes.length;}))//charge([-1500])
						//.gravity(0.3)
						//.start();
						//.force("center", d3.forceCenter());
						.force('link', d3.forceLink(links).distance(0).strength(0.01).id(function(d) {return d.id;}))
						.force('X', d3.forceX().x(function(d) { return d._x }).strength(function() {return 3;}))
						.force('Y', d3.forceY().y(function(d) { return d._y }).strength(function() {return .1;}))
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


		var texts = vis.selectAll("text")
					.data(nodes)
					.enter()
					.append("text")
					.attr("fill", "black")
					.attr("font-family", "sans-serif")
					.attr("font-size", "10px")
					.text(function(d) { return d.name; });
		/* Draw the nodes themselves */
		var nodes = vis.selectAll("circle")
						.data(nodes)
						.enter()
						.append("circle")
						.attr("r", 20)
						.attr("opacity", 0.5)
						.style("fill",function(d){//try{

																				if(d.party == "R"){
																					return "Red";
																				}else if(d.party=="D"){
																					return "Blue";
																				}
																			//} catch (){
																			//	return "#ooo"
																		//	}
																		});




						//.style("fill", "black")//function(d,i) { return d3.scale.category20()(i); })
						//.call(force.drag);
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

		/*vis.selectAll("circle .nodes")
			.data(nodes)
			.enter()
			.append("svg:circle")
			.attr("class", "nodes")
			.attr("cx", function(d) { return d.x; })
			.attr("cy", function(d) { return d.y; })
			.attr("r", "10px")
			.attr("fill", "black");
		vis.selectAll(".line")
		   .data(links)
		   .enter()
		   .append("line")
		   .attr("x1", function(d) { return d.source.x })
		   .attr("y1", function(d) { return d.source.y })
		   .attr("x2", function(d) { return d.target.x })
		   .attr("y2", function(d) { return d.target.y })
		   .style("stroke", "rgb(6,120,155)");*/
	}


const MODULE_NAME = 'app';

angular.module(MODULE_NAME, [])
  .directive('app', app)
  .controller('AppCtrl', /*@ngInject*/ ($http) => {
      $http.get('/api/datademo').then((response) => {
          alert("data");
          alert(response.data);
          console.log(response.data);
          drawGraph(response.data);
      });
  });

export default MODULE_NAME;
