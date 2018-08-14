function myMap() {

    // Function to display the google map on startup
    var mapProp = {
        center: new google.maps.LatLng(53.347515, -6.265377),
        zoom: 10,
    };
    map = new google.maps.Map(document.getElementById("map"), mapProp);

    infoWindow = new google.maps.InfoWindow;

    //this code is reponsible for finding and displaing the users current location. 

    if (navigator.geolocation) {

        navigator.geolocation.getCurrentPosition(function (position) {
            pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };

            current = new google.maps.Marker({
                position: new google.maps.LatLng(pos),
                map: map,
                animation: google.maps.Animation.BOUNCE,
                title: 'Me'
            });

            google.maps.event.addListener(current, 'mouseover', (function (current) {
                return function () {
                    infoWindow.open(map, this);
                    infoWindow.setContent('Current location');
                }
            })(current));

        }, function () {
            handleLocationError(true, infoWindow, map.getCenter());

        });

    } else {

        handleLocationError(false, infoWindow, map.getCenter());
    }

}

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    infoWindow.setPosition(pos);

    infoWindow.setContent(browserHasGeolocation ?
        'Geolocation is Disabled' :
        'Error: Your browser doesn\'t support geolocation.');
    infoWindow.open(map);
}

// Function used for displaying/hiding the traffic information using a check variable 
var trafficCheck = 0;

function toggleTraffic(btn) {
    // Function activated by show/hide button for traffic
    // The variable 'trafficCheck' acts as a semaphore
    //The appearrance of the button also changes depending on the value
    if (trafficCheck === 0) {
        var mapProp = {
            center: new google.maps.LatLng(53.347515, -6.265377),
            zoom: 12,
        };

        map = new google.maps.Map(document.getElementById("map"), mapProp);
        trafficLayer = new google.maps.TrafficLayer();
        trafficLayer.setMap(map);
        document.getElementById("trafficButton").innerHTML = "Hide Traffic";
        trafficCheck++;

    } else {

        trafficLayer.setMap(null);
        document.getElementById("trafficButton").innerHTML = "Traffic";
        trafficCheck--;
    }
}

var swap = 0;

function swapDirection() {
    // Function to swap source address to destination and vica versa
    // Currently only set to swap names
    if (swap === 0) {
        document.getElementsByName('searchSource')[0].placeholder = 'Destination..';
        document.getElementsByName('searchDest')[0].placeholder = 'Source..';
        swap++;
    } else {
        document.getElementsByName('searchDest')[0].placeholder = 'Destination..';
        document.getElementsByName('searchSource')[0].placeholder = 'Source..';
        swap--;
    }
}


// ---------------- Jquery ----------------

//Functions to enable or disable the time and date select for return trips
$(document).ready(function () {
    $("input:radio[id=return]").click(ena)
});

$(document).ready(function () {
    $("input:radio[id=single]").click(disa)
});

var ena = function () {
    $("#id_returnDate").prop("disabled", false);
    $("#id_returnTime").prop("disabled", false);
    $("#id_returnDate").css("background-color", "white");
    $("#id_returnTime").css("background-color", "white");
    $("#id_returnDate").css("opacity", "1");
    $("#id_returnTime").css("opacity", "1");

}
var disa = function () {
    $("#id_returnDate").prop("disabled", true);
    $("#id_returnTime").prop("disabled", true);
    $("#id_returnDate").css("background-color", "lightgrey");
    $("#id_returnTime").css("background-color", "lightgrey");
    $("#id_returnDate").css("opacity", "0.4");
    $("#id_returnTime").css("opacity", "0.4");
}


$(document).ready(function () {
    $("#planner-toggle").click(function () {

        $("#planner").slideToggle("slow");

        if ($("#planner-toggle").text() == "Expand Route Planner") {
            $("#planner-toggle").html("Hide Route Planner")

        } else if ($("#planner-toggle").text() == "Hide Route Planner") {


            $("#planner-toggle").text("Expand Route Planner")
        }
    });
});


