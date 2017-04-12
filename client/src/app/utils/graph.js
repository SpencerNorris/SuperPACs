
import d3 from './d3-modules';

class Graph {
    constructor(element) {
        //add our svg to the given element and set it up
        this.width = 1200;
        this.height = 900;
        this.svg = d3.select(element).append("svg");
        this.svg.attr("width", this.width).attr("height", this.height).style("background-color", "white");
        //add an empty arbitrary element, we'll add our graph to this later
        this.vis = this.svg.append("g");

        //automatically resize the svg when the window's size changes
        let resizeSVG = (() => {
            var rect = d3.select(element).node().getBoundingClientRect();
            this.width = rect.width;
            this.height = rect.height;

            this.svg.attr("width", this.width).attr("height", this.height);
        }).bind(this);
        window.onresize = resizeSVG;
        setTimeout(resizeSVG, 100);

        //set up zooming and panning functionality for the visualization
        this.zoom = d3.zoom()
            .scaleExtent([.01, 5])
            .on("zoom", () => {
                this.vis.attr("transform", d3.getEvent().transform);
            });

        this.svg.call(this.zoom).call(this.zoom.transform, d3.zoomIdentity.translate(0, this.height * .3));
    }

    /**
     * Recreate the graph with the given data
     */
    draw(data) {
        //clear the svg
        this.vis.selectAll("*").remove();

        //our graph, represented through nodes and links
        var nodes = [];
        var links = [];

        //add our nodes
        //add the committee nodes
        let init_y = 0;
        Object.keys(data.committees || {}).forEach(function(rep) {
            nodes.push({id:"c_"+data.committees[rep].id, name: data.committees[rep].name, x: 300, fx: 300, y: init_y+=60});
        });

        //add the representative nodes
        init_y = 0;
        Object.keys(data.representatives || {}).forEach(function(rep) {
            nodes.push({id:"r_"+data.representatives[rep].id, name: data.representatives[rep].name,party:data.representatives[rep].party, x:600, fx: 600, y: init_y+=60});
        });

        //add the bill nodes
        init_y = 0;
        Object.keys(data.bills || {}).forEach(function(rep) {
            nodes.push({id:"b_"+data.bills[rep].id, name: data.bills[rep].name, x: 900, fx: 900, y: init_y+=60});
        });

        //add our links
        //add the donation links between committees and representatives
        Object.keys(data.donations || {}).forEach(function(rep) {
            if(data.donations[rep].source in data.committees && data.donations[rep].destination in data.representatives){
                links.push({source:"c_"+data.donations[rep].source, target: "r_"+data.donations[rep].destination,thickness:data.donations[rep].amount,support:data.donations[rep].support});
            }
        });

        //add the vote links between representatives and bills
        Object.keys(data.votes || {}).forEach(function(rep) {
            links.push({source:"r_"+data.votes[rep].source, target: "b_"+data.votes[rep].destination});
        });

        //a scaling function that limits how think or thin edges can be in our graph
        var thicknessScale = d3.scaleLinear().domain([0,d3.max(data.donations,function(d){return d.amount;})]).range([2, 20]);

        //Create a force directed graph and define forces in it
        //Our graph is essentially a physics simulation between nodes and edges
        var force = d3.forceSimulation(nodes)
                        .force("charge", d3.forceManyBody().strength(250).distanceMax(300))
                        .force('link', d3.forceLink(links).distance(0).strength(.1).id(function(d) {return d.id;}))
                        .force("collide", d3.forceCollide().radius(30).iterations(2).strength(.7))
                        .force("center", d3.forceCenter())
                        .force('Y', d3.forceY().y(0).strength(.001));
        //Draw the edges between the nodes
        var edges = this.vis.selectAll("line")
                        .data(links)
                        .enter()
                        .append("line")
                        .style("stroke-width", function(d) { return thicknessScale(d.thickness); })
                        .style("stroke",function(d){
                            if(d.support == "S"){
                                return "Green";
                            }else if(d.support=="O"){
                                return "Purple";
                            }
                        })
                        .attr("marker-end", "url(#end)");
        //Draw the nodes themselves
        var circles = this.vis.selectAll("circle")
                        .data(nodes)
                        .enter()
                        .append("circle")
                        .attr("r", 20)
                        .style("stroke", "black")
                        .style("fill",function(d){
                            if(d.party == "R"){
                                return d.color = "#E64A19"; //red
                            } else if(d.party=="D"){
                                return d.color = "#1976D2"; //blue
                            } else {
                                return d.color = "#BCAAA4"; //brown
                            }
                        });
        //Draw text for all the nodes
        var texts = this.vis.selectAll("text")
                        .data(nodes)
                        .enter()
                        .append("text")
                        .attr("fill", "black")
                        .attr("font-family", "sans-serif")
                        .attr("font-size", "10px")
                        .html(function(d) { return d.name; })
                        .each(function(d) { d.bbox = this.getBBox(); });
        //Draw text background for all the nodes
        var textBGs = this.vis.selectAll("rect")
                        .data(nodes)
                        .enter()
                        .insert("rect", "text")
                        .attr("fill", function(d){return d.color;})
                        .attr("width", function(d){return d.bbox.width+10})
                        .attr("height", function(d){return d.bbox.height+10});

        //For every tick in our simulation, we update the positions for all ui elements
        force.on("tick", function() {
            edges.attr("x1", function(d) { return d.source.x; })
                    .attr("y1", function(d) { return d.source.y; })
                    .attr("x2", function(d) { return d.target.x; })
                    .attr("y2", function(d) { return d.target.y; });
            circles.attr("cx", function(d) { return d.x; })
                    .attr("cy", function(d) { return d.y; })
            texts.attr("transform", function(d) { return "translate(" + (d.party ? d.x : d.x-d.bbox.width) + "," + (d.y+(d.bbox.height/4)) + ")"; });
            textBGs.attr("transform", function(d) { return "translate(" + (d.party ? d.x-5 : d.x-d.bbox.width-5) + "," + (d.y-(d.bbox.height*.5)-5) + ")"; });
        }); // End tick func

        //zoom and pan our graph such that all elements are visible
        setTimeout(() => {this.zoomTo(this.vis)}, 100);
    }

    /**
     * Zoom and pan the graph so that the given element is visible
     */
    zoomTo(element) {
        //calculate the zooming and panning parameters needed
        var bounds = element.node().getBBox();
        var parent = element.node().parentElement;
        var width = bounds.width,
            height = bounds.height;
        var midX = bounds.x + width / 2,
            midY = bounds.y + height / 2;
        if (width == 0 || height == 0) return; // nothing to fit
        var scale = Math.max(.01, Math.min(5, 0.85 / Math.max(width / this.width, height / this.height)));
        var translate = [this.width / 2 - scale * midX, this.height / 2 - scale * midY];

        //if the element is empty, don't zoom or pan
        if(bounds.width == 0 || bounds.height == 0) {
            return;
        }

        //perform the zooming and panning
        this.svg.transition().duration(750).call(this.zoom.transform, d3.zoomIdentity.translate(translate[0], translate[1]).scale(scale));
    }
}

//export our graph as an AMD module
export default Graph;
