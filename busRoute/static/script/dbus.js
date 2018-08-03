function myMap() {
    // Function to display the google map on startup
    var mapProp= {
        center:new google.maps.LatLng(53.347515, -6.265377),
        zoom:10,
    };
        map=new google.maps.Map(document.getElementById("map"),mapProp);

        infoWindow = new google.maps.InfoWindow;

        //this code is reponsible for finding and displaing the users current location. 
        //This came from https://developers.google.com/maps/documentation/javascript/examples/map-geolocation
        // Try HTML5 geolocation.
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(function(position) {
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

                google.maps.event.addListener(current, 'mouseover', (function(current) {
                    return function() {
                        infoWindow.open(map, this);
                        infoWindow.setContent('Current location');
                    }
                })(current));

          }, function() {
            handleLocationError(true, infoWindow, map.getCenter());

          });

        } else {
        
          handleLocationError(false, infoWindow, map.getCenter());
        }
  
      }

      function handleLocationError(browserHasGeolocation, infoWindow, pos) {
        infoWindow.setPosition(pos);
        infoWindow.setContent(browserHasGeolocation ?
                              'Error: The Geolocation service failed.' :
                              'Error: Your browser doesn\'t support geolocation.');
        infoWindow.open(map);
      }

// Function used for displaying/hiding the traffic information using a check variable 
var trafficCheck = 0;
function toggleTraffic(btn){
    // Function activated by show/hide button for traffic
    // The variable 'trafficCheck' acts as a semaphore
    //The appearrance of the button also changes depending on the value
    if (trafficCheck === 0){
        var mapProp= {
            center:new google.maps.LatLng(53.347515, -6.265377),
            zoom:12,
        };
        var map=new google.maps.Map(document.getElementById("map"),mapProp);
        var trafficLayer = new google.maps.TrafficLayer();
        trafficLayer.setMap(map);
        document.getElementById("trafficButton").innerHTML = "Hide Traffic";
        trafficCheck++;
        
    } else{
        var mapProp= {
            center:new google.maps.LatLng(53.347515, -6.265377),
            zoom:12,
        };
        var map=new google.maps.Map(document.getElementById("map"),mapProp);
        document.getElementById("trafficButton").innerHTML = "Traffic";
        trafficCheck--;
    }
}

//this function is responsible for the autocomplete function for the source input box in the form on the stops page
$(function() {
    $("#autocomplete").autocomplete({
      source: "api/getSource/",
      select: function (event, ui) { //item selected
        AutoCompleteSelectHandler(event, ui)
      },
      minLength: 1,
    });
  });

  function AutoCompleteSelectHandler(event, ui)
  {
    var selectedObj = ui.item;
  } 


//this function is responsible for the autocomplete function for the source input box in the form on the routes page

  $(function() {
    $("#dAdd").autocomplete({
      source: "api/getAddressDestination/",
      select: function (event, ui) { //item selected
        AutoCompleteSelectHandler(event, ui)
      },
      minLength: 3,
    });
  });

  function AutoCompleteSelectHandler(event, ui)
  {
    var selectedObj = ui.item;
  } 

  //this function is responsible for the autocomplete function for the destination input box in the form on the routes page

  $(function() {
    $("#sAdd").autocomplete({
      source: "api/getAddressDestination/",
      select: function (event, ui) { //item selected
        AutoCompleteSelectHandler(event,  ui)
      },
      minLength: 3,
     
    });
  });

  function AutoCompleteSelectHandler(event, ui)
  {
    var selectedObj = ui.item;

  } 