//Function to swap the autocomplete in the form between the stop numbers and the stop addresses.
function swapSearch() {

    //Checks which option is selected between searching by stops or addresses
    var c = document.getElementById("stopSearch").style.backgroundColor;

    if (c != "black") {
        //Changes the colour of the tab and placeholder of the search form
        document.getElementById("stopSearch").style.backgroundColor = "black";

        document.getElementById("addSearch").style.backgroundColor = "#00743F";
        document.getElementById('id_source').placeholder = 'Source Address..';

        //This code turns off the autocomplete function to make sure they results from the stop autocomplete do not appear under the general address search. 

        $( "#id_source" ).autocomplete({
            disabled: true})

            $( "#id_destination" ).autocomplete({
                disabled: true})
        //Changes the autocomplete in the source to address based on name
        //     $('input[name=source]').autocomplete({

        //Autocomplete for general Address Input from Google in the Destination Input


        sourceAutocomplete = new google.maps.places.Autocomplete(document.getElementById(
            'id_source'))

        destinationAutocomplete = new google.maps.places.Autocomplete(document.getElementById(
            'id_destination'))

        sourceAutocomplete.setComponentRestrictions({
            'country': 'ie'
        });


        destinationAutocomplete.setComponentRestrictions({
            'country': 'ie'
        });

        //implementing the autocompletes for the different input fields - source and destination. 
        google.maps.event.addListener(sourceAutocomplete, 'place_changed', function () {
            source = sourceAutocomplete.getPlace();

            google.maps.event.addListener(destinationAutocomplete, 'place_changed', function () {
                destination = destinationAutocomplete.getPlace();

            })
        })


    } else {
        //Changes the colour of the tab and placeholder of the search form
        document.getElementById("addSearch").style.backgroundColor = "black";

        document.getElementById("stopSearch").style.backgroundColor = "#00743F";
        document.getElementById('id_source').placeholder = 'Source Stop..';


        $( "#id_source" ).autocomplete({
            disabled: false})

            $( "#id_destination" ).autocomplete({
                disabled: false})

        //This is needed to remove the google maps api before changing it to search by roots. 
        if (sourceAutocomplete !== undefined && destinationAutocomplete != undefined) {
            google.maps.event.clearInstanceListeners(sourceAutocomplete);
            google.maps.event.clearInstanceListeners(destinationAutocomplete);
            $(".pac-container").remove();


            //Autocomplete for Stop Addresses in the Destination Input

            $.ajax({
                type: "GET",
                url: "RouteInfo",
                dataType: "json",

                success: function (data) {
                    createArray(data);
                }
            });



            function createArray(Data) {

                results = [];
                for (var i = 0; i < Data.length; i++) {
                    results.push(Data[i].num);
                }
                $("#id_destination, #id_source").autocomplete({
                    source: results,
                    minLength: 2,
                });

            }
        }
    }

};


//This piece of code allows the getStops function to be called when the user hits the enter key. s
var markers = [];

function getStops() {

    //this function is responsible for displaying the route information
    //It uses jQuery to intitialise and pass the value to the url and to grab the data that is returned by get_route_info
    if (markers)

        //this checks to see if there are markers on the map, if there are markers it removes them before the function happens to add the new ones. 
        for (var i = 0; i < markers.length; i++) {

            markers[i].setMap(null);

        }


    var jqxhr = $.getJSON('/details/' + document.getElementById("routeSearch").value +
        '/',
        function (daily) {


            var table = "";
            table =
                "<table class = 'table table-hover table-condensed table-sm table-bordered table-striped overflow-y: hidden'>";
            table += "<tr><thead>";
            table += "<th>Stop</th>";
            table += "</tr></thead><tbody>";

            for (var i = 0; i < daily.length; i++) {


                var lat = daily[i].lat;
                var long = daily[i].lng;
                var name = daily[i].name;

                var id = daily[i].id;

                table += "<tr>";
                table += "<td>" + daily[i].name + "(" + id + ")" + "</td>";
                table += "</tr>";


                infoWindow = new google.maps.InfoWindow;
                infoBus = new google.maps.InfoWindow;

                //this function displays the dublin bus markers
                myLatLng = new google.maps.LatLng(lat, long)
                marker = new google.maps.Marker({
                    position: myLatLng,
                    map: map,
                    title: name
                });

                marker.addListener('mouseover', function () {
                    infoBus.open(map, this);
                    infoBus.setContent(this.title);
                })

                marker.addListener('click', function () {
                    document.getElementById("id_source").value = this.title;

                })

                markers.push(marker);

                // <!-- 
                //                             var path = poly.getPath();
                //                             path.push(myLatLng); -->
            }

            table += "</tbody></table>";
            document.getElementById("RouteDiv").innerHTML = table;
        })
};


