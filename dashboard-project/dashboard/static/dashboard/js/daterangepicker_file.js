var applyDatePickerStats=function(){
	$('.daterange').daterangepicker({
	    locale: { cancelLabel: 'Clear' },
	    "showDropdowns": true,
	    "showWeekNumbers": true,
	    "autoApply": true,
	    "maxDate":"+10Y",//Works, don't know why, but it does !
	    "autoUpdateInput": true,
	    "startDate": "01/13/2010",
	    "endDate": "01/19/2016",
	    "opens": "left"
	}, function(start, end, label) {
	  console.log("New date range selected: ' + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD') + ' (predefined range: ' + label + ')");
	});
	$('.daterange').on('apply.daterangepicker', function(ev, picker) {
	  console.log(picker.startDate.format('YYYY-MM-DD'));
	  console.log(picker.endDate.format('YYYY-MM-DD'));
	  drawAllGraphs();
	  drawCategoryGraphs();
	});
};
