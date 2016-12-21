// the "href" attribute of .modal-trigger must specify the modal ID that wants to be triggered
{% load static %}

//Google Maps
var map;

function initMap() {
    var myLatLng = {lat: -30.1291731, lng: -51.315149};

    var map = new google.maps.Map(document.getElementById('map'), {
      zoom: 15,
      center: myLatLng
    });

    var marcador = new Array();
    var infowindow = new Array();

        {% for users in member_maps %}

            marcador[{{ forloop.counter0 }}] = new  google.maps.Marker({
              position: new google.maps.LatLng({{ users.users.0.user.extra_data.addr_lat }}, {{ users.users.0.user.extra_data.addr_lng }}),
              map: map,
              title: '{% for names in users.users %} -{{ names.user.extra_data.first_name }}{% endfor %}'
            });

            var div = document.createElement('DIV');
            div.innerHTML = '<div class="cardpanel"><ul class="collection">{% for list in users.users %}    <li class="collection-item avatar">        {% if list.user.extra_data.profile_image %}            <img class="circle" src="{% static "upload/profile_images/" %}{{ list.user.extra_data.profile_image }}"> {% endif %}        <span class="title">{{ list.user.extra_data.first_name }} {{ list.user.extra_data.last_name }}</span> <a target="_blank" href="{{ base_url }}/usuario/get/{{ list.user.id }}" class=""><i class="material-icons activator">search</i></a>   </li>{% endfor %}    </ul></div>';

            infowindow[[{{ forloop.counter0 }}]] = new google.maps.InfoWindow({
                content: 'Neste endereço: '+div.innerHTML
            });

            marcador[{{ forloop.counter0 }}].addListener('click', function() {
                infowindow[[{{ forloop.counter0 }}]].open(map, marcador[{{ forloop.counter0 }}]);
            });            


        {% endfor %}

        var bounds = new google.maps.LatLngBounds();
        for (var i = 0; i < marcador.length; i++) {
            bounds.extend(marcador[i].getPosition());
        }


    map.fitBounds(bounds);
    var markerCluster = new MarkerClusterer(map, marcador, {imagePath: '{% static "images/m" %}'});

}






/*
* Trending line chart
*/
//var randomScalingFactor = function(){ return Math.round(Math.random()*10)};
var trendingLineChart;
var data = {
    labels : {{ presence_days|safe }},
    datasets : [
        {
            label: "Membros",
            fillColor : "rgba(128, 222, 234, 0.6)",
            strokeColor : "#ffffff",
            pointColor : "#FFbcd4",
            pointStrokeColor : "#ffffff",
            pointHighlightFill : "#ffffff",
            pointHighlightStroke : "#ffffff",
            data: {{ roles_presence.member|safe }}
        },
        {
            label: "Servos",
            fillColor : "rgba(128, 122, 111, 0.3)",
            strokeColor : "#80deea",
            pointColor : "#46bfbd",
            pointStrokeColor : "#80deea",
            pointHighlightFill : "#80deea",
            pointHighlightStroke : "#80deea",
            data: {{ roles_presence.leader|safe }}
        },
        {
            label: "Visitantes",
            fillColor : "rgba(222, 222, 111, 0.3)",
            strokeColor : "#80deea",
            pointColor : "#fdb45c",
            pointStrokeColor : "#80deea",
            pointHighlightFill : "#80deea",
            pointHighlightStroke : "#80deea",
            data: {{ roles_presence.visitor|safe }}
        }        
    ]
};

/*
Polor Chart Widget
PESSOAS
*/
 
var doughnutData = [
    {
        value: {{ total_roles.member }},
        color:"#F7464A",
        highlight: "#FF5A5E",
        label: "Membros"
    },
    {
        value: {{ total_roles.leader }},
        color: "#46BFBD",
        highlight: "#5AD3D1",
        label: "Servos"
    },
    {
        value: {{ total_roles.visitor }},
        color: "#FDB45C",
        highlight: "#FFC870",
        label: "Visitantes"
    }

];

/*
Trending Bar Chart
POR MES
*/

var dataBarChart = {
    labels : ["JAN","FEV","MAR","ABR","MAI","JUN"],
    datasets: [
        {
            label: "Bar dataset",
            fillColor: "#46BFBD",
            strokeColor: "#46BFBD",
            highlightFill: "rgba(70, 191, 189, 0.4)",
            highlightStroke: "rgba(70, 191, 189, 0.9)",
            data: [6, 9, 8, 4, 6, 7]
        }
    ]
};