function realTimeInfo() {

    //this function gets real time information for the stop that is selected.

    var jqxhr = $.getJSON(
        'https://data.smartdublin.ie/cgi-bin/rtpi/realtimebusinformation?stopid=' +
        document.getElementById("id_source").value + '&format=json',
        function (daily) {
            var now = new Date();
            var temp = new Date();

            var table = "";
            table = "<table class = 'table table-hover table-condensed table-sm table-bordered table-striped overflow-y: hidden'>";
            table += "<tr><thead>";
            table += "<th>Route</th>";
            table += "<th>Destination</th>";
            table += "<th>Arrival Time</th>";
            table += "<th>Expected</th>";
            table += "</tr></thead><tbody>";
            x = daily.results;
            for (var i = 0; i < x.length; i++) {

                var ti = x[i].arrivaldatetime.slice(11, );

                var array = ti.split(":");
                temp.setHours(array[0]);
                temp.setMinutes(array[1]);
                temp.setSeconds(array[2]);
                var difference = new Date();
                difference.setTime(temp - now);
                var m = difference.getMinutes();

                if (difference.getSeconds() >= 30) {
                    m = m + 1;
                };
                if (m == 0) {
                    m = "Due"
                } else {
                    m = String(m) + " mins"
                };

                table += "<tr>";
                table += "<td>" + x[i].route + "</td>";
                table += "<td>" + x[i].destination + "</td>";
                table += "<td>" + ti.slice(0, 5) + "</td>";
                table += "<td>" + m + "</td>";
                table += "</tr>";
            }
            table += "</tbody></table>";
            document.getElementById("realtimeTable").innerHTML = table;

        })
};


//Functions to display/hide the stop search and route search
function findStop() {
    if (document.getElementById("stopSearchOptions").style.display == "none") {
        document.getElementById("stopSearchOptions").style.display = "block";
        document.getElementById("routeSearchOptions").style.display = "none";
    } else {
        document.getElementById("stopSearchOptions").style.display = "none";
    }
}

function findRoute() {
    if (document.getElementById("routeSearchOptions").style.display == "none") {
        document.getElementById("routeSearchOptions").style.display = "block";
        document.getElementById("stopSearchOptions").style.display = "none";
    } else {
        document.getElementById("routeSearchOptions").style.display = "none";
    }
}



//autocomplete for stop search on page load

$("#id_souce, #id_destination").ready(function (){
$.ajax({
    type: "GET",
    url: "RouteInfo",
    dataType: "json",

    success: function (data) {
        createArray(data);
    }
});

})


function createArray(Data) {

    results = [];
    for (var i = 0; i < Data.length; i++) {
        results.push(Data[i].num);
    }
    $("#id_destination, #id_source").autocomplete({
        source: results,
        minLength: 2,
    });

}


//Shows the loading gif when the submit button is initally pressed
function showLoadGif(){
    var x = document.forms["routes"]["source"].value;
    var y = document.forms["routes"]["destination"].value;
    var z = document.forms["routes"]["departTime"].value;
    
    if (x != "" && y != "" && z != "") {
        document.getElementById("load_screen").style.display = "block"
    }
}

var busMarkers = 0;

var markBus = []

function displayBusMarkers() {

    var jqxhr = $.getJSON('/dublinBusInfo',
        function (daily) {
            var infoWindow = new google.maps.InfoWindow;
            var infoBikes = new google.maps.InfoWindow;


            if (busMarkers == 0) {

                var imageMarker = markerImages;

                //this function displays the dublin bikes markers

                for (var i = 0; i < daily.length; i++) {


                    var lat = daily[i].lat;
                    var long = daily[i].lng;

                    latlng = new google.maps.LatLng(lat, long);
                    var marker = new google.maps.Marker({
                        position: latlng,
                        title: daily[i].name + "(" + daily[i].num + ")"
                    });

                    markBus.push(marker);

                    marker.addListener('mouseover', function () {

                        infoBikes.open(map, this);
                        infoBikes.setContent(this.title);
                    })



                    google.maps.event.addListener(marker, 'click', (function (marker, i) {
                        return function () {
                         
                        markerName = daily[i].name
                        markerNum = daily[i].num
                        $(".modal-body #markerName").text(markerName + " " + markerNum);
                        $modal = $('#MarkersModal');
                        $modal.modal('show');
                        
                        }
                    })(marker, i));

                }

                markerCluster = new MarkerClusterer(map, markBus, {
                    imagePath: imageMarker
                });

                document.getElementById("markersbutton").innerHTML = "Hide Stops";
                busMarkers++;
                

            } else {

                //this checks to see if there are markers on the map, if there are markers it removes them before the function happens to add the new ones. 
                markerCluster.clearMarkers();
                markBus = []
                document.getElementById("markersbutton").innerHTML = "Stops";
                busMarkers--;

            }


        });

};
                                               
