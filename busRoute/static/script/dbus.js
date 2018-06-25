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

// function currentWeather() {
//     var jqxhr =  $.getJSON( '/'+document.getElementById("departTime").value+'/', function( today ){

//         document.getElementById("timeEst").innerHTML = today;
//     }  
// }

// function currentWeather() {
//     var jqweather = $.getJSON($SCRIPT_ROOT + "/weather", function(data) {
//         var weatherInfo = data.weatherInfo;
//         var actualTemp = weatherInfo.temp - 273.15; //turning kelvin temp to actual temp in degrees celsius
//         var actualTemp_min = weatherInfo.temp_min - 273.15;
//         var actualTemp_max = weatherInfo.temp_max - 273.15;
//         actualTemp = (actualTemp).toFixed(1) //rounding to 1 decimal place
//         var iconCode = weatherInfo.icon;
//         var icon = "http://openweathermap.org/img/w/" + iconCode + ".png";
       
//         document.getElementById("weatherDiv").innerHTML = "<h2>" + weatherInfo.date + "</h2><div id = \"icon\"><img src=" + icon +" style = \"float: left;margin-left: 15px;\">" + weatherInfo.main +"</div><div id = \"temp\"><em>" + actualTemp + "°C</em><br/><b>Min: </b>" + actualTemp_min + "°C<br/><b>Max: </b>" + actualTemp_max + "°C</div><br/><br/><br/><div id = \"line\"></div>";
            
//     })
// }

// ---------------- Jquery ----------------

//Functions to enable or disable the time and date select for return trips
$(document).ready(function(){
    $("input:radio[id=return]").click(ena)
});

$(document).ready(function(){
    $("input:radio[id=single]").click(disa)
});

var ena = function() {
    $("#returnDepartDate").prop( "disabled", false );
    $("#returnDepartTime").prop( "disabled", false );
    $("#returnDepartDate").css("background-color", "white");
    $("#returnDepartTime").css("background-color", "white");
    $("#returnDepartDate").css("opacity", "1");
    $("#returnDepartTime").css("opacity", "1");
    
}
var disa = function() {
    $("#returnDepartDate").prop( "disabled", true);
    $("#returnDepartTime").prop( "disabled", true);
    $("#returnDepartDate").css("background-color", "lightgrey");
    $("#returnDepartTime").css("background-color", "lightgrey");
    $("#returnDepartDate").css("opacity", "0.5");
    $("#returnDepartTime").css("opacity", "0.5");
}

// References:
// https://github.com/jonthornton/jquery-timepicker 
//http://api.jqueryui.com/datepicker/