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
    var HEIGHT=0;
    if ($("#" + elemID).parent().parent().parent().height()-90>1000){
        HEIGHT = 300;
    }else{
        HEIGHT = $("#" + elemID).parent().parent().parent().height()-90;
    }
    data = data[0];
    $("#" + elemID).empty();
    var width = $("#" + elemID).parent().width(),
        barHeight =  HEIGHT/data.length;

    var x = d3.scale.linear()
        .domain([0, d3.max(data, function(d) {return d.y;})])
        .range([0, width - 5]);

    var chart = d3.select("#" + elemID)
        .attr("width", width)
        .attr("height", HEIGHT);

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
        .attr("height", barHeight - 1)
        .on("mouseover", function() {                   //on mouseover the bar is highlighted with light blue
            d3.select(this).classed("highlight", true);
        })
        .on("mouseout", function() {
            d3.select(this).classed("highlight", false);
        });


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
function add_Trend_Element(elemID){
    var vis = d3.select("#" + elemID);
	vis.append("text")
           .attr("text-anchor", "middle")  // this makes it easy to centre the text as the transform is applied to the anchor
           .attr("transform", "translate("+ ($("#" + elemID).width()-100) +","+(($("#" + elemID).height()-250))+")")  // centre below axis
           .text("Highest Value was : 500")
	   .append('svg:tspan')
	   .attr('x', -40)
	   .attr('dy', 15)
	   .text("Now is : 300")
       .append('svg:tspan')
	        .attr('x', -40)
	        .attr('dy', 15)
	        .text("Lowest was : 100");
}
function cleanup_data(data, type, clean_data){
	var dates=$('input[name="daterange"]').val();//get daterangepicker's value
	var end_date=new Date();
	var start_date=new Date();
	var i,d, c_date, input;
	
	if (dates) {
	    var e_date = dates.slice(-4);
	    end_date.setYear(e_date);
	    
	    var s_date =dates.substring(6,10);
        start_date.setYear(s_date);
	} else {
	    start_date.setYear(1900);
	    end_date.setYear(2100);
	}
	
	if (type=="normal"){
    	for (i=0; i<data.length; i++) {
	    	for (d=0;d<data[i].length; d++) {
			c_date=new Date();
			c_date.setYear(data[i][d].x);
	    		if(c_date<=end_date && c_date>=start_date) {
					input={};
					input.x=c_date;
					input.y=data[i][d].y;
		    		clean_data[i].push(input);
	    		}
	    	}
		}
	} else {
		for (i=0; i<data.length; i++) {
		    	for (d=0;d<data[i].length; d++) {
				    c_date=new Date(data[i][d].x);
		    		if(c_date<=end_date && c_date>=start_date) {
    					input={};
    					input.x=c_date;
    					input.y=data[i][d].y;
		    			clean_data[i].push(input);
		    		}
		    	}
    		}
	}
	
	return clean_data;
}
function add_legend(elemID,vis,data,colours){

    for (i=0;data[i]!=null ;i++) {
        vis.append("rect")
            .attr("width",30)
            .attr("height",10)
            .attr("x",50)
            .attr("y",10)
            .attr("dy","0.35em")
            .attr('fill',colours[i]);
    }
}
function linegraph(elemID, data) {
    var vis;
    var c_data=data;//Copy of our data given in
    var type="normal";
    var clean_data=[];
    $("#" + elemID).empty();// Clean previous graph in widget
    for (var i=0;i<data.length;i++) {
     clean_data[i] = [];
    }
    if (!data[0][0]) return;
    if (typeof(data[0][0].x)=="string") type="date_format"; //Temporary solution for the different date formats

    clean_data=cleanup_data(c_data,type,clean_data);// Sends a copy of our data to be filtered and converts dates to JS Date format
    if (clean_data[0].length === 0 ) { //It does not add the text !!
    	vis = d3.select("#" + elemID).attr('width', $("#" + elemID).parent().width()).attr('height', 270);
    	vis.append("text")
           .attr("text-anchor", "middle")  // this makes it easy to centre the text as the transform is applied to the anchor
           .attr('x',$("#" + elemID).width()/2)
           .attr('y',$("#" + elemID).height()/2)
           .text("No information available for these dates");
    	return;
	}

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
    var HEIGHT=0;
    if ($("#" + elemID).parent().parent().parent().height()-90>1000){
        HEIGHT = 300;
    }else{
        HEIGHT = $("#" + elemID).parent().parent().parent().height()-90;
    }
     var WIDTH = $("#" + elemID).parent().width(),
        colours = ['#00264d', ' #0064cc' , '#0066cc',' #3399ff',' #fff'],

        MARGINS = {
            top: 40,
            right: 40,
            bottom: 40,
            left: 50
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

	}else if(type!="normal"){
        xScale = d3.scale.linear().range([MARGINS.left, WIDTH - MARGINS.right]).domain([xMin, xMax+1]);
        yScale = d3.scale.linear().range([HEIGHT - MARGINS.top, MARGINS.bottom]).domain([yMin, yMax]);
    }
    if (type!="normal") {}
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
            return xScale(d.x.getFullYear()+(d.x.getMonth()-1)/12);
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
    //add_legend(elemID,vis,clean_data,colours)
}

 