var bikeMarkers = 0;
var markBikes = []

function displayBikeMarkers() {

    var jqxhr = $.getJSON('/dublinBikeInfo',
        function (daily) {
            var infoWindow = new google.maps.InfoWindow;
            var infoBikes = new google.maps.InfoWindow;

            if (bikeMarkers == 0) {

                var imageMarker = markerImages;

                //this function displays the dublin bikes markers

                for (var i = 0; i < daily.length; i++) {


                    var lat = daily[i].lat;
                    var long = daily[i].lng;



                    var busicon = {
                        url: "{% static 'images/dublinBikes.png' %}", // url
                        scaledSize: new google.maps.Size(40, 40), // scaled size            
                    };


                    latlng = new google.maps.LatLng(lat, long);
                    var marker = new google.maps.Marker({
                        position: latlng,
                        icon: busicon,
                        title: daily[i].name
                    });


                    marker.addListener('mouseover', function () {

                        infoBikes.open(map, this);
                        infoBikes.setContent(this.title);
                    })

                    markBikes.push(marker);
                }

                markerCluster1 = new MarkerClusterer(map, markBikes, {
                    imagePath: imageMarker
                });

                document.getElementById("bikesbutton").innerHTML = "Hide Bikes";
                bikeMarkers++;

            } else {

                //this checks to see if there are markers on the map, if there are markers it removes them before the function happens to add the new ones. 
                markerCluster1.clearMarkers();
                markBikes = []

                document.getElementById("bikesbutton").innerHTML = "Bikes";
                bikeMarkers--;

            }


        });

};

markers = [];

function getStops() {


    //this function is responsible for displaying the route information
    //It uses jQuery to intitialise and pass the value to the url and to grab the data that is returned by get_route_info

    if (markers)
        //this checks to see if there are markers on the map, if there are markers it removes them before the function happens to add the new ones. 
        for (var i = 0; i < markers.length; i++) {

            markers[i].setMap(null);

        }

    var jqxhr = $.getJSON('/details/' + document.getElementById("routeSearch").value +
        '/',
        function (daily) {

            if (daily == "fail") {
                $modal = $('#routeModal');
                $modal.modal('show');
                $("#routeSearch").css('background-color', 'red');
            } else {
                var table = "";
                table =
                    "<table class = 'table table-hover table-condensed table-sm table-bordered table-striped overflow-y: hidden'>";
                table += "<tr><thead>";
                table += "<th>Stop</th>";
                table += "</tr></thead><tbody>";

                for (var i = 0; i < daily.length; i++) {

                    table += "<tr>";
                    table += "<td>" + daily[i].name + "(" + daily[i].id +
                        ")" + "</td>";
                    table += "</tr>";


                    infoWindow = new google.maps.InfoWindow;
                    infoBus = new google.maps.InfoWindow;

                    //this function displays the dublin bus markers
                    myLatLng = new google.maps.LatLng(parseFloat(daily[i].lat),
                        parseFloat(daily[i].lng))
                    marker = new google.maps.Marker({
                        position: myLatLng,
                        map: map,
                        title: daily[i].name + " " + "(" + daily[i].id +
                            ")"
                    });

                    marker.addListener('mouseover', function () {
                        infoBus.open(map, this);
                        infoBus.setContent(this.title);
                    })

                    markers.push(marker);
                }



                table += "</tbody></table>";
                document.getElementById("RouteDiv").innerHTML = table;

            }
        })
};


