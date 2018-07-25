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

function showRoute() {
    var x = document.getElementById("routeResult");
    x.style.display = 'block';
}

$(document).ready(function() {
    $("#routePlanner").submit(function(e) {
      $("#routeResult").show();
    });
  });

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
        else {		
            $("#planner-toggle").text("Expand Route Planner")
        }
        });
    });


//Function to swap the autocomplete in the form between the stop numbers and the stop addresses.
function swapSearch() {

    //Checks which option is selected between searching by stops or addresses
    var c =  document.getElementById("stopSearch").style.backgroundColor;

    if (c != "black") {
        //Changes the colour of the tab and placeholder of the search form
        document.getElementById("stopSearch").style.backgroundColor = "black";
        document.getElementById("addSearch").style.backgroundColor = "rgb(105,143,123)";
        document.getElementById('id_source').placeholder = 'Source Address..';

        //Changes the autocomplete in the source to address based on name
        //     $('input[name=source]').autocomplete({
     
   
    //Autocomplete for Stop Num in the Destination Input
  
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
        
    } else {
        //Changes the colour of the tab and placeholder of the search form
        document.getElementById("addSearch").style.backgroundColor = "black";
        document.getElementById("stopSearch").style.backgroundColor = "rgb(105,143,123)";
        document.getElementById('id_source').placeholder = 'Source Stop..';

        //Autocomplete for Stop Addresses in the Destination Input
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
              results.push(Data[i].name);
          }
          $( "#id_destination, #id_source" ).autocomplete({
              source: results,
              minLength: 2,
          });
             
        } 

    }   
};

function generateQuery() {

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
                        
                        var ti = x[i].arrivaldatetime.slice(11,);
                        
                        var array = ti.split(":");
                        temp.setHours(array[0]);
                        temp.setMinutes(array[1]);
                        temp.setSeconds(array[2]);
                        var difference = new Date();
                        difference.setTime(temp-now);
                        var m = difference.getMinutes();
                        
                        if (difference.getSeconds() >= 30){
                            m = m + 1;
                        };
                        if (m == 0){
                            m = "Due"
                        } else{
                            m = String(m) + " mins"
                        };
              
                        table += "<tr>";
                        table += "<td>" + x[i].route + "</td>";
                        table += "<td>" + x[i].destination + "</td>";
                        table += "<td>" + ti.slice(0 ,5) + "</td>";
                        table += "<td>" + m + "</td>";
                        table += "</tr>";
                        }
                    table += "</tbody></table>";
                    document.getElementById("realtimeTable").innerHTML = table;
                    
        })
    };



// References:
// https://github.com/jonthornton/jquery-timepicker 
//http://api.jqueryui.com/datepicker/
 //the code for the new Autocmplete function was inspired by; https://stackoverflow.com/questions/24594662/jqueryui-autocomplete-data-from-text-csv-file-with-ajax