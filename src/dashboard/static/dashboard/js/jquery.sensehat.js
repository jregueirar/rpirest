/**
 * Created by jonas on 1/07/16.
 *
 */

(function ($, undefined) {

	$.sensehat = {};
    $.sensehat.LED_OFF = "#fdf9e6";
	$.sensehat.NROWS = 8;

	$.sensehat.hexToRgb = function(hex) {
    		var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    		return result ? {
        		r: parseInt(result[1], 16),
        		g: parseInt(result[2], 16),
        		b: parseInt(result[3], 16)
    		} : null;
	}

	function componentToHex(c) {
    		var hex = c.toString(16);
    		return hex.length == 1 ? "0" + hex : hex;
	}

	$.sensehat.rgbToHex = function(r, g, b) {
    		return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
	}

	$.sensehat.svgChangeLed = function(svgDoc, x, y, hex_color) {
        nled = parseInt(x) + (parseInt(y) * $.sensehat.NROWS);
        console.log("Off Led: " + nled);
        $("#led" + nled, svgDoc).css("fill", hex_color);
        return true;
    }

   // Enciende de un color o apaga todos los leds de la Matriz
    $.sensehat.svgChangeAllLeds = function (svgDoc, hex_color) {
        console.log("On/off alls Leds");
        nleds = $.sensehat.NROWS * $.sensehat.NROWS;
        for (var i = 0; i < nleds; i++) {
            $("#led" + i, svgDoc).css("fill", hex_color);
        }
        return true;
    };

    // Lee el estado de la Matrix de Led y copia el estado
    // a la Matrix de Led SVG.
    // FIXME ¿ le pasamos la lista de Leds ? 0
    $.sensehat.syncSVG = function(svgDoc) {
        $.rpijs.get("led_matrix/pixels",function(result){
            var hex;
            var r=0, g=1, b=2;
            ledList = result.pixel_list;
            console.log("ledList.lenght: " + ledList.length);
            for (var i = 0; i < ledList.length; i++) {
                hex = $.sensehat.rgbToHex(ledList[i][r], ledList[i][g], ledList[i][b]);
                console.log("HEX: " + hex);
                if (hex == "#000000") {
                    hex = $.sensehat.LED_OFF
                }
                $("#led"+i, svgDoc).css('fill', hex);
            }
        });
    };

}(jQuery));
