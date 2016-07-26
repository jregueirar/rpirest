/**
 * Created by jonas on 1/07/16.
 * Original source code: jquery-rpijs.js (https://github.com/matematik7/rpi-dashboard)
 */

/* start fragment */
/* Source: https://gist.github.com/chicagoworks/754454 */
jQuery.extend({
    stringify  : function stringify(obj) {         
        if ("JSON" in window) {
            return JSON.stringify(obj);
        }

        var t = typeof (obj);
        if (t != "object" || obj === null) {
            // simple data type
            if (t == "string") obj = '"' + obj + '"';

            return String(obj);
        } else {
            // recurse array or object
            var n, v, json = [], arr = (obj && obj.constructor == Array);

            for (n in obj) {
                v = obj[n];
                t = typeof(v);
                if (obj.hasOwnProperty(n)) {
                    if (t == "string") {
                        v = '"' + v + '"';
                    } else if (t == "object" && v !== null){
                        v = jQuery.stringify(v);
                    }

                    json.push((arr ? "" : '"' + n + '":') + String(v));
                }
            }

            return (arr ? "[" : "{") + String(json) + (arr ? "]" : "}");
        }
    }
});
/* end fragment */

(function ($, undefined) {
	
	$.sensehat = {};

	/* initialize REST api details */
	$.sensehat.init = function(apiUrl, username, password) {
		$.sensehat.apiUrl = apiUrl;
		$.sensehat.username = username;
		$.sensehat.password = password;
	};

	$.sensehat.get = function(name, callback, options) {
		var settings = $.extend({}, $.sensehat.defaults, options);

	  	if (settings.rate) {
	   		getRate(name, callback, options);
	    		return;
	  	}

		$.ajax({
	  		url: $.sensehat.apiUrl + name,
	    	headers: {
			Authorization: authString()
	    	}
		}).done(function(object) {
	    		var ret = callback(parse(object, name, options));
	    
	    		if (ret && settings.update != 0) {
				setTimeout(function() {
		    		$.sensehat.get(name, callback, options);
				}, settings.update);
	    		}
		});
	};

	$.sensehat.put = function(name, data, callback) {
		return $.ajax({
			type: "PUT",
			url: $.sensehat.apiUrl + name,
			data: $.stringify(data),
			dataType: "json"
		}).done(callback); 
	};

}(jQuery));
