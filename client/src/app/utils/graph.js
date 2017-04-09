
import d3 from './d3-modules';

class Graph {
    constructor(element) {
        this.width = 1200;
        this.height = 900;
        this.svg = d3.select(element).append("svg");
        this.svg.attr("width", this.width).attr("height", this.height).style("background-color", "white");
        this.vis = this.svg.append("g");

        this.zoom = d3.zoom()
            .scaleExtent([.01, 5])
            .on("zoom", () => {
                this.vis.attr("transform", d3.getEvent().transform);
            });

        this.svg.call(this.zoom).call(this.zoom.transform, d3.zoomIdentity.translate(0, this.height * .3));
    }

    draw(data) {
        //clear the svg
        this.vis.selectAll("*").remove();

        var nodes = [];
        var links = [];

        //nodes
        let init_y = 0;
        Object.keys(data.committees).forEach(function(rep) {
            nodes.push({id:"c_"+data.committees[rep].id, name: data.committees[rep].name, x: 300, _x: 300, y: init_y+=60, _y: 400});
        });

        init_y = 0;
        Object.keys(data.representatives).forEach(function(rep) {
            nodes.push({id:"r_"+data.representatives[rep].id, name: data.representatives[rep].name,party:data.representatives[rep].party, x:600, _x: 600, y: init_y+=60, _y: 400});
        });

        //uncomment when bills are added
        /*Object.keys(data.bills).forEach(function(rep) {
            nodes.push({id:"b_"+data.bills[rep].id, name: data.bills[rep].name, _x: 700, _y: 200});
        });*/

        //links
        Object.keys(data.donations).forEach(function(rep) {
            if(data.donations[rep].source in data.committees && data.donations[rep].destination in data.representatives){
                links.push({source:"c_"+data.donations[rep].source, target: "r_"+data.donations[rep].destination,thickness:data.donations[rep].amount,support:data.donations[rep].support});
            }
        });

        //uncomment when votes are added
        /*Object.keys(data.votes).forEach(function(rep) {
            links.push({source:"r_"+data.votes[rep].source, target: "b_"+data.votes[rep].destination});
        });*/

        var y = d3.scaleLinear().domain([0,d3.max(data.donations,function(d){return d.amount;})]).range([2, 20]);

        /* Establish the dynamic force behavor of the nodes */
        var force = d3.forceSimulation(nodes)
                        .force('link', d3.forceLink(links).distance(0).strength(0.1).id(function(d) {return d.id;}))
                        .force('X', d3.forceX().x(function(d) { return d._x }).strength(function() {return 2;}))
                        .force("collide", d3.forceCollide().radius(function(d) { return 20 + 10; }).iterations(2));
        /* Draw the edges/links between the nodes */
        var edges = this.vis.selectAll("line")
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
        /* Draw text for all the nodes */
        var texts = this.vis.selectAll("text")
                        .data(nodes)
                        .enter()
                        .append("text")
                        .attr("fill", "black")
                        .attr("font-family", "sans-serif")
                        .attr("font-size", "10px")
                        .html(function(d) { return d.name; })
                        .each(function(d) { d.bbox = this.getBBox(); });
        /* Draw text background for all the nodes */
        var textBGs = this.vis.selectAll("rect")
                        .data(nodes)
                        .enter()
                        .insert("rect", "text")
                        .attr("fill", function(d){return d.color;})
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
            texts.attr("transform", function(d) { return "translate(" + (d.party ? d.x : d.x-d.bbox.width) + "," + (d.y+(d.bbox.height/4)) + ")"; });
            textBGs.attr("transform", function(d) { return "translate(" + (d.party ? d.x-5 : d.x-d.bbox.width-5) + "," + (d.y-(d.bbox.height*.5)-5) + ")"; });
        }); // End tick func

        setTimeout(() => {this.zoomTo(this.vis)}, 100);
    }

    zoomTo(element) {
        var bounds = element.node().getBBox();
        var parent = element.node().parentElement;
        var fullWidth = parent.clientWidth || parent.parentNode.clientWidth,
            fullHeight = parent.clientHeight || parent.parentNode.clientHeight;
        var width = bounds.width,
            height = bounds.height;
        var midX = bounds.x + width / 2,
            midY = bounds.y + height / 2;
        if (width == 0 || height == 0) return; // nothing to fit
        var scale = Math.max(.05, Math.min(5, 0.85 / Math.max(width / fullWidth, height / fullHeight)));
        var translate = [fullWidth / 2 - scale * midX, fullHeight / 2 - scale * midY];

        if(bounds.width == 0 || bounds.height == 0) {
            return;
        }

        this.svg.transition().duration(750).call(this.zoom.transform, d3.zoomIdentity.translate(translate[0], translate[1]).scale(scale));
    }
}
export default Graph;
