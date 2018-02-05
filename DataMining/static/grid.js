var clusters = 9;
getId = function(i, j, data){
    var square = (j)*100 + (100 - i);
    if(data.hasOwnProperty(square)){
        return data[square];
    }
    else
        return 0;
};

var gdt = function gridData(dt) {
    var data = new Array();
    var xpos = 1; //starting xpos and ypos at 1 so the stroke will show when we make the grid below
    var ypos = 1;
    var width = 7;
    var height = 7;

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


var draw = function drawGrid(data) {
    var gridData = gdt(data);
    var grid = d3.select("#grid")
        .append("svg")
        .attr("width", "1000px")
        .attr("height", "1000px");

    var row = grid.selectAll(".row")
        .data(gridData)
        .enter().append("g")
        .attr("class", "row");
    var column = row.selectAll(".square")
        .data(function (d) {
            return d;
        })
        .enter().append("rect")
        .attr("class", "square")
        .attr("x", function (d) {
            return d.x;
        })
        .attr("y", function (d) {
            return d.y;
        })
        .attr("width", function (d) {
            return d.width;
        })
        .attr("height", function (d) {
            return d.height;
        })
        .style("fill", function (d) {
            var colors = [
                "#2635ED",
                "#45B841",
                //"#7FDC3B",
                //"#ABDC3B",
                "#CBDC3B",
                "#EDCC26",
                "#EDA226",
                "#ED7D26",
                "#ED2641",
                "#ED5026"
            ];
            return colors[d.click];
        })
        .style("stroke", "#222");
};


$(document).ready(function(){
	$("button").click(function(){
		$.get("prediction/ttt", function(data, status){
       			draw_histogram("line", data);
    		});
	});
});

var x = d3.scale.ordinal().rangeRoundBands([0, width], .05);

var y = d3.scale.linear().range([height, 0]);

var margin = {top: 20, right: 20, bottom: 70, left: 40},
    width = 600 - margin.left - margin.right,
    height = 300 - margin.top - margin.bottom;

var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", 200 + margin.top + margin.bottom)
  .append("g")
    .attr("transform", 
          "translate(" + margin.left + "," + margin.top + ")");

var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");

var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left")
        .ticks(10);

var draw_histogram =function(error, data) {
	data = JSON.parse(data);
	console.log(data);
	svg.append("g")
	    .attr("class", "x axis")
	    .attr("transform", "translate(0," + 200 + ")")
	    .call(xAxis)
	    .selectAll("text")
	    .style("text-anchor", "end")
	    .attr("dx", "-.8em")
	    .attr("dy", "-.55em")
	    .attr("transform", "rotate(-90)" );
	
	svg.append("g")
	    .attr("class", "y axis")
	    .call(yAxis)
	    .append("text")
	    .attr("transform", "rotate(-90)")
	    .attr("y", 6)
	    .attr("dy", ".71em")
	    .style("text-anchor", "end")
	    .text("Value ($)");
	
	svg.selectAll("bar")
	    .data(data)
	    .enter()
	    .append("rect")
	    .style("fill", "steelblue")
	    .attr("x", function(d) { return x(d.x); })
	    .attr("y", function(d) { return y(d.y); })
	    .attr("height", function(d) { return 200 - y(d.y); });
};

 

var btn_dbscan = document.getElementById("btn_dbscan");
btn_dbscan.addEventListener("click", function(){
    var ourrequest = new XMLHttpRequest();
ourrequest.open('GET', 'http://localhost:5000/clustering/dbscan');
    ourrequest.onload = function(){
        var data = JSON.parse(ourrequest.responseText);
        data = JSON.parse(data);
        console.log(data);
        d3.select('svg').remove();
        draw(data['labels']);
        document.getElementById("ttle").innerHTML = "dbscan";
    };
        ourrequest.send();
});



var btn_tree = document.getElementById("btn_tree");
btn_tree.addEventListener("click", function(){
    var ourrequest = new XMLHttpRequest();
    ourrequest.open('GET', 'http://localhost:5000/clustering/tree');
    ourrequest.onload = function(){
        var data = JSON.parse(ourrequest.responseText);
        data = JSON.parse(data);
        document.getElementById("ttle").innerHTML = "isolation forest";
        d3.select('svg').remove();
        draw(data['labels']);
    };
        ourrequest.send();
});

var btn = document.getElementById("btn");
btn.addEventListener("click", function(){
    var ourrequest = new XMLHttpRequest();
    ourrequest.open('GET', 'http://localhost:5000/clustering/kmeans/'+clusters);
    ourrequest.onload = function(){
        var data = JSON.parse(ourrequest.responseText);
        data = JSON.parse(data);
	console.log(data);
        document.getElementById("ttle").innerHTML = "kmeans";
        d3.select('svg').remove();
        draw(data['labels']);

    };
        ourrequest.send();
});

var btn_ward = document.getElementById("btn_ward");
btn_ward.addEventListener("click", function(){
    var ourrequest = new XMLHttpRequest();
    ourrequest.open('GET', 'http://localhost:5000/clustering/ward');
    ourrequest.onload = function(){
        var data = JSON.parse(ourrequest.responseText);
        data = JSON.parse(data);
        document.getElementById("ttle").innerHTML = "ward";
        d3.select('svg').remove();
        draw(data['labels']);


    };
        ourrequest.send();
});

var btn_apriori = document.getElementById("btn_apriori");
btn_apriori.addEventListener("click", function(){
    var ourrequest = new XMLHttpRequest();
    ourrequest.open('GET', 'http://localhost:5000/clustering/apriori');
    ourrequest.onload = function(){
        var data = JSON.parse(ourrequest.responseText);
        console.log(data);
        document.getElementById("ttle").innerHTML = "apriori";
        d3.select('svg').remove();
    };
        ourrequest.send();
});


