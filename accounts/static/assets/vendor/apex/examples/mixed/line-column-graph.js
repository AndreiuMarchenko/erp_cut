var options = {
	chart: {
		height: 350,
		type: 'line',
		zoom: {
			enabled: false
		},
	},
	toolbar: {
		show: false
	},
	series: [{
		name: 'Website Blog',
		type: 'column',
		data: [440, 505, 414, 671, 227, 413, 201, 352, 752, 320, 257, 160]
	}, {
		name: 'Social Media',
		type: 'line',
		data: [23, 42, 35, 27, 43, 22, 17, 31, 22, 22, 12, 16]
	}],
	stroke: {
		width: [0, 4]
	},
	title: {
		text: 'Traffic Sources',
		align: 'center'
	},
	// labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
	labels: ['01 Jan 2001', '02 Jan 2001', '03 Jan 2001', '04 Jan 2001', '05 Jan 2001', '06 Jan 2001', '07 Jan 2001', '08 Jan 2001', '09 Jan 2001', '10 Jan 2001', '11 Jan 2001', '12 Jan 2001'],
	xaxis: {
		type: 'datetime'
	},
	colors: ['#af772b', '#333333', '#e0ac69', '#f1c17d', '#ffdbac'],
	grid: {
    borderColor: '#e0e6ed',
    strokeDashArray: 5,
    xaxis: {
      lines: {
        show: true
      }
    },   
    yaxis: {
      lines: {
        show: false,
      } 
    },
    padding: {
      top: 0,
      right: 0,
      bottom: 0,
      left: 0
    }, 
  },
	yaxis: [{
		title: {
			text: 'Website Blog',
		},
	},{
		opposite: true,
		title: {
			text: 'Social Media'
		}
	}]
}
var chart = new ApexCharts(
	document.querySelector("#line-column-graph"),
	options
);
chart.render();