var swap = 0;
function swapDirection() {
    // Function to swap source address to destination and vica versa
    // Currently only set to swap names
    if (swap === 0){
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
$(document).ready(function(){
    $("input:radio[id=return]").click(ena)
});

$(document).ready(function(){
    $("input:radio[id=single]").click(disa)
});

var ena = function() {
    $("#id_returnDate").prop( "disabled", false );
    $("#id_returnTime").prop( "disabled", false );
    $("#id_returnDate").css("background-color", "white");
    $("#id_returnTime").css("background-color", "white");
    $("#id_returnDate").css("opacity", "1");
    $("#id_returnTime").css("opacity", "1");
    
}
var disa = function() {
    $("#id_returnDate").prop( "disabled", true);
    $("#id_returnTime").prop( "disabled", true);
    $("#id_returnDate").css("background-color", "lightgrey");
    $("#id_returnTime").css("background-color", "lightgrey");
    $("#id_returnDate").css("opacity", "0.4");
    $("#id_returnTime").css("opacity", "0.4");
}


$(document).ready(function(){ 
    $("#planner-toggle").click(function() {
    
        $("#planner").slideToggle( "slow");

        if ($("#planner-toggle").text() == "Expand Route Planner"){			
            $("#planner-toggle").html("Hide Route Planner")
        }

        else if ($("#planner-toggle").text() == "Hide Route Planner") {		

            $("#planner-toggle").text("Expand Route Planner")
        }
        });
    });


//Autocomplete initialisation for the route planner form source
$(function() {
    $('input[name=source]').autocomplete({
        source: "api/getSource/", 
        select: function (event, ui) { //item selected
        AutoCompleteSelectHandler(event, ui)
      },
      minLength: 1,
    });
  });
 
  function AutoCompleteSelectHandler(event, ui){
    var selectedObj = ui.item;
  }

//Autocomplete initialisation for the route planner form destination
$(function() {
    $("#id_destination").autocomplete({
        source: "api/getDesintation/",
        select: function (event, ui) { //item selected
        AutoCompleteSelectHandler(event, ui)
      },
      minLength: 1,
    });
  });

  function AutoCompleteSelectHandler(event, ui){
    var selectedObj = ui.item;
  }

  //this function is responsible for the autocomplete function for the destination input box in the form on the stops page

  $(function() {
    $("#id_destination").autocomplete({
    source: "api/getDesintation/",
    select: function (event, ui) { //item selected
        AutoCompleteSelectHandler(event, ui)
    },
    minLength: 1,
    });
});

function AutoCompleteSelectHandler(event, ui)
{
    var selectedObj = ui.item;
}



//Function to swap the autocomplete in the form between the stop numbers and the stop addresses.
function swapSearch() {

    //Checks which option is selected between searching by stops or addresses
    var c = document.getElementById("stopSearch").style.backgroundColor;

    if (c != "black") {
        //Changes the colour of the tab and placeholder of the search form
        document.getElementById("stopSearch").style.backgroundColor = "black";

        document.getElementById("addSearch").style.backgroundColor = "#00743F";
        document.getElementById('id_source').placeholder = 'Source Address..';

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

                //Accessing the lattitude and longtitude for the source and destination stop. 
                sourceLat = source.geometry.location.lat();
                sourceLong = source.geometry.location.lng();
                destinationLat = destination.geometry.location.lat();
                destinationLong = destination.geometry.location.lng();
                

                //parsing them to create floats. 

                var startLat = parseFloat(sourceLat);
                var startLng = parseFloat(sourceLong);
                var finLat = parseFloat(destinationLat);
                var finLng = parseFloat(destinationLong);

                var directionsService = new google.maps.DirectionsService();

                //creating start and finish google map lattitudes and longtitides.
                var start = new google.maps.LatLng(startLat, startLng);
                var end = new google.maps.LatLng(finLat, finLng);


                //calculating the route
                function getStopId() {
                    var request = {
                        origin: start,
                        destination: end,
                        travelMode: 'TRANSIT',
                        transitOptions: {

                            modes: ['BUS'],
                            routingPreference: 'FEWER_TRANSFERS'
                        },
                    };

                    directionsService.route(request, function (response, status) {
                        if (status == 'OK') {

                            //creating a variable to iterte over from the response returned. 
                            var x = response.routes[0].legs[0].steps;

                            var buses = []

                        
                            //iterating over the results 
                            for (var i = 0; i < x.length; i++) {

                                //checking if there is a transit response
                                if (x[i].transit) {

                                    buses.push(x[i].transit.line.short_name)
                                    //if there is, access the arrival stop and departure stop lattiitudes and longtitudes. 
                                    var DLat = x[i].transit.arrival_stop.location.lat();
                                    var DLong = x[i].transit.arrival_stop.location.lng();
                                    var SLat = x[i].transit.departure_stop.location.lat();
                                    var Slong = x[i].transit.departure_stop.location.lng();

                                    //i had issues where what was being returned was rounded off differently than the stops we have in our data so I rounded them
                                    var destLatitude = parseFloat(DLat.toFixed(4));
                                    var destLongtitude = parseFloat(DLong.toFixed(4));
                                    var sourceLatitude = parseFloat(SLat.toFixed(3));
                                    var sourceLongtitude = parseFloat(Slong.toFixed(3))

                                    //access our bus data because we need to get the stop number for the model. 

                                   
                                    $.ajax({
                                        type: "GET",
                                        url: "dublinBusInfo",
                                        dataType: "json",

                                        success: function (data) {


                                            //Iterate over the data
                                            for (var i = 0; i < data.length; i++) {

                                                //creating variables from our data to compare to the lattitudes and longtitudes from the returned arrival and destination stops from google. 
                                                var comparisonLat = parseFloat(data[i].lat).toFixed(4)
                                                var comparisonLong = parseFloat(data[i].lng).toFixed(4)
                                                var comparisonLat1 = parseFloat(data[i].lat).toFixed(3)
                                                var comparisonLong1 = parseFloat(data[i].lng).toFixed(3)


                                                //Check if they match, return the num and name
                                                if (destLatitude == comparisonLat && destLongtitude == comparisonLong) {

                                                    console.log(data[i].num);
                                                    console.log(data[i].name);


                                                }

                                                //check if they match then return the num and name
                                                if (sourceLatitude == comparisonLat1 && sourceLongtitude == comparisonLong1) {

                                                    console.log(data[i].num);
                                                    console.log(data[i].name);

                                                }

                                            }

                                            //view the routes that can be taken.
                                            console.log(buses);

                                        }
                                    });





                                }


                            }

                        }

                    })



                }

                 getStopId();

            })
        })


    } else {
        //Changes the colour of the tab and placeholder of the search form
        document.getElementById("addSearch").style.backgroundColor = "black";

        document.getElementById("stopSearch").style.backgroundColor = "#00743F";
        document.getElementById('id_source').placeholder = 'Source Stop..';



        //This is needed to remove the google maps api before changing it to search by roots. 
        //Reference: //https://stackoverflow.com/questions/9828856/how-to-toggle-the-google-maps-autocomplete-on-and-off
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

//Functions to display/hide the stop search and route search
function findStop(){
    if (document.getElementById("stopSearchOptions").style.display == "none"){
        document.getElementById("stopSearchOptions").style.display = "block";
        document.getElementById("routeSearchOptions").style.display = "none";
    } else {
        document.getElementById("stopSearchOptions").style.display = "none";
    }
}
function findRoute(){
    if (document.getElementById("routeSearchOptions").style.display == "none"){
        document.getElementById("routeSearchOptions").style.display = "block";
        document.getElementById("stopSearchOptions").style.display = "none";
    } else{
        document.getElementById("routeSearchOptions").style.display = "none";
    }
}

//Autocomplete for Route Search
$(document).ready(function() {
    $.ajax({
      type: "GET",
      url: "dublinBusRoutes",
      dataType: "json",
     
       success: function(data) {createArray(data);}
   });
  });
  
  
  function createArray(Data) {
  
  var results = [];
  for (var i = 0; i < Data.length; i++){
      results.push(Data[i].route);
  }
  $( "#routeSearch" ).autocomplete({
      source: results,
      minLength: 1,
  });
     
} 

//Load stop search on initial page load
$(document).ready(function() {
    $.ajax({
      type: "GET",
      url: "RouteInfo",
      dataType: "json",
     
       success: function(data) {createArray(data);}
   });
  });
  
  
  function createArray(Data) {
  
  var results = [];
  for (var i = 0; i < Data.length; i++){
      results.push(Data[i].num);
  }
  $( "#id_destination, #id_source" ).autocomplete({
      source: results,
      minLength: 2,
  });
     
} 


// References:
// https://github.com/jonthornton/jquery-timepicker 
//http://api.jqueryui.com/datepicker/