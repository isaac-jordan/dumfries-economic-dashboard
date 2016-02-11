var applyDatePickerStats=function(){
	$('.daterange').daterangepicker({
	    locale: { cancelLabel: 'Clear' },
	    "showDropdowns": true,
	    "showWeekNumbers": true,
	    "autoApply": true,
	    "maxDate":"+10Y",//Works, don't know why, but it does !
	    "autoUpdateInput": true,
	    "startDate": "01/01/1990",
	    "endDate": new Date(),
	    "opens": "left"
	}, function(start, end, label) {
	  console.log("New date range selected: ' + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD') + ' (predefined range: ' + label + ')");
	});
	$('.daterange').on('apply.daterangepicker', function(ev, picker) {
	  drawAllGraphs();
	});
};
