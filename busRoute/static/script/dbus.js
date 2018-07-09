function myMap() {
    // Function to display the google map on startup
    var mapProp= {
        center:new google.maps.LatLng(53.347515, -6.265377),
        zoom:12,
    };
        var map=new google.maps.Map(document.getElementById("map"),mapProp);
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

function timeEstimate() {

    //Function for the actions taken by the 'Go!' button on the stops page

    var jqxhr =  $.getJSON( '/'+document.getElementById("departTime").value+'/', function( daily ){

        document.getElementById("timeEst").innerHTML = daily;
    }  
    )};


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

// References:
// https://github.com/jonthornton/jquery-timepicker 
//http://api.jqueryui.com/datepicker/