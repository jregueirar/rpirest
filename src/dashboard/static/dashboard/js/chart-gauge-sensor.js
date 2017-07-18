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
            console.log("Temperature " + result.Temperature.toFixed(2));
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
            console.log("Humidity " + result.Humidity.toFixed(2));
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
            console.log("Humidity " + result.Pressure.toFixed(2));
            return true;
        })
    }, updateInterval);
}
