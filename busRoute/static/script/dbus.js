function myMap() {
    // Function to display the google map on startup
    var mapProp= {
        center:new google.maps.LatLng(53.347515, -6.265377),
        zoom:12,
    };
        var map=new google.maps.Map(document.getElementById("map"),mapProp);

var marker = new google.maps.Marker({
    position: myLatLng,
    map: map,
    title: 'Hello World!'
  });

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

$(function() {
    $("#autocomplete").autocomplete({
      source: "api/getSource/",
      select: function (event, ui) { //item selected
        AutoCompleteSelectHandler(event, ui)
      },
      minLength: 2,
    });
  });

  function AutoCompleteSelectHandler(event, ui)
  {
    var selectedObj = ui.item;
  } 

  $(function() {
      $("#desto").autocomplete({
      source: "api/getDesintation/",
      select: function (event, ui) { //item selected
          AutoCompleteSelectHandler(event, ui)
      },
      minLength: 2,
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

// function currentWeather() {
//     var jqxhr =  $.getJSON( '/'+document.getElementById("departTime").value+'/', function( today ){

//         document.getElementById("timeEst").innerHTML = today;
//     }  
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