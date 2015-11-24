/*jshint*/
/*global d3 */
    
function drawGraph(elemID, data, type) {
    switch(type) {
        case "bar":
            bargraph(elemID, data);
            break;
        case "line":
            linegraph(elemID, data);
            break;
        case "pie":
            piegraph(elemID, data);
            break;
    }
}

function bargraph(elemID, data) {
    $("#" + elemID).empty();
    var width = $("#" + elemID).parent().width(),
        barHeight = 8.5;

    var x = d3.scale.linear()
        .domain([0, d3.max(data)])
        .range([0, width - 5]);

    var chart = d3.select("#" + elemID)
        .attr("width", width)
        .attr("height", barHeight * data.length);

    var bar = chart.selectAll("g")
        .data(data)
        .enter().append("g")
        .attr("transform", function (d, i) {
            return "translate(0," + i * barHeight + ")";
        });

    bar.append("rect")
        .attr("width", function(d) {
            console.log(d);
            console.log(x(d));
            return x(d);
        })
        .attr("height", barHeight - 1);

    bar.append("text")
        .attr("x", function (d) {
            return x(d) - 3;
        })
        .attr("y", barHeight / 2)
        .attr("dy", ".35em")
        .text(function (d) {
            return d;
        });
        
}

function linegraph(elemID, data) {
    $("#" + elemID).empty();
    var WIDTH = $("#" + elemID).parent().width()+80,
        HEIGHT = 250,
        MARGINS = {
            top: 30,
            right: 70,
            bottom: 30,
            left: 30
        },
        xScale = d3.scale.linear().range([MARGINS.left, WIDTH - MARGINS.right]).domain([d3.min(data, function(d) { return d.x; }), d3.max(data, function(d) { return d.x; })]),
        yScale = d3.scale.linear().range([HEIGHT - MARGINS.top, MARGINS.bottom]).domain([d3.min(data, function(d) { return d.y; }), d3.max(data, function(d) { return d.y; })]),
        xAxis = d3.svg.axis()
            .scale(xScale)
            .ticks(Math.max(WIDTH/50, 2)),
        yAxis = d3.svg.axis()
            .scale(yScale)
            .orient("left"),
        vis = d3.select("#" + elemID).attr("width", WIDTH).attr("height", HEIGHT);
    
    vis.append("svg:g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + (HEIGHT - MARGINS.bottom) + ")")
        .call(xAxis);
    vis.append("svg:g")
        .attr("class", "y axis")
        .attr("transform", "translate(" + (MARGINS.left) + ",0)")
        .call(yAxis);
    var lineGen = d3.svg.line()
        .x(function(d) {
            return xScale(d.x);
        })
        .y(function(d) {
            return yScale(d.y);
        })
        .interpolate("basis");
    vis.append('svg:path')
        .attr('d', lineGen(data))
        .attr('stroke', 'green')
        .attr('stroke-width', 2)
        .attr('fill', 'none');
}

function piegraph(elemID, data) {
    
}

 