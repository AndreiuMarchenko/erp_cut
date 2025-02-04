var options = {
  chart: {
    height: 300,
    type: 'bar',
    stacked: true,
    toolbar: {
      show: false
    },
    zoom: {
      enabled: true
    }
  },
  responsive: [{
    breakpoint: 480,
    options: {
      legend: {
        position: 'bottom',
        offsetX: -10,
        offsetY: 0
      }
    }
  }],
  plotOptions: {
    bar: {
      horizontal: false,
    },
  },
  dataLabels: {
    enabled: true
  },
  series: [{
    name: 'Product A',
    data: [44, 55, 41, 67, 22, 43]
  },{
    name: 'Product B',
    data: [13, 23, 20, 8, 13, 27]
  },{
    name: 'Product C',
    data: [11, 17, 15, 15, 21, 14]
  },{
    name: 'Product D',
    data: [21, 7, 25, 13, 22, 8]
  }],
  xaxis: {
    type: 'datetime',
    categories: ['01/01/2011 GMT', '01/02/2011 GMT', '01/03/2011 GMT', '01/04/2011 GMT', '01/05/2011 GMT', '01/06/2011 GMT'],
  },
  legend: {
    position: 'top',
    offsetY: 10
  },
  fill: {
    opacity: 1
  },
  grid: {
    borderColor: '#ffdee7',
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
  colors: ['#fd789b', '#ff8caa', '#ffa3bb', '#ffb9cb', '#ffd1dd'],
}
var chart = new ApexCharts(
  document.querySelector("#basic-column-stack-graph"),
  options
);
chart.render();


