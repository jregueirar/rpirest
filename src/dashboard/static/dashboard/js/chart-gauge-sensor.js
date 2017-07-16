// GAUGE CHARTS: TEMPERATURE, HUMIDITY AND PRESION
// div chart_gauge_env
google.charts.load('current', {'packages':['gauge']});

//google.charts.setOnLoadCallback(drawChart);
google.charts.setOnLoadCallback(drawChartTemperature);
// google.charts.setOnLoadCallback(drawChartHumidity);
// google.charts.setOnLoadCallback(drawChartPressure);

var refreshInterval = 2000;

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



    // $.rpijs.init(" ");
    // $.rpijs.formatDefaults.valueType = "binary";
    // $.rpijs.formatDefaults.update = 2000;
    // $.rpijs.get("/api/v1/env_sensors/temperature/", function(result) {
    //      data.setValue(0, 1, result.Temperature.toFixed(2));
    //      chartTemperature.draw(data, options);
    //      console.log("Temperature " + result.Temperature.toFixed(2));
    //      return true;
    //  });
    // });

    var chart = new google.visualization.Gauge(document.getElementById('chart_gauge_temp'));

    setInterval(function() {
        $.getJSON("api/v1/env_sensors/temperature/", function(result) {
            data.setValue(0,1,result.Temperature.toFixed(2));
            chart.draw(data, options);
            console.log("Temperature " + result.Temperature.toFixed(2));
            return true;
        })
    }, interval);

    setInterval(function() {
        $.getJSON("api/v1/env_sensors/humidity/", function(result) {
            data.setValue(1,1,result.Humidity.toFixed(2));
            chart.draw(data, optionsH);
            console.log("Humidity " + result.Humidity.toFixed(2));
            return true;
        })
    }, interval);

    var chartPressure = new google.visualization.Gauge(document.getElementById('chart_gauge_pressure'));
    setInterval(function() {
        $.getJSON("api/v1/env_sensors/pressure/", function(result) {
            data.setValue(2,1,result.Pressure.toFixed(2));
            chartPressure.draw(data, optionsP);
            console.log("Presión " + result.Pressure.toFixed(2));
        })
    }, interval);

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

    setInterval(function() {
        $.getJSON("http://rpi2/api/v1/env_sensors/humidity/", function(result) {
            data.setValue(0,1,result.Humidity.toFixed(2));
            chartHumidity.draw(data, options);
            console.log("Humidity " + result.Humidity.toFixed(2));
            return true;
        })
    }, interval);


}

function drawChartPressure() {

    var data = google.visualization.arrayToDataTable([
         ['Label', 'Value'],
         ['Presión', 20],
        ]);

    var options = {
        greenFrom: 10, greenTo: 40,
        redFrom: 40, redTo: 50,
        yellowFrom: 30, yellowTo: 40,
        majorTicks: [10,20,30,40,50],
        minorTicks: 5,
        max: 50
    };



}

function drawChart() {
    var data = google.visualization.arrayToDataTable([
        ['Label', 'Value'],
        ['Memory', 80],
        ['CPU', 55],
        ['Network', 68]
    ]);

    var options = {
        redFrom: 90, redTo: 100,
        yellowFrom:75, yellowTo: 90,
        minorTicks: 5
    };

    var chart = new google.visualization.Gauge(document.getElementById('chart_gauge_env'));

    chart.draw(data, options);

    setInterval(function() {
        data.setValue(0, 1, 40 + Math.round(60 * Math.random()));
        chart.draw(data, options);
    }, 13000);
    setInterval(function() {
        data.setValue(1, 1, 40 + Math.round(60 * Math.random()));
        chart.draw(data, options);
    }, 5000);
    setInterval(function() {
        data.setValue(2, 1, 60 + Math.round(20 * Math.random()));
        chart.draw(data, options);
    }, 26000);
}


