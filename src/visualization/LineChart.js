class LineChart {
  constructor(series, canvas_width, canvas_height) {
    // Create the tag:
    this.canvas_tag =
      "<canvas width='" + canvas_width + "' height='" + canvas_height + "' ";
    this.canvas_tag += "></canvas>";
    // Append it to #elements
    this.canvas = $(this.canvas_tag)[0];
    $("#elements").append(this.canvas);
    // Create the context and the drawing controller:
    this.context = this.canvas.getContext("2d");

    // Prep the chart properties and series:
    this.datasets = [];
    for (let i in series) {
      let s = series[i];
      let new_series = {
        label: s.Label,
        borderColor: s.Color,
        backgroundColor: this.convertColorOpacity(s.Color),
        data: [],
      };
      this.datasets.push(new_series);
    }

    this.chartData = {
      labels: [],
      datasets: this.datasets,
    };

    this.chartOptions = {
      responsive: true,
      tooltips: {
        mode: "index",
        intersect: false,
      },
      hover: {
        mode: "nearest",
        intersect: true,
      },
      scales: {
        xAxes: [
          {
            display: true,
            scaleLabel: {
              display: true,
            },
            ticks: {
              maxTicksLimit: 11,
            },
          },
        ],
        yAxes: [
          {
            display: true,
            scaleLabel: {
              display: true,
            },
          },
        ],
      },
    };

    this.chart = new Chart(this.context, {
      type: "line",
      data: this.chartData,
      options: this.chartOptions,
    });
  }

  convertColorOpacity(hex) {
    if (hex.indexOf("#") != 0) {
      return "rgba(0,0,0,0.1)";
    }

    hex = hex.replace("#", "");
    r = parseInt(hex.substring(0, 2), 16);
    g = parseInt(hex.substring(2, 4), 16);
    b = parseInt(hex.substring(4, 6), 16);
    return "rgba(" + r + "," + g + "," + b + ",0.1)";
  }

  render(data) {
    this.chart.data.labels.push(control.tick);
    for (i = 0; i < data.length; i++) {
      this.chart.data.datasets[i].data.push(data[i]);
    }
    this.chart.update();
  }

  reset() {
    while (this.chart.data.labels.length) {
      this.chart.data.labels.pop();
    }
    this.chart.data.datasets.forEach(function (dataset) {
      while (dataset.data.length) {
        dataset.data.pop();
      }
    });
    this.chart.update();
  }
}
