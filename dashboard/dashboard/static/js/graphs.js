/*jshint*/
/*global d3, console */
    
function drawGraph(elemID, data, type) {
    if ($("#" + elemID).parent().width() < 0) return;
    switch(type) {
        case "bar":
            bargraph(elemID, data);
            break;
        case "line":
            linegraph(elemID, data);
            break;
    }
}

function bargraph(elemID, data) {
    data = data[0];
    $("#" + elemID).empty();
    var width = $("#" + elemID).parent().width(),
        barHeight = 8.5;

    var x = d3.scale.linear()
        .domain([0, d3.max(data, function(d) {return d.y;})])
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
            return x(d.y);
        })
        .attr("height", barHeight - 1);

    bar.append("text")
        .attr("x", function (d) {
            return x(d.y) - 3;
        })
        .attr("y", barHeight / 2)
        .attr("dy", ".35em")
        .text(function (d) {
            return d.y;
        });
        
}

function linegraph(elemID, data) {
    $("#" + elemID).empty();
    var xMin = data[0][0].x, xMax = data[0][0].x, yMin = data[0][0].y, yMax = data[0][0].y;
    var xMinCurr, xMaxCurr, yMinCurr, yMaxCurr;
    
    for (var i=0; i<data.length; i++) {
        xMinCurr = d3.min(data[i], function(d) {return d.x; });
        xMaxCurr = d3.max(data[i], function(d) {return d.x; });
        yMinCurr = d3.min(data[i], function(d) {return d.y; });
        yMaxCurr = d3.max(data[i], function(d) {return d.y; });
        
        if (xMinCurr < xMin) xMin = xMinCurr;
        if (xMaxCurr > xMax) xMax = xMaxCurr;
        if (yMinCurr < yMin) yMin = yMinCurr;
        if (yMaxCurr > yMax) yMax = yMaxCurr;
    }
    
    var WIDTH = $("#" + elemID).parent().width(),
        colours = ['green', 'blue', 'red', 'yellow', 'orange'],
        HEIGHT = 250,
        MARGINS = {
            top: 30,
            right: 30,
            bottom: 30,
            left: 30
        },
        xScale = d3.scale.linear().range([MARGINS.left, WIDTH - MARGINS.right]).domain([xMin, xMax]),
        yScale = d3.scale.linear().range([HEIGHT - MARGINS.top, MARGINS.bottom]).domain([0, yMax]),
        xAxis = d3.svg.axis()
            .scale(xScale)
            .ticks(Math.max(WIDTH/50, 2)),
        yAxis = d3.svg.axis()
            .scale(yScale)
            .orient("left"),
        vis = d3.select("#" + elemID).attr("width", WIDTH).attr("height", HEIGHT);
    
    console.log("BEFORE: " + MARGINS.left);
    var maxw = 0;
    vis.append("svg:g")
        .attr("class", "y axis")
        .attr("transform", "translate(" + MARGINS.left + ",0)")
        .call(yAxis)
        .selectAll("text").each(function() {
            if(this.getBBox().width > maxw) {
                maxw = this.getBBox().width;
                MARGINS.left = Math.max(MARGINS.left, maxw + 10);
            }
        });
    vis.selectAll("g").remove();
    console.log("AFTER: " + MARGINS.left);
        
    xScale = d3.scale.linear().range([MARGINS.left, WIDTH - MARGINS.right]).domain([xMin, xMax]);
    yScale = d3.scale.linear().range([HEIGHT - MARGINS.top, MARGINS.bottom]).domain([0, yMax]);
    xAxis = d3.svg.axis()
        .scale(xScale)
        .ticks(Math.max(WIDTH/50, 2));
    yAxis = d3.svg.axis()
        .scale(yScale)
        .orient("left");
        
    vis.append("svg:g")
        .attr("class", "y axis")
        .attr("transform", "translate(" + MARGINS.left + ",0)")
        .call(yAxis);
        
    vis.append("svg:g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + (HEIGHT - MARGINS.bottom) + ")")
        .call(xAxis);
    
    var lineGen = d3.svg.line()
        .x(function(d) {
            return xScale(d.x);
        })
        .y(function(d) {
            return yScale(d.y);
        })
        .interpolate("basis");
        
    for (i=0; i<data.length; i++) {
        vis.append('svg:path')
        .attr('d', lineGen(data[i]))
        .attr('stroke', colours[i])
        .attr('stroke-width', 2)
        .attr('fill', 'none');
    }
    
}

 