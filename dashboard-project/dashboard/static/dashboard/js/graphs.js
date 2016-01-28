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
function reconstruct_data(data){
	
}
function cleanup_data(data,type,clean_data){
	var dates=$('input[name="daterange"]').val();//get daterangepicker's value
	var e_date = dates.slice(-4);
	var end_date=new Date();
	end_date.setYear(e_date);
	var s_date =dates.substring(6,10);
	var start_date=new Date();
	start_date.setYear(s_date);
	if (type=="normal"){
		for (i=0; i<data.length; i++) {
		    	for (i=0; i<data.length; i++) {
			    	for (var d=0;d<data[i].length; d++) {
					var c_date=new Date();
					c_date.setYear(data[i][d].x);
			    		if(c_date<=end_date && c_date>=start_date) {
						var input={};
						input["x"]=c_date;
						input["y"]=data[i][d].y;
						
			    			clean_data[i].push(input);
			    		}
			    	}
    			}
	    	}
	}else{
		for (i=0; i<data.length; i++) {
		    	for (var d=0;d<data[i].length; d++) {
		    		if(data[i][d].x<=end_date && data[i][d].x>=start_date) {
					var date_c=new Date(data[i][d].x);
					var input={};
					input["x"]=date_c;
					input["y"]=data[i][d].y;
		    			clean_data[i].push(input);
		    		}
		    	}
    		}
	}
	return clean_data;
}

function linegraph(elemID, data) {
    var dates=$('input[name="daterange"]').val();//get daterangepicker's value
    var end_date = dates.slice(-4);
    var start_date =dates.substring(6,10);
    var c_data=data;//Copy of our data given in
    var type="normal";
    var clean_data=[];
    for (var i=0;i<data.length;i++) {
     clean_data[i] = [];
  }
    if (typeof(data[0][0].x)=="string") type="date_format"//Temporary solution for the different date formats
    
    clean_data=cleanup_data(c_data,type,clean_data);// Sends a copy of our data to be filtered and converts dates to JS Date format
    if (clean_data[0].length == 0 ) { //It does not add the text !!
    	vis = d3.select("#" + elemID)
    		.attr('width', $("#" + elemID).parent().width())
                	.attr('height', 300)
    		.append('text')
    			.attr('text','No information is available for these dates')
    			.attr('x', 3)
        			.attr('y', 15);
    	return;
	}
    $("#" + elemID).empty();// Clean previous graph in widget
    
    var xMin = clean_data[0][0].x, xMax = clean_data[0][0].x, yMin = clean_data[0][0].y, yMax = clean_data[0][0].y;
    var xMinCurr, xMaxCurr, yMinCurr, yMaxCurr;
    var x=0;

    //Date comparison to find min and max values
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
	//For now just get the year value
	xMin=xMin.getFullYear();
	xMax=xMax.getFullYear();
	
     var WIDTH = $("#" + elemID).parent().width(),
        colours = ['#00264d', ' #0064cc' , '#0066cc',' #3399ff',' #fff'],
        HEIGHT = 300,
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
            .orient("left");
        vis = d3.select("#" + elemID).attr("width", WIDTH).attr("height", HEIGHT);
    /**var maxw = 0;
    vis.append("svg:g")
        .attr("class", "y axis")
        .attr("transform", "translate(" + MARGINS.left + ",0)")
        .call(yAxis)
        .selectAll("text").each(function() {
            if(this.getBBox().width > maxw) {
                maxw = this.getBBox().width;
                MARGINS.left = Math.max(MARGINS.left, maxw + 10);
            }
        });*/
    xScale = d3.scale.linear().range([MARGINS.left, WIDTH - MARGINS.right]).domain([xMin, xMax]);
    yScale = d3.scale.linear().range([HEIGHT - MARGINS.top, MARGINS.bottom]).domain([yMin, yMax]);
    if (clean_data[0].length==1) {// In case of 1 element margin domain changes 
	xScale = d3.scale.linear().range([MARGINS.left, WIDTH - MARGINS.right]).domain([xMin-1, xMax+1]);
    	yScale = d3.scale.linear().range([HEIGHT - MARGINS.top, MARGINS.bottom]).domain([yMax/2, yMax*2]);
	}
    xAxis = d3.svg.axis()
        .scale(xScale)
        .tickFormat(d3.format("date"));
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
            return xScale(d.x.getFullYear());
        })
        .y(function(d) {
            return yScale(d.y);
        })
        .interpolate("basis");
     //In case of 1 element we append a circle with just a text
     if (clean_data[0].length==1){
	vis.append('circle')
	   .attr("cx", WIDTH/2)
           .attr("cy", HEIGHT/2+40)                         
	   .attr("r", 10);
	  vis.append('text')
	   .attr("transform", "translate("+ (WIDTH/2-40) +","+((HEIGHT/2-40))+")")  // centre below axis
	   .text(clean_data[0][0].y+" for "+clean_data[0][0].x.getFullYear()); 
	return;
	}
    for (i=0; i<clean_data.length; i++) {
        vis.append('svg:path')
        .attr('d', lineGen(clean_data[i]))
        .attr('stroke', colours[i])
        .attr('stroke-width', 2)
        .attr('fill', 'none');
    }
}

 
