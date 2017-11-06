 /* Library to Control Sense Hat from Browser.
 *  =====================
 *  Copyright 2017 Jonás Regueira Rodríguez <jregueirar@gmail.com>
 *
 */
window.onload=function() {
    var type_device = $("#type_device").attr("data-value");
    var apirest_url = $("#api_rest_url").attr("data-value");
    var led_apagado = "#fdf9e6";


    $.rpijs.init(apirest_url + type_device +  "/");
    var svgDoc = $('#svgObject')[0].contentDocument;    // Get the document object for the SVG

    // $(document).ajaxSuccess(function() {
    //     $.sensehat.syncSVG(svgDoc);
    //     console.log("Ajax Success Ejecutado")
    // });

    $('#ledmatrix_clear').click(function (event) {
        var data = {
            "r": 0,
            "g": 0,
            "b": 0
        }
        var service_name = "led_matrix/clear/";
        $.rpijs.put(service_name, data, function () {
            // $.sensehat.svgChangeAllLeds(svgDoc, led_apagado);
            $.sensehat.syncSVG(svgDoc);
            console.log("Clear Done");
        });
    });

    $('#ledmatrix_on_all').click(function (event) {
        var hex_color = $('#led_color').val();
        var data = $.sensehat.hexToRgb(hex_color);
        var service_name = "led_matrix/clear/"
        $.rpijs.put(service_name, data, function () {
            $.sensehat.svgChangeAllLeds(svgDoc, hex_color);
            console.log("Clear Done");
        });
    });

    $('#ledmatrix_on_led').click(function() {
        var x = $('#led_coord_x').val();
        var y = $('#led_coord_y').val();
        var hex_color = $("#led_color").val();
		var data = $.sensehat.hexToRgb(hex_color);
		var service_name = 'led_matrix/pixels/' + x + ',' + y + "/"
		$.rpijs.put(service_name, data, function() {
		    $.sensehat.svgChangeLed(svgDoc, x, y, hex_color)
			console.log("Set Pixel Callback Done");
		});
   });


    $('#ledmatrix_off_led').click(function (event) {
        var x = $("#led_coord_x").val();
        var y = $("#led_coord_y").val();
        var data={
    		"r": 0,
    		"g": 0,
    		"b": 0
		};
        var service_name = "led_matrix/pixels/" + x + ',' + y + "/"
        $.rpijs.put(service_name, data, function () {
            $.sensehat.svgChangeLed(svgDoc,x,y,led_apagado);
            console.log("Clear Done");
        });
    });

    $('.led', svgDoc).click(function(event){
        var hex_color = $('#led_color').val();
        $(this, svgDoc).css('fill', hex_color);
        var x =$(this, svgDoc).attr('x');
        var y =$(this, svgDoc).attr('y');

        var data = $.sensehat.hexToRgb($('#led_color').val());
        var service_name = "led_matrix/pixels/" + x + ',' + y + "/"
        $.rpijs.put(service_name, data, function() {
            console.log("Set Pixel Callback Done");
        });
    });
};
