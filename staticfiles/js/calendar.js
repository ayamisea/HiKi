//日曆
$( function() {
	$( "#datepicker" ).datepicker({
		dateFormat: 'yy-mm-dd',
		minDate: new Date(2014, 6 - 1, 5),
		maxDate: "0",
		changeMonth: true,
		changeYear: true,
		showButtonPanel: true,
	});
});