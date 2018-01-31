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
    var width = 5;
    var height = 5;

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

        // I like to log the data to the console for quick debugging

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
                "#ef5",
                "#2C93E8",
                "#F56C4E",
                "#f3e",
                "#838690"
            ];
            return colors[d.click];
        })
        .style("stroke", "#222");
};


var btn_dbscan = document.getElementById("btn_dbscan");
btn_dbscan.addEventListener("click", function(){
    var ourrequest = new XMLHttpRequest();
    ourrequest.open('GET', 'http://localhost:5000/dbscan');
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
    ourrequest.open('GET', 'http://localhost:5000/tree');
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
    ourrequest.open('GET', 'http://localhost:5000/kmeans/'+clusters);
    ourrequest.onload = function(){
        var data = JSON.parse(ourrequest.responseText);
        data = JSON.parse(data);

        document.getElementById("ttle").innerHTML = "kmeans";
        d3.select('svg').remove();
        draw(data['labels']);
    };
        ourrequest.send();
});


var btn_ward = document.getElementById("btn_ward");
btn_ward.addEventListener("click", function(){
    var ourrequest = new XMLHttpRequest();
    ourrequest.open('GET', 'http://localhost:5000/ward');
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
    ourrequest.open('GET', 'http://localhost:5000/apriori');
    ourrequest.onload = function(){
        var data = JSON.parse(ourrequest.responseText);
        data = JSON.parse(data);
        console.log(data);
        document.getElementById("ttle").innerHTML = "apriori";
        d3.select('svg').remove();
    };
        ourrequest.send();
    });
