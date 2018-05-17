$(document).ready(function() {
	var loc = "https://maps.googleapis.com/maps/api/place/autocomplete/json?input={0}&key=AIzaSyCyFRpNW97igHUptANBC5kvJgr-9RcfZXw";
	var latlong = "https://maps.googleapis.com/maps/api/geocode/json?place_id={0}&key=AIzaSyAbNOCrzImiI8XExitXoVqhkzrr2Cc3JPI";
	var citycount = 4;
	var cities = {};

	hinit([2,3]);


	$('.typeahead').change(predict);


	$('#add-btn').click(function() {
		var $city =$(`
			<p class="city-recommend" id="city{0}-cr">City {0}</p>
			<div class="form-group">
				<input 
				class="form-control"
				type="text" 
				class="city-input" 
				id="city{0}"
				name="city{0}"
				placeholder="Enter city {0}">
			</div>
			`.format(++citycount));

		$('#city-inputs').append($city);
		$('#city{0}'.format(citycount)).change(predict);
	});


	$('#next-btn').click(function() {
		var place_id_tmp = [];
		var place_name_tmp = [];

		for (var i = 1; i <= citycount; i++) {
			var elem = $('#city{0}-cr'.format(i));
			if (elem.data("placeid") != undefined) {
				if (place_id_tmp.indexOf(elem.data("placeid")) < 0) {
					place_id_tmp.push(elem.data("placeid"));
					place_name_tmp.push(elem.html());
				} else {
					alert("No Repeated City allowed!")
					return;
				}
			}
		}
		console.log("placeidtmp");
		console.log(place_id_tmp);
		console.log("placenametmp");
		console.log(place_name_tmp);

		cities = {};
		cities['cities'] = {};

		// get long and lat from placeid
		place_id_tmp.forEach(function(item, i) {
			$.get(latlong.format(place_id_tmp[i]), function (data) {
				var lat = data['results'][0]['geometry']['location']['lat'];
				var lng = data['results'][0]['geometry']['location']['lng'];
				var placename = place_name_tmp[i];
				cities['cities'][placename] = [lat, lng];
				setTimeout(function() {
					if (i == place_id_tmp.length -1) {
						sw(1,2);
						begEnd();
					}
				}, 500);
			});
		});

	});

	$('#calc-btn').click(function() {
		var begin = $('#begin-city').find(":selected").text();
		var end = $('#end-city').find(":selected").text();

		console.log(begin + ":::" + end);
		if(begin && end) {
			sw(2,3);
			calc(begin, end);
		} else {
			alert("You must pick beginning and ending city!");
		}
	})

	function calc(begin, end) {
		console.log('HAHAHA')
		console.log(begin, end);
		if (begin !== "NOCITY") {
			cities['origin'] = begin;
		}if (end !== "NOCITY"){
			cities['destination'] = end;
		}
		console.log(cities);
		console.log("Calculating:" + cities);

		fetch('https://map-algo.herokuapp.com/get_path/', {
		    body: JSON.stringify(cities), // must match 'Content-Type' header
		    headers: {
		      'content-type': 'application/json'
		    },
		    method: 'POST', // *GET, POST, PUT, DELETE, etc.
		    // mode: 'cors', // no-cors, cors, *same-origin
		  }).then(res => res.json())
		.then(res => {
			console.log(res);
			var $list = $("<ul class='list-group'>");
			for (var i = 0; i < res.path.length; i ++) {
				$list.append($("<li class='list-group-item'></li>").html( (i+1) + ". " + res.path[i]));
			}
			$('#res-cost').html(
				"You can travel from <b>" + res.path[0]
				+ "</b> to <b>"
				+ res.path[res.path.length - 1] 
				+ "</b> in only <b>"
				+ res.cost / 1000 
				+ " km</b>, by travelling in this order!"
			);
			$('#res').html($list);


			// PLOT MAP

			xhr = new XMLHttpRequest();
			var url = "https://map-algo.herokuapp.com/plot_path/";
			xhr.open("POST", url, true);
			xhr.setRequestHeader("Content-type", "application/json", "charset", "utf-8");
			xhr.onreadystatechange = function () { 
			    if (xhr.readyState == 4 && xhr.status == 200) {
			    	// $('#plot').html(xhr.responseText);
			    	// console.log(xhr.responseText);
			    	var win = window.open("https://www.google.com.my", '_blank');
			    	win.focus();
			        win.document.open();
			        win.document.write(xhr.responseText);
			        win.document.close();
			    }
			}

			var pts = [];
			for (var i=0; i < res.path.length; i ++) {
				pts.push(cities['cities'][res.path[i]]);
			}
			console.log(pts)


			var data = {
				points:pts
			}
			data = JSON.stringify(data);
			xhr.send(data);


		})

	}

	function hinit(arr) {
		for (var i = 0; i < arr.length; i++){
			$('#scn' + arr[i]).hide();
		}
	}


	function sw(frm, to) {
		$('#scn' + frm).hide();
		$('#scn' + to).show();
	}


	function begEnd() {
		// var pick_tmp = `
		// 	<div class="form-check">
		// 	  <input class="form-check-input" type="radio" name="{0}" id="{0}{1}" value="{2}">
		// 	  <label class="form-check-label" for="{0}{1}">
		// 	    {2}
		// 	  </label>
		// 	</div>
		// `;
		var pick_tmp = `
			<div class="form-group">
				<select class="form-control" name="{0}" id="{0}">
					{1}
				</select>
			</div>
		`;

		var opt_tmp = `
			<option>{0}</option>
		`;
		var all = '<div>';
		var citynames = Object.keys(cities['cities']);

		all += '<h4>Beginning city:</h4>';
		var inside = "";
		inside += opt_tmp.format("NOCITY");
		for (var i = 0; i < citynames.length; i++) {
			inside += opt_tmp.format(citynames[i]);
		}
		all += pick_tmp.format('begin-city', inside);


		all += '<h4>Ending city:</h4>';
		var inside = "";
		inside += opt_tmp.format("NOCITY");
		for (var i = 0; i < citynames.length; i++) {
			inside += opt_tmp.format(citynames[i]);
		}
		all += pick_tmp.format('end-city', inside);

		all += '</div>';
		$("#scn2body").append($(all));
	}


	function predict(){
		console.log('change!')
		$that = $(this);
		console.log($that)
		$.get(loc.format($that.val()), function(data) {
			console.log('data!')
			var placedesc = data['predictions'][0]['description'];
			var placeid = data['predictions'][0]['place_id'];
			var index = $that.attr('id').substring(4);
			$('#city{0}-cr'.format(index)).html(placedesc);
			$('#city{0}-cr'.format(index)).data("placeid", placeid);
		});
	}

});
String.prototype.format = function () {
    var a = this;
    for (var k in arguments) {
        a = a.replace(new RegExp("\\{" + k + "\\}", 'g'), arguments[k]);
    }
    return a
}