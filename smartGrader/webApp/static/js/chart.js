import { Chart } from "chart.js";
import ChartDataLabels from "chartjs-plugin-datalabels";
import "chartjs-plugin-labels";

// Chart.js gauge

var data = [40, 70, 100];
var value = 76;

var config = {
  type: "gauge",
  data: {
    labels: ["Normal", "Warning", "Critical"],
    datasets: [
      {
        label: "Current Appeal Risk",
        data: data,
        value: value,
        minValue: 0,
        backgroundColor: ["green", "orange", "red"],
        borderWidth: 2
      }
    ]
  },
  options: {
    legend: {
      display: true,
      position: "bottom",
      labels: {
        generateLabels: {}
      }
    },
    responsive: true,
    title: {
      display: true,
      text: "Financial Risk"
    },
    layout: {
      padding: {
        bottom: 20
      }
    },
    needle: {
      radiusPercentage: 1,
      widthPercentage: 1,
      lengthPercentage: 60,
      color: "rgba(0, 0, 0, 1)"
    },
    valueLabel: {
      fontSize: 12,
      formatter: function (value, context) {
        return value + "X";
      }
    },
    plugins: {
      datalabels: {
        display: "auto",
        formatter: function (value, context) {
          return context.chart.data.labels[context.dataIndex];
        },
        color: function (context) {
          return "white";
        },
        font: function (context) {
          var innerRadius = Math.round(context.chart.innerRadius);
          var size = Math.round(innerRadius / 8);
          return {
            weight: "normal",
            size: size
          };
        }
      }
    }
  }
};

// Initialize the chart
var ctx4 = document.getElementById("gaugeChart").getContext("2d");
var myGauge = new Chart(ctx4, config);
myGauge.update();