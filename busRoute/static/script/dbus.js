function myMap() {

    // Function to display the google map on startup
    var mapProp = {
        center: new google.maps.LatLng(53.347515, -6.265377),
        zoom: 10,
    };
    map = new google.maps.Map(document.getElementById("map"), mapProp);

    infoWindow = new google.maps.InfoWindow;

    //this code is reponsible for finding and displaing the users current location. 
    //This essenially casuses the user to be prompted for their current location
    if (navigator.geolocation) {
        //the getCurrentLocation function is repsonsible for accessing the users current location. 
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

    //Checks which option is selected between searching by stops or addresses by which background is black. 
    var c = document.getElementById("stopSearch").style.backgroundColor;

    if (c != "black") {
        //Changes the colour of the tab and placeholder of the search form to search by address. 
        document.getElementById("stopSearch").style.backgroundColor = "black";

        document.getElementById("addSearch").style.backgroundColor = "#00743F";
        document.getElementById('id_source').placeholder = 'Source Address..';

        //This code turns off the autocomplete function to make sure they results from the stop autocomplete do not appear under the general address search. 

        $("#id_source").autocomplete({
            disabled: true
        })

        $("#id_destination").autocomplete({
            disabled: true
        })

        //Autocomplete for general Address Input from Google in the Source and Destination Input

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
        //Changes the colour of the tab and placeholder of the search form to search by stops. 
        document.getElementById("addSearch").style.backgroundColor = "black";

        document.getElementById("stopSearch").style.backgroundColor = "#00743F";
        document.getElementById('id_source').placeholder = 'Source Stop..';

        //This enables the autocomplete function once when the user choses to search by address
        //This is important as the stops autocomplete needs to be disabled when the user chosen to search by address. 
        $("#id_source").autocomplete({
            disabled: false
        })

        $("#id_destination").autocomplete({
            disabled: false
        })

        //This is needed to disable the google maps api before changing it to search by roots. 
        if (sourceAutocomplete !== undefined && destinationAutocomplete != undefined) {
            google.maps.event.clearInstanceListeners(sourceAutocomplete);
            google.maps.event.clearInstanceListeners(destinationAutocomplete);
            $(".pac-container").remove();


            //Autocomplete for Stop numbers 
            //This ajax function accesses the data passed to the url provided by the backend. 
            $.ajax({
                type: "GET",
                url: "dublinBusInfo",
                dataType: "json",

                success: function (data) {
                    createArray(data);
                }
            });

            //this creates the array of information from the url. 
            function createArray(Data) {

                results = [];
                for (var i = 0; i < Data.length; i++) {
                    results.push(Data[i].num);
                }

                //This initiates the autocomplete and returns that information that matches the user input.  
                $("#id_destination, #id_source").autocomplete({
                    source: results,
                    minLength: 2,
                });

            }
        }
    }

};

var markers = [];

function getStops() {

    //this function is responsible for displaying the route information
    //It uses jQuery to intitialise and pass the value to the url and to grab the data that is returned by get_route_info views function. 
    if (markers)

        //This checks to see if there are markers on the map, if there are markers it removes them before the function happens to add the new ones. 

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

            }

            table += "</tbody></table>";
            document.getElementById("RouteDiv").innerHTML = table;
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

//Autocomplete for stop search on page load

$("#id_souce, #id_destination").ready(function () {
    $.ajax({
        type: "GET",
        url: "dublinBusInfo",
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
function showLoadGif() {
    var x = document.forms["routes"]["source"].value;
    var y = document.forms["routes"]["destination"].value;
    var z = document.forms["routes"]["departTime"].value;

    if (x != "" && y != "" && z != "") {
        document.getElementById("load_screen").style.display = "block"
    }
}
//This is used as a semaphore to help the onclick button functionality to add/remove markers. 
var busMarkers = 0;
//The google markers are added to this array. 
var markBus = []

//This function displays the dublin Bus Markers
function displayBusMarkers() {

    var jqxhr = $.getJSON('/dublinBusInfo',
        function (daily) {
            var infoWindow = new google.maps.InfoWindow;
            var infoBikes = new google.maps.InfoWindow;

            //checks the value of the bus Markers. Initially the value will be zero. 
            if (busMarkers == 0) {

                //this variable is the markers clustering images. 
                var imageMarker = markerImages;

                //this function displays the dublin bus markers by iterating over the data returned in the jQuery. 

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

                //this function clusters the markers. 

                markerCluster = new MarkerClusterer(map, markBus, {
                    imagePath: imageMarker
                });

                //onclick the markers will now be displayed so the button name is changed. 

                document.getElementById("markersbutton").innerHTML = "Hide Stops";
                //The bus markers variable is incremented so on the next click, the if statement above is no longer satisfied. 

                busMarkers++;


            } else {

                // The else statement occurs when the button is clicked to "Hide Stops" after the above functionality has been implemented. 

                //This checks to see if there are markers on the map, if there are markers it removes them before the function happens to add the new ones. 
                markerCluster.clearMarkers();
                //the array is set to null. 
                markBus = []
                //the button name is changed back. 
                document.getElementById("markersbutton").innerHTML = "Stops";
                //The variable is decremented so the if statement will be satisfied during another click to then show the stops. 
                busMarkers--;

            }


        });

};

//This is used as a semaphore to help the onclick button functionality to add/remove markers. 

var bikeMarkers = 0;

//The google markers are added to this array. 

var markBikes = []

//This function displays the dublin Bike Markers

function displayBikeMarkers() {

    var jqxhr = $.getJSON('/dublinBikeInfo',
        function (daily) {
            var infoWindow = new google.maps.InfoWindow;
            var infoBikes = new google.maps.InfoWindow;

            //checks the value of the bike Markers. Initially the value will be zero. 

            if (bikeMarkers == 0) {

                //this variable is the markers clustering images. 

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

                //this function clusters the markers. 

                markerCluster1 = new MarkerClusterer(map, markBikes, {
                    imagePath: imageMarker
                });

                //onclick the markers will now be displayed so the button name is changed to a hide them option. 

                document.getElementById("bikesbutton").innerHTML = "Hide Bikes";

                //The bus markers variable is incremented so on the next click, the if statement above is no longer satisfied. 
                bikeMarkers++;

            } else {

                // The else statement occurs when the button is clicked to "Hide Stops" after the above functionality has been implemented. 


                //this checks to see if there are markers on the map, if there are markers it removes them before the function happens to add the new ones. 
                markerCluster1.clearMarkers();

                //the array is set to null. 
                markBikes = []

                //the button name is changed back to provide an option to show the bikes. 

                document.getElementById("bikesbutton").innerHTML = "Bikes";
                //The variable is decremented so the if statement will be satisfied during another click to then show the stops. 
                bikeMarkers--;

            }


        });
};

markers = [];


function placeSearch() {

    //the below function used a combination of the above two efforts. 

    //This function is responsible for allowing the user to search for a general address in the stop info search option. 
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
//Gets the data. 
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

    //turms the data into an array to be passed into the autocomplete. 
    function createArray(Data) {

        var results = [];

        for (var i = 0; i < Data.length; i++) {

            results.push(Data[i].route);



        }

        //the array of data is passed in to the autocomplete to provide matches to user input. 
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