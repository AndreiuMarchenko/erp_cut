var options = {
	chart: {
		height: 320,
		type: 'line',
		stacked: false,
		toolbar: {
			show: false,
		},
	},
	dataLabels: {
		enabled: false
	},
	series: [{
		name: 'Orders',
		type: 'column',
		data: [4, 2, 2, 5, 6, 8, 8, 7]
	},{
		name: 'Sales',
		type: 'column',
		data: [2, 3, 1, 4, 5, 9, 5, 8]
	},{
		name: 'Revenue',
		type: 'line',
		data: [20, 10, 15, 36, 44, 45, 50, 58]
	}],
	stroke: {
		width: [1, 1, 3]
	},
	title: {
		text: 'Overall income in millon dollors form online and offline sales from 2010 to 2018.',
		align: 'center',
	},
	colors: ['#af772b', '#da9d46', '#e0ac69', '#f1c17d', '#ffdbac'],
	xaxis: {
		categories: [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018],
	},
	yaxis: [{
		axisTicks: {
			show: true,
		},
		axisBorder: {
			show: true,
			color: '#af772b'
		},
		labels: {
			style: {
				color: '#af772b',
			}
		},
		title: {
			text: "Orders (in thousands)",
			style: {
				color: '#af772b',
			}
		},
		tooltip: {
			enabled: true
		}
	},{
			seriesName: 'Orders',
			opposite: true,
			axisTicks: {
				show: true,
			},
			axisBorder: {
				show: true,
				color: '#da9d46'
			},
			labels: {
				style: {
					color: '#da9d46',
				}
			},
			title: {
				text: "Sales (in thousand)",
				style: {
					color: '#da9d46',
				}
			},
		},{
			seriesName: 'Revenue',
			opposite: true,
			axisTicks: {
				show: true,
			},
			axisBorder: {
				show: true,
				color: '#333333'
			},
			labels: {
				style: {
					color: '#333333',
				},
			},
			title: {
				text: "Revenue (in crores)",
				style: {
					color: '#333333',
				}
			}
		},
	],
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
	legend: {
		horizontalAlign: 'center',
		offsetY: -5
	}
}

var chart = new ApexCharts(
	document.querySelector("#multiple-yaxis"),
	options
);
chart.render();