window.onload = function(){
    var trendingLineChart = document.getElementById("trending-line-chart").getContext("2d");
    window.trendingLineChart = new Chart(trendingLineChart).Line(data, {  
        multiTooltipTemplate: "<%= datasetLabel %>:  <%= value %>",
        scaleShowGridLines : true,///Boolean - Whether grid lines are shown across the chart        
        scaleGridLineColor : "rgba(255,255,255,0.4)",//String - Colour of the grid lines        
        scaleGridLineWidth : 1,//Number - Width of the grid lines       
        scaleShowHorizontalLines: true,//Boolean - Whether to show horizontal lines (except X axis)     
        scaleShowVerticalLines: false,//Boolean - Whether to show vertical lines (except Y axis)        
        bezierCurve : true,//Boolean - Whether the line is curved between points        
        bezierCurveTension : 0.4,//Number - Tension of the bezier curve between points      
        pointDot : true,//Boolean - Whether to show a dot for each point        
        pointDotRadius : 5,//Number - Radius of each point dot in pixels        
        pointDotStrokeWidth : 2,//Number - Pixel width of point dot stroke      
        pointHitDetectionRadius : 20,//Number - amount extra to add to the radius to cater for hit detection outside the drawn point        
        datasetStroke : true,//Boolean - Whether to show a stroke for datasets      
        datasetStrokeWidth : 3,//Number - Pixel width of dataset stroke     
        datasetFill : true,//Boolean - Whether to fill the dataset with a colour                
        animationSteps: 15,// Number - Number of animation steps        
        animationEasing: "easeOutQuart",// String - Animation easing effect         
        tooltipTitleFontFamily: "'Roboto','Helvetica Neue', 'Helvetica', 'Arial', sans-serif",// String - Tooltip title font declaration for the scale label        
        scaleFontSize: 12,// Number - Scale label font size in pixels       
        scaleFontStyle: "normal",// String - Scale label font weight style      
        scaleFontColor: "#fff",// String - Scale label font colour
        tooltipEvents: ["mousemove", "touchstart", "touchmove"],// Array - Array of string names to attach tooltip events       
        tooltipFillColor: "rgba(255,255,255,0.8)",// String - Tooltip background colour     
        tooltipTitleFontFamily: "'Roboto','Helvetica Neue', 'Helvetica', 'Arial', sans-serif",// String - Tooltip title font declaration for the scale label        
        tooltipFontSize: 12,// Number - Tooltip label font size in pixels
        tooltipFontColor: "#000",// String - Tooltip label font colour      
        tooltipTitleFontFamily: "'Roboto','Helvetica Neue', 'Helvetica', 'Arial', sans-serif",// String - Tooltip title font declaration for the scale label        
        tooltipTitleFontSize: 14,// Number - Tooltip title font size in pixels      
        tooltipTitleFontStyle: "bold",// String - Tooltip title font weight style       
        tooltipTitleFontColor: "#000",// String - Tooltip title font colour     
        tooltipYPadding: 8,// Number - pixel width of padding around tooltip text       
        tooltipXPadding: 16,// Number - pixel width of padding around tooltip text      
        tooltipCaretSize: 10,// Number - Size of the caret on the tooltip       
        tooltipCornerRadius: 6,// Number - Pixel radius of the tooltip border       
        tooltipXOffset: 10,// Number - Pixel offset from point x to tooltip edge
        responsive: true,
        });

        var doughnutChart = document.getElementById("doughnut-chart").getContext("2d");
        window.myDoughnut = new Chart(doughnutChart).Doughnut(doughnutData, {
            segmentStrokeColor : "#fff",
            tooltipTitleFontFamily: "'Roboto','Helvetica Neue', 'Helvetica', 'Arial', sans-serif",// String - Tooltip title font declaration for the scale label        
            percentageInnerCutout : 50,
            animationSteps : 15,
            segmentStrokeWidth : 4,
            animateScale: true,
            percentageInnerCutout : 60,
            responsive : true
        });

        var trendingBarChart = document.getElementById("trending-bar-chart").getContext("2d");
        window.trendingBarChart = new Chart(trendingBarChart).Bar(dataBarChart,{
            scaleShowGridLines : false,///Boolean - Whether grid lines are shown across the chart
            showScale: true,
            animationSteps:15,
            tooltipTitleFontFamily: "'Roboto','Helvetica Neue', 'Helvetica', 'Arial', sans-serif",// String - Tooltip title font declaration for the scale label        
            responsive : true
        });


    
};
