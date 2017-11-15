 /* Library to Control Sense Hat from Browser.
 *  =====================
 *  Copyright 2017 Jonás Regueira Rodríguez <jregueirar@gmail.com>
 *
 */
window.onload=function() {
    var type_device = $("#type_device").attr("data-value");
    var apirest_url = $("#api_rest_url").attr("data-value");
    var led_apagado = "#fdf9e6";

    $.rpijs.init(apirest_url + type_device + "/");
    var svgDoc = $('#svgObject')[0].contentDocument;    // Get the document object for the SVG
    $.sensehat.syncSVG(svgDoc);

    if ($('#ledmatrix_lowlight').prop('checked')) {
        data = {'low_light': 'true'}
    } else {
        data = {'low_light': 'false'}
    }
    $.rpijs.put("led_matrix/low_light/", data, function () {
        $.sensehat.syncSVG(svgDoc);
        console.log("[INFO] Toggle the led light mode... DONE");
    });


    // $(document).ajaxSuccess(function() {
    //     $.sensehat.syncSVG(svgDoc);
    //     console.log("Ajax Success Ejecutado")
    // });

    // $( document ).ajaxSuccess(function( event, xhr, settings ) {
    //     console.log("[DEBUG] Triggered ajaxSuccess handler. The Ajax response was: " + xhr.responseText );
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
        var hex_color = $('#led_colour').val();
        var data = $.sensehat.hexToRgb(hex_color);
        var service_name = "led_matrix/clear/"
        $.rpijs.put(service_name, data, function () {
            $.sensehat.syncSVG(svgDoc);
            console.log("On All Leds...done");
        });
    });

    $('#ledmatrix_on_led').click(function() {
        var x = $('#led_coord_x').val();
        var y = $('#led_coord_y').val();
        var hex_color = $("#led_colour").val();
		var data = $.sensehat.hexToRgb(hex_color);
		var service_name = 'led_matrix/pixels/' + x + ',' + y + "/"
		$.rpijs.put(service_name, data, function() {
		    $.sensehat.syncSVG(svgDoc);
			console.log("On Led... Done");
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
            $.sensehat.syncSVG(svgDoc);
            console.log("Off Led done");
        });
    });

    $('#ledmatrix_rotation').click(function(event) {
        var angle=$("#angle_rotation").val();
        var data={'angle': angle, redraw: false};

        $.rpijs.put("led_matrix/rotation/", data, function(){
            $.sensehat.syncSVG(svgDoc);
            console.log("Rotation " + angle + "º ...Done");
            data={'angle': angle, redraw:true};
            $.rpijs.put("led_matrix/rotation/", data, function(){
                console.log("Rotation Redraw " + angle + "º... Done");
            });
        });




    });

    $('#ledmatrix_fliph').click(function(event) {
        var data={};
        $.rpijs.put("led_matrix/flip_h/", data, function(){
            console.log("[INFO] Flip Horizontal Done");
            $.sensehat.syncSVG(svgDoc);
            console.log("[DEBUG] Flip Horizontal Done");
        });
    });

    $('#ledmatrix_flipv').click(function(event) {
        var data={};
        $.rpijs.put("led_matrix/flip_v/", data, function(){
            console.log("Flip Vertical Done");
            $.sensehat.syncSVG(svgDoc);
            console.log("[DEBUG] Flip Vertical Done");
        });
    });

    $('#ledmatrix_lowlight').click(function () {
        var data={};

        if( $('#ledmatrix_lowlight').prop('checked') ) {
            data = {'low_light': 'true'}
        }else {
            data = {'low_light': 'false'}
        }
        $.rpijs.put("led_matrix/low_light/", data, function() {
            $.sensehat.syncSVG(svgDoc);
            console.log("[INFO] Toggle the led light mode... DONE");
        });
    });

    $('#ledmatrix_letter').click(function () {
        var letter=$("#input_letter").val();
        var back_colour = $("#background_colour").val();
        var text_colour = $("#led_colour").val();

        if (back_colour == led_apagado) {
            back_colour = {"r": 0, "g": 0, "b": 0};
        }else{
            back_colour = $.sensehat.hexToRgb(back_colour);
        }
        var data={
            "text_colour": $.sensehat.hexToRgb(text_colour),
            "back_colour": back_colour,
            "letter": letter
        };
        $.rpijs.put("led_matrix/show_letter/", data, function() {
            $.sensehat.syncSVG(svgDoc);
            console.log("[INFO] Show the letter " + letter + "... DONE");
        });
    });

    $('#ledmatrix_message').click(function () {
        var data={};

        if( $('#ledmatrix_lowlight').prop('checked') ) {
            data = {'low_light': 'true'}
        }else {
            data = {'low_light': 'false'}
        }
        $.rpijs.put("led_matrix/low_light/", data, function() {
            $.sensehat.syncSVG(svgDoc);
            console.log("[INFO] Toggle the led light mode... DONE");
        });
    });

    $('.led', svgDoc).click(function(event){
        var hex_color = $('#led_colour').val();
        var x =$(this, svgDoc).attr('x');
        var y =$(this, svgDoc).attr('y');
        var data = $.sensehat.hexToRgb(hex_color);
        var service_name = "led_matrix/pixels/" + x + ',' + y + "/"

        $("#led_coord_x").val(x);
        $("#led_coord_y").val(y);
        $.rpijs.put(service_name, data, function() {
            $.sensehat.svgChangeLed(svgDoc, x, y , hex_color);
            console.log("Set Led Callback... Done");
        });
    });
};
