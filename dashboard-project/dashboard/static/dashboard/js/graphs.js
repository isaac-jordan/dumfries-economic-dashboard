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
        barHeight = 10;

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
    var dates=$('input[name="daterange"]').val();//get daterangepicker's value
    var end_date = dates.slice(-4);
    
    var start_date =dates.substring(6,10);
    var clean_data=[];
    for (var i=0;i<data.length;i++) {
     clean_data[i] = [];
  }
    
    for (i=0; i<data.length; i++) {
	for (d=0;d<data[i].length; d++) {
		if(data[i][d].x<=end_date && data[i][d].x>=start_date) {
			clean_data[i].push(data[i][d]);
		}
	}

    }
    if (clean_data[0].length==0 ) {
	return;}
    $("#" + elemID).empty();
    var xMin = clean_data[0][0].x, xMax = clean_data[0][0].x, yMin = clean_data[0][0].y, yMax = clean_data[0][0].y;
    var xMinCurr, xMaxCurr, yMinCurr, yMaxCurr;
    var x=0;
    for (x=0;x<clean_data.length;x++){
	    for (i=0; i<clean_data[x].length; i++) {
		xMinCurr = clean_data[x][i].x;
		xMaxCurr = clean_data[x][i].x;
		yMinCurr = clean_data[x][i].y;
		yMaxCurr = clean_data[x][i].y;

		if (xMinCurr < xMin) xMin = xMinCurr;
		if (xMaxCurr > xMax) xMax = xMaxCurr;
		if (yMinCurr < yMin) yMin = yMinCurr;
		if (yMaxCurr > yMax) yMax = yMaxCurr;
	    }
    }
    var WIDTH = $("#" + elemID).parent().width(),
        colours = ['#00264d', ' #0064cc' , '#0066cc',' #3399ff',' #fff'],
        HEIGHT = 250,
        MARGINS = {
            top: 30,
            right: 30,
            bottom: 30,
            left: 30
        },
        xScale = d3.scale.linear().range([MARGINS.left, WIDTH - MARGINS.right]).domain([xMin, xMax]),
        yScale = d3.scale.linear().range([HEIGHT - MARGINS.top, MARGINS.bottom]).domain([yMin, yMax]),
        xAxis = d3.svg.axis()
            .scale(xScale)
            .tickFormat(d3.format(xAxis)),
        yAxis = d3.svg.axis()
            .scale(yScale)
            .orient("left"),
        vis = d3.select("#" + elemID).attr("width", WIDTH).attr("height", HEIGHT);
    
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
        
    xScale = d3.scale.linear().range([MARGINS.left, WIDTH - MARGINS.right]).domain([xMin, xMax]);
    yScale = d3.scale.linear().range([HEIGHT - MARGINS.top, MARGINS.bottom]).domain([yMin, yMax]);
    xAxis = d3.svg.axis()
        .scale(xScale)
        .tickFormat(d3.format("date"))
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

    vis.append("text")
           .attr("text-anchor", "middle")  // this makes it easy to centre the text as the transform is applied to the anchor
           .attr("transform", "translate("+ (WIDTH/2) +","+((HEIGHT+10)-(MARGINS.bottom/3))+")")  // centre below axis
           .text("Year");



    var lineGen = d3.svg.line()
        .x(function(d) {
            return xScale(d.x);
        })
        .y(function(d) {
            return yScale(d.y);
        })
        .interpolate("basis");
        
    for (i=0; i<clean_data.length; i++) {
        vis.append('svg:path')
        .attr('d', lineGen(clean_data[i]))
        .attr('stroke', colours[i])
        .attr('stroke-width', 2)
        .attr('fill', 'none');
    }
    
}

 
