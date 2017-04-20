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
    alert("#"+d.id);
    console.log(d3.selectAll("#"+d.id));
    let locache = d3.select(this.parentNode).selectAll("g > rect#"+d.id).attr("transform");
    console.log("loc"+locache);
    locache = locache.substring(locache.indexOf("(")+1, locache.indexOf(")")).split(",");
    let color = d3.select(this.parentNode).selectAll("g > rect#"+d.id).style("fill");

    let rectwidth = d3.select(this.parentNode).selectAll("g > rect#"+d.id).attr("width");
    //let id =
    console.log(locache);
    console.log(color);
    console.log(rectwidth);
    // Use D3 to select element, change color and size
    //If statement for checking the status of a node? is it a superpac or a representative.

    d3.select(this.parentNode).selectAll("g > rect#"+d.id)
      .attr("width","150px");

    d3.select(this.parentNode).selectAll("g > text#"+d.id)
      .html(()=>{return d.name+"("+d.party+")"+" from "+d.state+"'s "+d.district+" district";});


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
