
// GAUGE CHARTS: TEMPERATURE, HUMIDITY AND PRESION
function myGaugeCharts (pressure) {
    var updateInterval = $("#id_select_interval").val();
    var apirest_temperature = $("#apirest_temperature").attr("data-value");
    var apirest_humidity = $("#apirest_humidity").attr("data-value");
    var apirest_pressure = $("#apirest_pressure").attr("data-value");

    google.charts.load('current', {'packages': ['gauge']});
    google.charts.setOnLoadCallback(drawChartTemperature);
    google.charts.setOnLoadCallback(drawChartHumidity);
    if (pressure) {
        google.charts.setOnLoadCallback(drawChartPressure);
    }

    function drawChartTemperature() {
        var idElement = "chart_gauge_temp";

        var data = google.visualization.arrayToDataTable([
             ['Label', 'Value'],
             ['ºC', 20]
            ]);
        var options = {
            greenFrom: 10, greenTo: 40,
            redFrom: 40, redTo: 50,
            yellowFrom: 30, yellowTo: 40,
            majorTicks: [10,20,30,40,50],
            minorTicks: 5,
            max: 50
        };
        var chart = new google.visualization.Gauge(document.getElementById(idElement));

        setInterval(function() {
            $.getJSON(apirest_temperature, function(result) {
                data.setValue(0,1,result.result.toFixed(2));
                chart.draw(data, options);
                // console.log("Temperature " + result.Temperature.toFixed(2));
                return true;
            })
        }, updateInterval);
    }

    function drawChartHumidity() {
        var data = google.visualization.arrayToDataTable([
            ['Label', 'Value'],
            ['%H', 20],
        ]);
        var options = {
            greenFrom: 40, greenTo:60,
            minorTicks: 5
        };
        var chart = new google.visualization.Gauge(document.getElementById('chart_gauge_humidity'));

        setInterval(function() {
            $.getJSON(apirest_humidity, function(result) {
                data.setValue(0,1,result.result.toFixed(2));
                chart.draw(data, options);
                // console.log("Humidity " + result.Humidity.toFixed(2));
                return true;
            })
        }, updateInterval);
    }

    function drawChartPressure() {
        var data = google.visualization.arrayToDataTable([
             ['Label', 'Value'],
             ['mbar', 20],
            ]);
        var options = {
            minorTicks: 5,
            max: 2000
        };
        var chart = new google.visualization.Gauge(document.getElementById('chart_gauge_pressure'));

        setInterval(function() {
            $.getJSON(apirest_pressure, function(result) {
                data.setValue(0,1,result.result.toFixed(2));
                chart.draw(data, options);
                // console.log("Humidity " + result.Pressure.toFixed(2));
                return true;
            })
        }, updateInterval);
    }
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

function graphiteSerialChart (target, daysFrom, idElement, dygraphAttrs) {
    this.target = target;
    this.idElement = idElement;
    this.dygraphAttrs = dygraphAttrs;
    var url = target + "&format=json&from=" + daysFrom + "d&jsonp=?";
    var chart;

    plot(url, this.idElement, this.dygraphAttrs);

    function plot (graphiteUrl,idElement,dygraphAttrs) {
        $("#" + idElement).html("<p><i class=\"fa fa-spinner fa-pulse fa-3x fa-fw\"></i> Cargando Datos...</p>");
        $.getJSON(graphiteUrl, function (response) {
            var data = [];
            for (i in response[0].datapoints) {
                data.push([new Date(response[0].datapoints[i][1] * 1000), response[0].datapoints[i][0]]);
            }
            $("#"+idElement).removeClass("loader");
            chart = new Dygraph(document.getElementById(idElement), data, dygraphAttrs);
        });
    }

    this.replot = function(daysFrom) {
        var url = this.target + "&format=json&from=" + daysFrom + "d&jsonp=?";
        chart.destroy();
        plot(url, this.idElement, this.dygraphAttrs);
    }
}
