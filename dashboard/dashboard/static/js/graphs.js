/**
 * Created by lewis on 12/11/15.
 */

(function () {

    var data = [4, 8, 15, 16, 23, 42];

    var width = 200,
        barHeight = 8.5;

    var x = d3.scale.linear()
        .domain([0, d3.max(data)])
        .range([0, width]);

    var chart = d3.select(".chart")
        .attr("width", width)
        .attr("height", barHeight * data.length);

    var bar = chart.selectAll("g")
        .data(data)
        .enter().append("g")
        .attr("transform", function (d, i) {
            return "translate(0," + i * barHeight + ")";
        });

    bar.append("rect")
        .attr("width", x)
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
})();

/* other graphs, TODO: figure out how to insert into different divs

 // LINE


 (function(){

 var margin = {top: 20, right: 20, bottom: 30, left: 50},
 width = 260 - margin.left - margin.right,
 height = 100 - margin.top - margin.bottom;

 var parseDate = d3.time.format("%d-%b-%y").parse;

 var x = d3.time.scale()
 .range([0, width]);

 var y = d3.scale.linear()
 .range([height, 0]);

 var xAxis = d3.svg.axis()
 .scale(x)
 .orient("bottom");

 var yAxis = d3.svg.axis()
 .scale(y)
 .orient("left");

 var line = d3.svg.line()
 .x(function(d) { return x(d.date); })
 .y(function(d) { return y(d.close); });

 var svg = d3.select("body").append("svg")
 .attr("width", width + margin.left + margin.right)
 .attr("height", height + margin.top + margin.bottom)
 .append("g")
 .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

 d3.tsv("data.tsv", function(error, data) {
 if (error) throw error;

 data.forEach(function(d) {
 d.date = parseDate(d.date);
 d.close = +d.close;
 });

 x.domain(d3.extent(data, function(d) { return d.date; }));
 y.domain(d3.extent(data, function(d) { return d.close; }));

 svg.append("g")
 .attr("class", "x axis")
 .attr("transform", "translate(0," + height + ")")
 .call(xAxis);

 svg.append("g")
 .attr("class", "y axis")
 .call(yAxis)
 .append("text")
 .attr("transform", "rotate(-90)")
 .attr("y", 6)
 .attr("dy", ".71em")
 .style("text-anchor", "end")
 .text("Price ($)");

 svg.append("path")
 .datum(data)
 .attr("class", "line")
 .attr("d", line);
 });

 })();

 // PIE

 (function() {
 'use strict';

 var dataset = [
 { label: 'Abulia', count: 10 },
 { label: 'Betelgeuse', count: 20 },
 { label: 'Cantaloupe', count: 30 },
 { label: 'Dijkstra', count: 40 }
 ];

 var width = 360;
 var height = 360;
 var radius = Math.min(width, height) / 2;

 var color = d3.scale.category20b();

 var svg = d3.select('#chart')
 .append('svg')
 .attr('width', width)
 .attr('height', height)
 .append('g')
 .attr('transform', 'translate(' + (width / 2) +
 ',' + (height / 2) + ')');

 var arc = d3.svg.arc()
 .outerRadius(radius);

 var pie = d3.layout.pie()
 .value(function(d) { return d.count; })
 .sort(null);

 var path = svg.selectAll('path')
 .data(pie(dataset))
 .enter()
 .append('path')
 .attr('d', arc)
 .attr('fill', function(d, i) {
 return color(d.data.label);
 });

 })();

 (function(){
 var margin = {top: 20, right: 20, bottom: 30, left: 40},
 width = 260 - margin.left - margin.right,
 height = 200 - margin.top - margin.bottom;

 /*
 * value accessor - returns the value to encode for a given data object.
 * scale - maps value to a visual display encoding, such as a pixel position.
 * map function - maps from data value to display value
 * axis - sets up axis

 // setup x
 var xValue = function(d) { return d.Calories;}, // data -> value
 xScale = d3.scale.linear().range([0, width]), // value -> display
 xMap = function(d) { return xScale(xValue(d));}, // data -> display
 xAxis = d3.svg.axis().scale(xScale).orient("bottom");

 // setup y
 var yValue = function(d) { return d["Protein (g)"];}, // data -> value
 yScale = d3.scale.linear().range([height, 0]), // value -> display
 yMap = function(d) { return yScale(yValue(d));}, // data -> display
 yAxis = d3.svg.axis().scale(yScale).orient("left");

 // setup fill color
 var cValue = function(d) { return d.Manufacturer;},
 color = d3.scale.category10();

 // add the graph canvas to the body of the webpage
 var svg = d3.select("body").append("svg")
 .attr("width", width + margin.left + margin.right)
 .attr("height", height + margin.top + margin.bottom)
 .append("g")
 .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

 // add the tooltip area to the webpage
 var tooltip = d3.select("body").append("div")
 .attr("class", "tooltip")
 .style("opacity", 0);

 // load data
 d3.csv("cereal.csv", function(error, data) {

 // change string (from CSV) into number format
 data.forEach(function(d) {
 d.Calories = +d.Calories;
 d["Protein (g)"] = +d["Protein (g)"];
 //    console.log(d);
 });

 // don't want dots overlapping axis, so add in buffer to data domain
 xScale.domain([d3.min(data, xValue)-1, d3.max(data, xValue)+1]);
 yScale.domain([d3.min(data, yValue)-1, d3.max(data, yValue)+1]);

 // x-axis
 svg.append("g")
 .attr("class", "x axis")
 .attr("transform", "translate(0," + height + ")")
 .call(xAxis)
 .append("text")
 .attr("class", "label")
 .attr("x", width)
 .attr("y", -6)
 .style("text-anchor", "end")
 .text("Calories");

 // y-axis
 svg.append("g")
 .attr("class", "y axis")
 .call(yAxis)
 .append("text")
 .attr("class", "label")
 .attr("transform", "rotate(-90)")
 .attr("y", 6)
 .attr("dy", ".71em")
 .style("text-anchor", "end")
 .text("Protein (g)");

 // draw dots
 svg.selectAll(".dot")
 .data(data)
 .enter().append("circle")
 .attr("class", "dot")
 .attr("r", 3.5)
 .attr("cx", xMap)
 .attr("cy", yMap)
 .style("fill", function(d) { return color(cValue(d));})
 .on("mouseover", function(d) {
 tooltip.transition()
 .duration(200)
 .style("opacity", .9);
 tooltip.html(d["Cereal Name"] + "<br/> (" + xValue(d)
 + ", " + yValue(d) + ")")
 .style("left", (d3.event.pageX + 5) + "px")
 .style("top", (d3.event.pageY - 28) + "px");
 })
 .on("mouseout", function(d) {
 tooltip.transition()
 .duration(500)
 .style("opacity", 0);
 });

 // draw legend
 var legend = svg.selectAll(".legend")
 .data(color.domain())
 .enter().append("g")
 .attr("class", "legend")
 .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

 // draw legend colored rectangles
 legend.append("rect")
 .attr("x", width - 18)
 .attr("width", 18)
 .attr("height", 18)
 .style("fill", color);

 // draw legend text
 legend.append("text")
 .attr("x", width - 24)
 .attr("y", 9)
 .attr("dy", ".35em")
 .style("text-anchor", "end")
 .text(function(d) { return d;})
 });
 })();
 */