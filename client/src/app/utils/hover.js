import d3 from './d3-modules';
//TODO:Subclass this hoe class to work with any kind of node, edge.
class Hover {
  scream(){
    console.log("scream");
    alert("Scream");
  }
  // Create Event Handlers for mouse
  handleMouseOverRepresentative(d,i) {  // Add interactivity
    //alert(d);
    console.log(d);

    let locache = d3.select(this.parentNode).selectAll("g > rect").attr("transform");
    locache = locache.substring(locache.indexOf("(")+1, locache.indexOf(")")).split(",");
    let color = d3.select(this.parentNode).selectAll("g > rect").style("fill");
    console.log(locache);
    console.log(color)
    // Use D3 to select element, change color and size
    //If statement for checking the status of a node? is it a superpac or a representative.



    d3.select(this.parentElement).append("rect")
    .style("fill",color)
    .attr("height","22px")
    .attr("width","150px")
    .attr("transform",() => {return "translate("+String(52+parseInt(locache[0]))+","+String(parseInt(locache[1]))+")"});
    //.html((d) => { });

    d3.select(this.parentElement).append("text")
    .attr("font-family", "sans-serif")
    .attr("font-size", "10px")
    .attr("transform",() => {return "translate("+String(52+parseInt(locache[0]))+","+String(14+parseInt(locache[1]))+")";})
    .html(()=>{return "("+d.party+")"+" from "+d.state+"'s "+d.district+" district";});


    /*attr({
      fill: "tan",
      text: d.name+"("+d.party+")"+" from "+d.state+"'s "+d.district+" disrict"
    });*/

  }

  handleMouseOutRepresentative() {
    // Use D3 to select element, change color back to normal
    d3.select(this).attr({
      fill: "black",
    });

    // Select text by id and then remove
    //d3.select("#t" + d.x + "-" + d.y + "-" + i).remove();  // Remove text location
  }

}
export default Hover;
