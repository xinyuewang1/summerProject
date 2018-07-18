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

function timeEstimate() {

    //Function for the actions taken by the 'Go!' button on the stops page
    //it causes the url generation to get the information the user has chosen
    //for the moment these simply display what the user has chosenbut later, they will cause queries to take place.

    var jqxhr =  $.getJSON( '/'+document.getElementById("departTime").value+'/', function( deptTime ){

        //this function displays the departure time chosen

        document.getElementById("timeEst").innerHTML = deptTime;
    }  
    );

    var jqxhr2 =  $.getJSON( 'return/'+document.getElementById("returnDepartTime").value+'/', function( returntime ){

         //this function displays the departure return time chosen

        document.getElementById("returnTimeEst").innerHTML = returntime;
    }
    )

    var jqxhr3 =  $.getJSON( 'month/'+document.getElementById("departDate").value+'/', function( deptdate ){

         //this function displays the departure departure date chosen

        document.getElementById("monthChosen").innerHTML = deptdate;
    }
    )


    var jqxhr4 =  $.getJSON( 'return/month/'+document.getElementById("returnDepartDate").value+'/', function( returndate ){

         //this function displays the departure departure time chosen

        document.getElementById("retmonthChosen").innerHTML = returndate;
    }
    )
};


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


//Autocomplete for index 
$(function() {
    $("#id_source").autocomplete({
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



// References:
// https://github.com/jonthornton/jquery-timepicker 
//http://api.jqueryui.com/datepicker/