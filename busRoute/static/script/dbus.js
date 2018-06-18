function myMap() {
    var mapProp= {
        center:new google.maps.LatLng(53.347515, -6.265377),
        zoom:12,
    };
        var map=new google.maps.Map(document.getElementById("map"),mapProp);
}


var check = 0;
function toggleTraffic(btn){
    if (check === 0){
        var mapProp= {
            center:new google.maps.LatLng(53.347515, -6.265377),
            zoom:12,
        };
        var map=new google.maps.Map(document.getElementById("map"),mapProp);
        var trafficLayer = new google.maps.TrafficLayer();
        trafficLayer.setMap(map);
        document.getElementById("trafficButton").innerHTML = "Hide Traffic";
        btn.style.backgroundColor = "lightgrey";
        check++;
        
    } else{
        var mapProp= {
            center:new google.maps.LatLng(53.347515, -6.265377),
            zoom:12,
        };
        var map=new google.maps.Map(document.getElementById("map"),mapProp);
        document.getElementById("trafficButton").innerHTML = "Show Traffic";
        btn.style.backgroundColor = "rgb(250,219,50)";
        check--;
    }
}
//function disableBtn() {
//    document.getElementById("dis").disabled = true;
//    document.getElementById("dis2").disabled = true;
//}

var swap = 0;
function swapAdd() {
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
    document.getElementById("timeEst").innerHTML = "<p>Next Bus leaves at: </p>";
}


// ---------------- Jquery ----------------
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

//$("input:radio[name=sam1]").click(disp)



// References:
// https://github.com/jonthornton/jquery-timepicker 
//http://api.jqueryui.com/datepicker/