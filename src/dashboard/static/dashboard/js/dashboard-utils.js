// GAUGE CHARTS: TEMPERATURE, HUMIDITY AND PRESION

google.charts.load('current', {'packages':['gauge']});

google.charts.setOnLoadCallback(drawChartTemperature);
google.charts.setOnLoadCallback(drawChartHumidity);
google.charts.setOnLoadCallback(drawChartPressure);

var updateInterval = 2000;

function drawChartTemperature() {
    var data = google.visualization.arrayToDataTable([
         ['Label', 'Value'],
         ['T (ºC)', 20]
        ]);
    var options = {
        greenFrom: 10, greenTo: 40,
        redFrom: 40, redTo: 50,
        yellowFrom: 30, yellowTo: 40,
        majorTicks: [10,20,30,40,50],
        minorTicks: 5,
        max: 50
    };
    var chart = new google.visualization.Gauge(document.getElementById('chart_gauge_temp'));

    setInterval(function() {
        $.getJSON("api/v1/env_sensors/temperature/", function(result) {
            data.setValue(0,1,result.Temperature.toFixed(2));
            chart.draw(data, options);
            // console.log("Temperature " + result.Temperature.toFixed(2));
            return true;
        })
    }, updateInterval);
}

function drawChartHumidity() {
    var data = google.visualization.arrayToDataTable([
        ['Label', 'Value'],
        ['H (%)', 20],
    ]);
    var options = {
        greenFrom: 40, greenTo:60,
        minorTicks: 5
    };
    var chart = new google.visualization.Gauge(document.getElementById('chart_gauge_humidity'));

    setInterval(function() {
        $.getJSON("api/v1/env_sensors/humidity/", function(result) {
            data.setValue(0,1,result.Humidity.toFixed(2));
            chart.draw(data, options);
            // console.log("Humidity " + result.Humidity.toFixed(2));
            return true;
        })
    }, updateInterval);
}

function drawChartPressure() {
    var data = google.visualization.arrayToDataTable([
         ['Label', 'Value'],
         ['Presión', 20],
        ]);
    var options = {
        minorTicks: 5,
        max: 2000
    };
    var chart = new google.visualization.Gauge(document.getElementById('chart_gauge_pressure'));

    setInterval(function() {
        $.getJSON("api/v1/env_sensors/pressure/", function(result) {
            data.setValue(0,1,result.Pressure.toFixed(2));
            chart.draw(data, options);
            // console.log("Humidity " + result.Pressure.toFixed(2));
            return true;
        })
    }, updateInterval);
}

// chartName: Chart to print, one of the charts in chartsOptions
// htmlElementId: The id name of the HTML Element where the chart is plotted.
// updateInterval: Refresh Interval.
// chartsOptions, format example:
//{
//  'temperature': {
//      url: "{{ API_REST_URL }}env_sensors/temperature", labels: ['t', 'Temperatura'],
//      ylabel: "Temperatura (ºC)", key: "Temperature"
//   },
//   'humidity': {
//      url: "{{ API_REST_URL }}env_sensors/humidity", labels: ['h', 'Humedad'],
//      ylabel: "Humedad (%)", key: "Humidity"
//   },
//   'pressure': {
//      url: "{{ API_REST_URL }}env_sensors/pressure", labels: ['p', 'Presión'],
//      ylabel: "Presión", key: "Pressure"
//   }
//};
function serialChart(chartName, htmlElementId, updateInterval, chartsOptions) {
    var data = [];
    this.chartName = chartName;
    this.divIdChart = htmlElementId;
    this.refreshInterval = updateInterval;
    this.intervalId;
    var url = chartsOptions[this.chartName]['url'];

    // Initializing data
    // FIXME: Why this code is executed after new Dygraph?
    $.getJSON(url, function (result) {
        var x = new Date();
        var y = result[chartsOptions[chartName]['key']];
        data.push([x, y]);
        return true;
    });

    var chart = new Dygraph(this.divIdChart, data, {
        drawPoints: false,
        showRoller: false,
        labels: [chartsOptions[this.chartName]['labels'][0], chartsOptions[this.chartName]["labels"][1]],
        legend: 'always',
        ylabel: chartsOptions[this.chartName]['ylabel']
    });

    this.plot = function () {

        // Cuidado en el contexto de setInterval this es el objeto Windows
        this.intervalId = setInterval(function () {
            $.getJSON(url, function (result) {
                var x = new Date();
                var y = result[chartsOptions[chartName]['key']].toFixed(2);
                data.push([x, y]);
                chart.updateOptions({'file': data});
                return true;
            })
        }, this.refreshInterval);
    };

    this.replot = function () {
        clearInterval(this.intervalId)
        this.plot();
    };

    this.plot();
}
