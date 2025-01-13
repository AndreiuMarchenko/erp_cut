// Date Range
$('.datepicker').daterangepicker({
	singleDatePicker: true,
  startDate: moment().startOf('hour'),
  endDate: moment().startOf('hour').add(32, 'hour'),
  minDate: moment(),  
  locale: {
    format: 'DD/MM/YYYY'
  }
});
$('#datepicker-0').daterangepicker({
	singleDatePicker: true,
  autoUpdateInput: false,
  startDate: moment().startOf('day'),
  locale: {
	  format: 'DD/MM/YYYY'
  }
});


// Date Range Opens Left
$('.datepicker-opens-left').daterangepicker({
	singleDatePicker: true,
	opens: 'left',
  startDate: moment().startOf('hour'),
  endDate: moment().startOf('hour').add(32, 'hour'),
  locale: {
    format: 'DD/MM/YYYY'
  }
});



$('.datepicker-week-numbers').daterangepicker({
	singleDatePicker: true,
	showWeekNumbers: true,
  startDate: moment().startOf('hour'),
  endDate: moment().startOf('hour').add(32, 'hour'),
  locale: {
    format: 'DD/MM/YYYY'
  }
});



$('.datepicker-iso-week-numbers').daterangepicker({
	singleDatePicker: true,
	showISOWeekNumbers: true,
  startDate: moment().startOf('hour'),
  endDate: moment().startOf('hour').add(32, 'hour'),
  locale: {
    format: 'DD/MM/YYYY'
  }
});



$('.datepicker-time').daterangepicker({
	singleDatePicker: true,
	timePicker: true,
  startDate: moment().startOf('hour'),
  endDate: moment().startOf('hour').add(32, 'hour'),
  locale: {
    format: 'DD/MM/YYYY hh:mm A'
  }
});



$('.datepicker-time-24').daterangepicker({
	drops: 'up',
	singleDatePicker: true,
	timePicker: true,
	timePicker24Hour: true,
  startDate: moment().startOf('hour'),
  endDate: moment().startOf('hour').add(32, 'hour'),
  locale: {
    format: 'DD/MM/YYYY hh:mm A'
  }
});



$('.datepicker-time-seconds').daterangepicker({
	drops: 'up',
	singleDatePicker: true,
	timePicker: true,
	timePicker24Hour: true,
  startDate: moment().startOf('hour'),
  endDate: moment().startOf('hour').add(32, 'hour'),
  locale: {
    format: 'DD/MM/YYYY hh:mm:ss A'
  }
});



$('.datepicker-range').daterangepicker({
	drops: 'up',
	startDate: moment().startOf('hour'),
	endDate: moment().startOf('hour').add(32, 'hour'),
	locale: {
		format: 'DD/MM/YYYY'
	}
});



$('.datepicker-range-week-numbers').daterangepicker({
	drops: 'up',
	showWeekNumbers: true,
	opens: 'left',
	startDate: moment().startOf('hour'),
	endDate: moment().startOf('hour').add(32, 'hour'),
	locale: {
		format: 'DD/MM/YYYY'
	}
});



$('.datepicker-range-iso-week-numbers').daterangepicker({
	drops: 'up',
	opens: 'left',
	showWeekNumbers: true,
	showISOWeekNumbers: true,
	startDate: moment().startOf('hour'),
	endDate: moment().startOf('hour').add(32, 'hour'),
	locale: {
		format: 'DD/MM/YYYY'
	}
});



$('.datepicker-range-time').daterangepicker({
	drops: 'up',
	timePicker: true,
  startDate: moment().startOf('hour'),
  endDate: moment().startOf('hour').add(32, 'hour'),
  locale: {
    format: 'DD/MM/YYYY hh:mm A'
  }
});


$('.datepicker-range-time-24').daterangepicker({
	drops: 'up',
	timePicker: true,
	timePicker24Hour: true,
	opens: 'left',
  startDate: moment().startOf('hour'),
  endDate: moment().startOf('hour').add(32, 'hour'),
  locale: {
    format: 'DD/MM/YYYY hh:mm A'
  }
});



$('.datepicker-range-left').daterangepicker({
	opens: 'left',
	drops: 'up',
	startDate: moment().startOf('hour'),
	endDate: moment().startOf('hour').add(32, 'hour'),
	locale: {
		format: 'DD/MM/YYYY'
	}
});



$('.datepicker-range-right').daterangepicker({
	opens: 'right',
	drops: 'up',
	startDate: moment().startOf('hour'),
	endDate: moment().startOf('hour').add(32, 'hour'),
	locale: {
		format: 'DD/MM/YYYY'
	}
});



$('.datepicker-range-top-right').daterangepicker({
	opens: 'right',
	drops: 'up',
	startDate: moment().startOf('hour'),
	endDate: moment().startOf('hour').add(32, 'hour'),
	locale: {
		format: 'DD/MM/YYYY'
	}
});



$('.datepicker-range-top-left').daterangepicker({
	opens: 'left',
	drops: 'up',
	startDate: moment().startOf('hour'),
	endDate: moment().startOf('hour').add(32, 'hour'),
	locale: {
		format: 'DD/MM/YYYY'
	}
});



$('.datepicker-range-auto-apply').daterangepicker({
	autoApply: true,
	drops: 'up',
	opens: 'left',
	startDate: moment().startOf('hour'),
	endDate: moment().startOf('hour').add(32, 'hour'),
	locale: {
		format: 'DD/MM/YYYY'
	}
});


// Custom Date Range
$(function() {
	var start = moment().subtract(29, 'days');
	var end = moment();
	function cb(start, end) {
		$('.custom-daterange span').html(start.format('MMM D, YYYY') + ' - ' + end.format('MMM D, YYYY'));
	}
	$('.custom-daterange').daterangepicker({
		opens: 'left',
		startDate: start,
		endDate: end,
		ranges: {
			'Сьогодні': [moment(), moment()],
			'Вчора': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
			'Останні 7 днів': [moment().subtract(6, 'days'), moment()],
			'Останні 15 днів': [moment().subtract(14, 'days'), moment()],
			'Останній місяць': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')],
			'Останній рік': [moment().subtract(1, 'year').startOf('year'), moment().subtract(1, 'year').endOf('year')]
		}
	}, cb);
	cb(start, end);
});



// Custom Date Range
$(function() {
	var start = moment().subtract(29, 'days');
	var end = moment();
	function cb(start, end) {
		$('.custom-daterange2 span').html(start.format('MMM D, YYYY') + ' - ' + end.format('MMM D, YYYY'));
	}
	$('.custom-daterange2').daterangepicker({
		autoApply: true,
		opens: 'left',
		startDate: start,
		endDate: end,
		ranges: {
			'Сьогодні': [moment(), moment()],
			'Вчора': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
			'Останні 7 днів': [moment().subtract(6, 'days'), moment()],
			'Останні 15 днів': [moment().subtract(14, 'days'), moment()],
			'Останній місяць': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')],
			'З початку року': [moment().startOf('year'), moment()]
		}
	}, cb);
	cb(start, end);
});