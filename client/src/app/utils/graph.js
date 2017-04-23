
import d3 from './d3-modules';
import Hover from './hover';

class Graph {
    constructor(element, nodeMenu) {
        //add our svg to the given element and set it up
        this.width = 1200;
        this.height = 900;
        this.svg = d3.select(element).append("svg");
        this.nodeMenu = nodeMenu;
        this.parentElement = element;
        this.vis = this.svg.append("g"); //add an empty arbitrary element, we'll add our graph to this later

        this.svg.attr("width", this.width).attr("height", this.height).style("background-color", "white");

        //automatically resize the svg when the window's size changes
        window.onresize = this.resize.bind(this);
        setTimeout(this.resize.bind(this), 100);

        //set up zooming and panning functionality for the visualization
        this.zoom = d3.zoom()
            .scaleExtent([.01, 5])
            .on("zoom", () => {
                this.vis.attr("transform", d3.getEvent().transform);
            });

        this.svg.call(this.zoom).call(this.zoom.transform, d3.zoomIdentity.translate(0, this.height * .3));
        this.hover = new Hover();

    }

    /**
     * Recreate the graph with the given data
     */
    draw(data) {
        //clear the svg
        this.vis.selectAll("*").remove();

        //our graph, represented through nodes and links
        let nodes = [];
        let links = [];

        //Most nodes follow (id,type,arg1,arg2....) pattern
        //Most edges follow (id,sourceid,targetid,type,arg1,arg2) pattern

        //add the committee nodes
        let init_y = 0;
        Object.keys(data.committees || {}).forEach((key) => {
            nodes.push({id:"c_"+data.committees[key].id, name: data.committees[key].name, type:"superpac", x: 300, fx: 300, y: init_y+=60});
        });

        //add the representative nodes
        init_y = 0;
        Object.keys(data.representatives || {}).forEach((key) => {
            nodes.push({id:"r_"+data.representatives[key].id, name: data.representatives[key].name, type:"representative", party:data.representatives[key].party, x:600, fx: 600, y: init_y+=60, state:data.representatives[key].state, district:data.representatives[key].district});
        });

        //add the bill nodes
        init_y = 0;
        Object.keys(data.bills || {}).forEach((key) => {
            nodes.push({id:"b_"+data.bills[key].bill_id, name: data.bills[key].name, bill:true, x: 900, fx: 900, y: init_y+=60});
        });

        //add our links
        //add the donation links between committees and representatives
        Object.keys(data.donations || {}).forEach((key) => {
            if(data.donations[key].source in data.committees && data.donations[key].destination in data.representatives){
                links.push({id:"d_"+data.donations[key].source+"d"+data.donations[key].destination,source:"c_"+data.donations[key].source, target: "r_"+data.donations[key].destination,type:"donation",thickness:data.donations[key].amount, status:data.donations[key].support == "S" ? 1 : 2});
                //TODO: refactor the id system for the links node. This ghetto id is mainly a hack for now to enable edge hovering.
            }
        });

        //add the vote links between representatives and bills
        Object.keys(data.votes || {}).forEach((key) => {
            if(data.votes[key].source in data.representatives && data.votes[key].destination in data.bills){
                links.push({source:"r_"+data.votes[key].source, target: "b_"+data.votes[key].destination,type:"vote", status:data.votes[key].position == "Yes" ? 1 : data.votes[key].position == "No" ? 2 : 3});
            }
        });

        //a scaling function that limits how think or thin edges can be in our graph
        let thicknessScale = d3.scaleLinear().domain([0,d3.max(data.donations,(d) => {return d.amount;})]).range([2, 20]);

        //function that calls our given context menu with the appropria parameters
        let contextMenu = (d) => {
            let event = d3.getEvent();
            event.preventDefault();
            this.nodeMenu(d, event);
        };

        //Create a force directed graph and define forces in it
        //Our graph is essentially a physics simulation between nodes and edges
        let force = d3.forceSimulation(nodes)
                        .force("charge", d3.forceManyBody().strength(250).distanceMax(300))
                        .force('link', d3.forceLink(links).distance(0).strength(.1).id((d) => {return d.id;}))
                        .force("collide", d3.forceCollide().radius(30).iterations(2).strength(.7))
                        .force("center", d3.forceCenter())
                        .force('Y', d3.forceY().y(0).strength(.001));
        //Draw the edges between the nodes
        let edges = this.vis.selectAll("line")
                        .data(links)
                        .enter()
                        .append("path")//So that I could have text on the path.
                        .attr("id",(d)=>{return String(d.source.id)+"d"+String(d.target.id);})
                        .style("stroke-width", (d) => { return thicknessScale(d.thickness); })
                        .style("stroke", (d) => {
                            if(d.status == 1) {
                                return "Green";
                            } else if(d.status == 2) {
                                return "Purple";
                            }
                            return "White";
                        })
                        .attr("d", (d)=>{return "M "+d.source.x+","+d.source.y+" L "+d.target.x+","+d.target.y})
                        .attr("marker-end", "url(#end)")
                        .on("mouseover", this.hover.handleMouseOverEdge)
                        .on("mouseout", this.hover.handleMouseOutEdge);
        //Draw the nodes themselves
        let circles = this.vis.selectAll("circle")
                        .data(nodes)
                        .enter()
                        .append("circle")
                        .attr("r", 20)
                        .attr("id",(d) => {return d.id;})
                        .style("stroke", "black")
                        .style("fill", (d) => {
                            if(d.party == "R"){
                                return d.color = "#E64A19"; //red
                            } else if(d.party=="D"){
                                return d.color = "#1976D2"; //blue
                            } else {
                                return d.color = "#BCAAA4"; //brown
                            }
                        })
                        .on('contextmenu', contextMenu)
                        .on("mouseover", this.hover.handleMouseOverNode)
                        .on("mouseout", this.hover.handleMouseOutNode);
        //Draw text for all the nodes
        let texts = this.vis.selectAll("text")
                        .data(nodes)
                        .enter()
                        .append("text")
                        .attr("id",(d) => {return d.id;})
                        .attr("fill", "black")
                        .attr("font-family", "sans-serif")
                        .attr("font-size", "10px")
                        .html((d) => { return d.name; })
                        .each((d, i, nodes) => { d.bbox = nodes[i].getBBox(); })
                        .on('contextmenu', contextMenu);
        //Draw text background for all the nodes
        let textBGs = this.vis.selectAll("rect")
                        .data(nodes)
                        .enter()
                        .insert("rect", "text")
                        .attr("id",(d) => {return d.id;})
                        .attr("fill", (d) => {return d.color;})
                        .attr("width", (d) => {return d.bbox.width+10})
                        .attr("height", (d) => {return d.bbox.height+10})
                        .on('contextmenu', contextMenu);

        //For every tick in our simulation, we update the positions for all ui elements
        force.on("tick", () => {
            edges.attr("x1", (d) => { return d.source.x; })
                    .attr("y1", (d) => { return d.source.y; })
                    .attr("x2", (d) => { return d.target.x; })
                    .attr("y2", (d) => { return d.target.y; })
                    .attr("d", (d) => {return "M "+d.source.x+" "+d.source.y+" L "+d.target.x+" "+d.target.y;});
            circles.attr("cx", (d) => { return d.x; })
                    .attr("cy", (d) => { return d.y; })
            texts.attr("transform", (d) => { return "translate(" + (d.party || d.bill ? d.x : d.x-d.bbox.width) + "," + (d.y+(d.bbox.height/4)) + ")"; });
            textBGs.attr("transform", (d) => { return "translate(" + (d.party || d.bill ? d.x-5 : d.x-d.bbox.width-5) + "," + (d.y-(d.bbox.height*.5)-5) + ")"; });
        }); // End tick func

        //zoom and pan our graph such that all elements are visible
        setTimeout(() => {this.zoomTo(this.vis)}, 500);
    }

    /**
     * Zoom and pan the graph so that the given element is visible
     */
    zoomTo(element) {
        //calculate the zooming and panning parameters needed
        let bounds = element.node().getBBox();
        let parent = element.node().parentElement;
        let width = bounds.width,
            height = bounds.height;
        let midX = bounds.x + width / 2,
            midY = bounds.y + height / 2;
        if (width == 0 || height == 0) return; // nothing to fit
        let scale = Math.max(.01, Math.min(5, 0.85 / Math.max(width / this.width, height / this.height)));
        let translate = [this.width / 2 - scale * midX, this.height / 2 - scale * midY];

        //if the element is empty, don't zoom or pan
        if(bounds.width == 0 || bounds.height == 0) {
            return;
        }

        //perform the zooming and panning
        this.svg.transition().duration(750).call(this.zoom.transform, d3.zoomIdentity.translate(translate[0], translate[1]).scale(scale));
    }

    /**
     * Resizes the graph to fit the parent element
     */
    resize() {
        let rect = d3.select(this.parentElement).node().getBoundingClientRect();
        this.width = rect.width;
        this.height = rect.height;

        this.svg.attr("width", this.width).attr("height", this.height);
    }
}

//export our graph as an AMD module
export default Graph;