function placeSearch() {

    //the below function used a combination of the above two efforts. 


    //This function is responsible for allowing the user to search for a general address
    //the map will then zoom in on that place
    //they can then chose to view the markers in that area.

    autocomplete = new google.maps.places.Autocomplete(document.getElementById(
        'genSearch'));

    autocomplete.setComponentRestrictions({
        'country': 'ie'
    });

    google.maps.event.addListener(autocomplete, 'place_changed', function () {
        var place = autocomplete.getPlace();


        if (!place.geometry) {
            // User entered the name of a Place that was not suggested and
            // pressed the Enter key, or the Place Details request failed.
            window.alert("No details available for input: '" + place.name + "'");
            return;
        }

        // If the place has a geometry, then present it on a map.
        if (place.geometry.viewport) {
            map.fitBounds(place.geometry.viewport);
        } else {
            map.setCenter(place.geometry.location);
            map.setZoom(17); // Why 17? Because it looks good.
        }
        marker.setPosition(place.geometry.location);
        marker.setVisible(true);
    });
};

 //Autocomplete for Route Search this is paired with an onfocus function to watch for a user click into the box. 
 function routeSearch() {
    $(document).ready(function () {
        $.ajax({
            type: "GET",
            url: "dublinBusRoutes",
            dataType: "json",

            success: function (data) {
                createArray(data);
            }
        });
    });


    function createArray(Data) {

        var results = [];

        for (var i = 0; i < Data.length; i++) {

            results.push(Data[i].route);



        }
        $("#routeSearch").autocomplete({
            source: results,
            minLength: 1,
        });
    }
}

//This function handles the users response on the markers onclick modal

function HandleResponse(name, num) {

    if (document.getElementById("first").checked) {

        var c = document.getElementById("stopSearch").style.backgroundColor;
        //checks the background color and adds the address if address is selected or adds number if number is selected. 
        if (c == "black") {
            document.getElementById("id_source").value = name;
        } else {
            document.getElementById("id_source").value = num;
        }
    } else if (document.getElementById("second").checked) {

        var c = document.getElementById("stopSearch").style.backgroundColor;

        if (c == "black") {
            document.getElementById("id_destination").value = name;
        } else {
            document.getElementById("id_destination").value = num;
        }
    }

    $('#MarkersModal').modal('hide');

}

function generateQuery() {
    //this function gets real time information for the stop that is selected.
    var jqxhr = $.getJSON(
        'https://data.smartdublin.ie/cgi-bin/rtpi/realtimebusinformation?stopid=' +
        "{{ source}}" + '&format=json',
        function (daily) {
            var now = new Date();
            var temp = new Date();

            var table = "";
            table =
                "<table class = 'table table-hover table-condensed table-sm table-bordered table-striped' style = 'overflow-x:scroll;'>";
            table += "<tr><thead>";
            table += "<th>Route</th>";
            table += "<th>Destination</th>";
            table += "<th>Arrival Time</th>";
            table += "<th>Expected</th>";
            table += "</tr></thead><tbody>";
            x = daily.results;
            for (var i = 0; i < x.length; i++) {

                var ti = x[i].arrivaldatetime.slice(11, );

                var array = ti.split(":");
                temp.setHours(array[0]);
                temp.setMinutes(array[1]);
                temp.setSeconds(array[2]);
                var difference = new Date();
                difference.setTime(temp - now);
                var m = difference.getMinutes();

                if (difference.getSeconds() >= 30) {
                    m = m + 1;
                };
                if (m == 0) {
                    m = "Due"
                } else {
                    m = String(m) + " mins"
                };

                table += "<tr>";
                table += "<td>" + x[i].route + "</td>";
                table += "<td>" + x[i].destination + "</td>";
                table += "<td>" + ti.slice(0, 5) + "</td>";
                table += "<td>" + m + "</td>";
                table += "</tr>";
            }
            table += "</tbody></table><br>";
            document.getElementById("realtimeTable").innerHTML = table;

        })
};



// References:
//https://github.com/jonthornton/jquery-timepicker 
//http://api.jqueryui.com/datepicker/
//the code for the new Autocmplete function was inspired by; https://stackoverflow.com/questions/24594662/jqueryui-autocomplete-data-from-text-csv-file-with-ajax

//the place search functions
//https://www.w3docs.com/learn-javascript/places-autocomplete.html
//https://developers.google.com/maps/documentation/javascript/examples/places-autocomplete-multiple-countries

//toggling the autocomplete on and off
 // https://stackoverflow.com/questions/9828856/how-to-toggle-the-google-maps-autocomplete-on-and-off


//Geolocation
 //https://developers.google.com/maps/documentation/javascript/examples/map-geolocation
 