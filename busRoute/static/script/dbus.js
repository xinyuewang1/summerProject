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
        btn.style.backgroundColor = "lightgrey";
        trafficCheck++;
        
    } else{
        var mapProp= {
            center:new google.maps.LatLng(53.347515, -6.265377),
            zoom:12,
        };
        var map=new google.maps.Map(document.getElementById("map"),mapProp);
        document.getElementById("trafficButton").innerHTML = "Show Traffic";
        btn.style.backgroundColor = "rgb(250,219,50)";
        trafficCheck--;
    }
}


var swap = 0;
function swapAdd() {
    // Function to swap source address to destination and vica versa
    // Currently only set to swap names
    if (swap === 0){
        document.getElementsByName('search')[0].placeholder = 'Destination..';
        document.getElementsByName('search2')[0].placeholder = 'Source..';
        swap++;
    } else{
        document.getElementsByName('search2')[0].placeholder = 'Destination..';
        document.getElementsByName('search')[0].placeholder = 'Source..';
        swap--;
    }
}

function timeEstimate() {
   //Function for the actions taken by the 'Go!' button on the stops page
    document.getElementById("timeEst").innerHTML = "<p>Next Bus leaves at: </p>";
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
    $("#dis").prop( "disabled", false );
    $("#dis2").prop( "disabled", false );
    $("#dis").css("background-color", "white");
    $("#dis2").css("background-color", "white");
    $("#dis").css("opacity", "1");
    $("#dis2").css("opacity", "1");
    
}
var disa = function() {
    $("#dis").prop( "disabled", true);
    $("#dis2").prop( "disabled", true);
    $("#dis").css("background-color", "lightgrey");
    $("#dis2").css("background-color", "lightgrey");
    $("#dis").css("opacity", "0.5");
    $("#dis2").css("opacity", "0.5");
}

// References:
// https://github.com/jonthornton/jquery-timepicker 
//http://api.jqueryui.com/datepicker/