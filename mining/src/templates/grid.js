var btn = document.getElementById("btn");
console.log("test");
btn.addEventListener("click", function(){
	var ourrequest = new XMLHttpRequest();
	ourrequest.open('GET', 'http://localhost:5000/kmeans');
	ourrequest.onload = function(){
		var data = JSON.parse(ourrequest.responseText);
		console.log(data);
	};
	ourrequest.send();
});

getId = function(i, j, data){
	var square = j*100 + i;
	if(data.hasOwnProperty(square)){
		console.log(data[square]);
		return data[square];
	}
	else
		return 0;
};

function gridData(dt) {
	var data = new Array();
	var xpos = 1; //starting xpos and ypos at 1 so the stroke will show when we make the grid below
    var ypos = 1;
    var width = 9;
    var height = 9;

	// iterate for rows
	for (var row = 0; row < 100; row++) {
		data.push( new Array() );

		// iterate for cells/columns inside rows
		for (var column = 0; column < 100; column++) {
			data[row].push({
				x: xpos,
				y: ypos,
				width: width,
				height: height,
				click: getId(row, column, dt)
			});
			// increment the x position. I.e. move it over by 50 (width variable)
			xpos += width;
		}
		// reset the x position after a row is complete
		xpos = 1;
		// increment the y position for the next row. Move it down 50 (height variable)
		ypos += height;
	}
	return data;
}


var gridData = gridData(dt);
console.log(gridData);
// I like to log the data to the console for quick debugging

var grid = d3.select("#grid")
	.append("svg")
	.attr("width","1000px")
	.attr("height","1000px");

var row = grid.selectAll(".row")
	.data(gridData)
	.enter().append("g")
	.attr("class", "row");
var column = row.selectAll(".square")
    .data(function(d) { return d; })
    .enter().append("rect")
    .attr("class","square")
    .attr("x", function(d) { return d.x; })
    .attr("y", function(d) { return d.y; })
    .attr("width", function(d) { return d.width; })
    .attr("height", function(d) { return d.height; })
    .style("fill", function (d) {
        var colors = [
            "#fff",
            "#2C93E8",
            "#F56C4E",
            "#838690",
            "#f3e"
            ];
        return colors[d.click];
    })
    .style("stroke", "#222");