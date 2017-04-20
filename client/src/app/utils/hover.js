import d3 from './d3-modules';
//TODO:Subclass this class to work with any kind of node, edge.
class Hover {

  //Mouse event when you stop hovering over a node in the visualization.
  //Shows the representative description of the representative on the edge.
  handleMouseOverNode(d,i) {  // Add interactivity

    //If statement for checking the status of a node.
    //is it a superpac or a representative.
    if(d.type == "representative"){
      if(d.district == ""){
        d3.select(this.parentNode).selectAll("g > text#"+d.id)
          .html(()=>{return d.name+" ("+d.party+") senator from "+d.state;});
      }else{
        d3.select(this.parentNode).selectAll("g > text#"+d.id)
          .html(()=>{return d.name+" ("+d.party+") congressman from "+d.state+"'s district "+d.district;});
      }


      d3.select(this.parentNode).selectAll("g > rect#"+d.id)
        .attr("width",250);
        //TODO:Could use a bounding box, but I don't know how to do it.
        //TODO:Make this less coupled with the json data. Essentially remove need for if statements
    }
  }

  //Mouse event when you stop hovering over a node in the visualization.
  //Shows the representative description of the representative on the edge.
  handleMouseOutNode(d,i) {

    if(d.type == "representative"){
      d3.select(this.parentNode).selectAll("g > rect#"+d.id)
        .attr("width",d.bbox.width+10);

      d3.select(this.parentNode).selectAll("g > text#"+d.id)
      .html((d)=>{return d.name;});
    }
  }

  //Mouse event when you hover over a donation edge in the visualization.
  //Shows the dollar amount donated from the superpac to the representative on the edge.
  handleMouseOverEdge(d,i){
    if(d.type == "donation"){
      //Thickness is amount....
      var svg = d3.select("g");
      let thickness = d.thickness;
      let id = d.id;

      svg.append("text")
      .append("textPath")
      .attr("id",()=>{return id;})
       .attr("xlink:href", "#"+d.id) //place the ID of the path here
       .style("text-anchor","right")
       .attr("startOffset", "50%")
       .text(()=>{return "$"+String(thickness);});//
    }

  }
  //Mouse event when you stop hovering over a donation edge in the visualization.
  //hides the dollar amount donated from the superpac to the representative on the edge.
  handleMouseOutEdge(d,i){
    if(d.type == "donation"){
      d3.selectAll("text > textPath#"+d.id).remove();
    }
  }
}
export default Hover;
