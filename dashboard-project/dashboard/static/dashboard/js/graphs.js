/*jshint*/
/*global d3, console, GLOBAL */

function drawGraph(elemID, data, type,datasetLabels,xLabel,yLabel) {
    if ($("#" + elemID).parent().width() < 0) return;
    switch(type) {
        case "bar":
            bargraph(elemID, data,xLabel,yLabel);
            break;
        case "line":
            linegraph(elemID, data,datasetLabels,xLabel,yLabel);
            break;
    }
}

function bargraph(elemID, data,xLabel,yLabel) {
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
        .attr("fill","white")
        .attr("x", function (d) {
            return x(d.y) - 3;
        })
        .attr("y", barHeight / 2)
        .attr("dy", ".35em")
        .text(function (d) {
            return (d.x+" "+d.y);
        });
    //console.log(yLabel);
}

function cleanup_data(data, type, clean_data){
    var end_date = GLOBAL.endDateRange;
    var start_date = GLOBAL.startDateRange;
    var i,d, c_date, input;

    if (!end_date || !start_date) {
        start_date = new Date();
        start_date.setYear(1900);
        
        end_date = new Date();
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

function add_legend(elemID,vis,data,colours,datasetLabels,MARGINS){
    var y=0;

    for (var i=0; data[i] !== null && i < data.length; i++) {;
        vis.append("rect")
            .attr("width",30)
            .attr("height",12)
            .attr("x",MARGINS.left)
            .attr("y",y)
            .attr("dy","-3.5em")
            .attr('fill',colours[i]);
        vis.append("text")
            .attr("x",MARGINS.left+40)
            .attr("y",y+12)
            .text(datasetLabels[i]);
        y+=17;
    }
}
function linegraph(elemID, data,datasetLabels,xLabel,yLabel) {
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
    //console.log("Finished cleanup.");
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
    //console.log("Starting date comparison.");
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
    //console.log("Finished date comparison.");
    //For now just get the year value
    xMin=xMin.getFullYear();
    xMax=xMax.getFullYear();

    //console.log("Starting d3 code.");
    var HEIGHT=0;
    if ($("#" + elemID).parent().parent().parent().height()-90>1000){
        HEIGHT = 300;
    }else{
        HEIGHT = $("#" + elemID).parent().parent().parent().height()-90;
    }
    var WIDTH = $("#" + elemID).parent().width(),
        colours = ['#00264d', ' #0064cc' , '#0066cc',' #3399ff',' #fff'],

        MARGINS = {
            top: 30,
            right: 5,
            bottom: data.length*10+10,
            left: 60
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

    xScale = d3.scale.linear().range([MARGINS.left, WIDTH - MARGINS.right]).domain([xMin, xMax]);
    yScale = d3.scale.linear().range([HEIGHT - MARGINS.top, MARGINS.bottom]).domain([yMin, yMax]);
    if (clean_data[0].length==1) {// In case of 1 element margin domain changes
        xScale = d3.scale.linear().range([MARGINS.left, WIDTH - MARGINS.right]).domain([xMin-1, xMax+1]);
        yScale = d3.scale.linear().range([HEIGHT - MARGINS.top, MARGINS.bottom]).domain([yMax/2, yMax*2]);

    }else if(type!="normal"){
        xScale = d3.scale.linear().range([MARGINS.left, WIDTH - MARGINS.right]).domain([xMin, xMax+1]);
    }
    if (type!="normal") {}
    var datelength=xMax-xMin;
    xAxis = d3.svg.axis()
        .scale(xScale)
        .tickFormat(d3.format("date"))
        .orient("bottom")
        .ticks((WIDTH-90)/30);
    yAxis = d3.svg.axis()
        .scale(yScale)
        .orient("left");

    vis.append("svg:g")
        .attr("class", "y axis")
        .attr("transform", "translate(" + MARGINS.left + ",0)")
        .call(yAxis);

    vis.append("svg:g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + (HEIGHT - MARGINS.top) + ")")
        .call(xAxis);




    var lineGen = d3.svg.line()
        .x(function(d) {
            return xScale(d.x.getFullYear()+(d.x.getMonth())/12);
        })
        .y(function(d) {
            return yScale(d.y);
        });
    
    var div = d3.select("body")
        .append("div")
        .attr("class", "tooltip")
        .style("opacity", 0);
    
    var bisectDate = d3.bisector(function(d) { return d.y; }).left;
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
    
    var focus = vis.append("g")
        .attr("class", "focus")
        .style("display", "none");

    focus.append("circle")
        .attr("r", 4.5);

    focus.append("text")
        .attr("x", 9)
        .attr("dy", ".35em");
    
    //console.log("Starting last clean_data loop");
    for (i=0; i<clean_data.length; i++) {
        vis.append('svg:path')
            .attr('d', lineGen(clean_data[i]))
            .attr('stroke', colours[i])
            .attr('stroke-width', 2)
            .attr('fill', 'none')
            .on("mousemove", function(d) {
                        div.transition()
                            .duration(10)
                            .style("opacity", 1)
                            .delay(1000)
                            .style("opacity",0);
                    })
            .on("mouseover", mousemove);
    }
    //console.log("Finished last clean_data loop");

    function kiklos() {
        for (var a = 0; a < clean_data.length; a++) {
            for (var i = 0; i < clean_data[a].length; i++) {
                vis.append('circle')
                    .attr("cx", xScale(clean_data[a][i].x.getFullYear()+(clean_data[a][i].x.getMonth())/12))
                    .attr("cy", yScale(clean_data[a][i].y))
                    .attr("r", 4.5);
            }
        }
    }
    
    function mousemove() {
        var a = 0;
        for (a = 0; a < clean_data.length; a++) {

            var x0 = xScale.invert(d3.mouse(this)[0]).toFixed(0);
            var y = yScale.invert(d3.mouse(this)[1]).toFixed(0),
                i = bisectDate(clean_data, x0, a),
                d0 = clean_data[i - 1],
                d1 = clean_data[i + a],
                d = x0 - d0 > d1 - x0 ? d1 : d0;
            //console.log(yLabel);
            var x2 = Math.round(xScale(x0));
            var y2 = Math.ceil(y / 10) * 10;
            div.transition()
                .duration(10)
                .style("opacity",0.9);
            div.html(yLabel+"<b/>" +": " + y+  "<br/>"  + xLabel +": " +x0)

                .style("left", (d3.event.pageX) + "px")
                .style("top", (d3.event.pageY - 28) + "px");


            /*vis.append('circle')
             .attr('fill', "transparent")
             .attr('stroke', colours[i])
             .attr('stroke-width', 2)
             .attr("cx", xScale(x0) )
             .attr("cy",yScale(y2) )

             .attr("r", 3.5);      }
             */
        }
    }
    
    //console.log("Adding legend");
    if(datasetLabels){
        add_legend(elemID,vis,clean_data,colours,datasetLabels,MARGINS);
    }
    //console.log("Finished adding legend");
    
    //console.log("Adding axis labels");
    add_axis_labels(vis,xLabel,yLabel,WIDTH,HEIGHT,MARGINS);
    //console.log("Finished adding axis labels");
    
    //console.log("Finished d3 code.");

}

function add_axis_labels(vis,xLabel,yLabel,WIDTH,HEIGHT,MARGINS){

    vis.append("text")
        .attr("text-anchor", "middle")  // this makes it easy to centre the text as the transform is applied to the anchor
        .attr("transform", "translate("+ 12 +","+((HEIGHT)/2)+")rotate("+270+")")  // centre below axis
        .text(yLabel);

    vis.append("text")
        .attr("text-anchor", "middle")  // this makes it easy to centre the text as the transform is applied to the anchor
        .attr("transform", "translate("+ (WIDTH/2) +","+((HEIGHT))+")")  // centre below axis
        .text(xLabel);
}


