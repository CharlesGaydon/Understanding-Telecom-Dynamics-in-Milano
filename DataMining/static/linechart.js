    $.ajax({
            type: "POST",
            contentType: "application/json; charset=utf-8",
            url: 'url to your web servise',
            dataType: 'json',
            async: true,
            data: "{}", 
            success: function (data) {
               var pos_data = data;
               div_name = "div.histogram";

        draw_histogram(div_name, pos_data);

            },
            error: function (result) {



}
    })



//The drawing of the histogram has been broken out from the data retrial 
    // or computation. (In this case the 'Irwin-Hall distribution' computation above)

    function draw_histogram(reference, pos_data){

        $(reference).empty()

        //The drawing code needs to reference a responsive elements dimneions
        var width = $(reference).width();
        // var width = $(reference).empty().width(); we can chain for effeicanecy as jquery returns jquery.

        // var height = 230;  // We don't want the height to be responsive.

        var margin = {top: 10, right: 30, bottom: 40, left: 30},
        // width = 960 - margin.left - margin.right,
        height = 270 - margin.top - margin.bottom;


        var histogram = d3.layout.histogram() (pos_data);
        //var neg_histogram = d3.layout.histogram()(neg_data);

        var x = d3.scale.ordinal()
            .domain(histogram.map(function(d) { return d.x; }))
            .rangeRoundBands([0, width]);

        var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");


        var y = d3.scale.linear()
            .domain([0, d3.max(histogram.map(function(d) { return d.y; }))])
            .range([0, height]);

        //var ny = d3.scale.linear()
        //    .domain([0, d3.max(neg_histogram.map(function(d) { return d.y; }))])
        //    .range([0, height]);

        var svg = d3.select(reference).append("svg")
            .attr("width", width)
            .attr("height", height + 20);



        svg.selectAll("rect")
            .data(histogram)
          .enter().append("rect")
            .attr("width", x.rangeBand())
            .attr("x", function(d) { return x(d.x); })
            .attr("y", function(d) { return height - y(d.y); })
            .attr("height", function(d) { return y(d.y); });


        svg.append("line")
            .attr("x1", 0)
            .attr("x2", width)
            .attr("y1", height)
            .attr("y2", height);

        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + (height)  + ")")
            .call(xAxis);
    };

    //Bind the window resize to the draw method.
    //A simple bind example is

    //A better idom for binding with resize is to debounce
    var debounce = function(fn, timeout) 
    {
      var timeoutID = -1;
      return function() {
        if (timeoutID > -1) {
          window.clearTimeout(timeoutID);
        }
        timeoutID = window.setTimeout(fn, timeout);
      }
    };

    var debounced_draw = debounce(function() {
      draw_histogram(div_name, pos_data);
    }, 125);

    $(window).resize(debounced_draw);

