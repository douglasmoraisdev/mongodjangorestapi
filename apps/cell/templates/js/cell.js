// the "href" attribute of .modal-trigger must specify the modal ID that wants to be triggered
{% load static %}


$('#member-modal-trigger').leanModal({
    dismissible: false,
    ready: function(modal, trigger) { // Callback for Modal open. Modal and trigger parameters available.

        $('#cell-role-multiple').prop('selectedIndex', 0); //Sets the first option as selected
        $('#cell-role-multiple').material_select();    

        $('#result-search-users').html('');
    },                
    complete: function(){


        user_selected = $('#member_searched_selected').val();
        roles_selectec = $('#member_role_selected').val();
        group = 'group'
        group_id = '{{ group_id }}'

        $('#loader-member-cell-added').show();

        $.ajax({
            method: "GET",
            dataType: "html",
            url: "{{ base_url }}/usuario/add_member_list_save",
            data: { userid: user_selected, rolesid: roles_selectec, origin: group, origin_id: group_id}
            })
            .fail(function( ){
                $('#loader-member-cell-added').hide();
                alert("Erro");
            })                        
            .done(function( msg ) {

                $('#member-cell-added').append(msg);

                $('#loader-member-cell-added').hide();
            });

    }
});



function add_day_group(){

    $.get( "day_group_hmtl_frag", function( data ) {
      $( "#days_list" ).append( data );

    });          

};        


function remove_user(list_id){

    $('#member-added-'+list_id).remove();
};

function remove_user_save(user_id){

    user_selected = user_id;
    group = 'group'
    group_id = '{{ group_id }}'

    $('#loader-member-cell-added').show();                    

    $.ajax({
        method: "GET",
        dataType: "html",
        url: "{{ base_url }}/remove_member_list_save",
        data: { userid: user_selected, origin: group, origin_id: group_id}
        })
        .fail(function( ){
            $('#loader-member-cell-added').hide();
            alert("Erro");
        })                        
        .done(function( msg ) {

            remove_user(user_id);
            $('#loader-member-cell-added').hide();

        });

}


//Google Maps
var map;

function initMap() {
    var myLatLng = {lat: -30.1291731, lng: -51.315149};

    var map = new google.maps.Map(document.getElementById('map'), {
      zoom: 20,
      center: myLatLng
    });

    var marcador = new Array();
    var infowindow = new Array();

        {% for users in member_maps %}

            marcador[{{ forloop.counter0 }}] = new  google.maps.Marker({
              position: new google.maps.LatLng({{ users.users.0.user.geolocation.coordinates.0 }} , {{ users.users.0.user.geolocation.coordinates.1 }}),
              map: map,
              title: '{% for names in users.users %} -{{ names.user.first_name }}{% endfor %}'
            });

            var div = document.createElement('DIV');
            div.innerHTML = '<div class="cardpanel"><ul class="collection">{% for list in users.users %}    <li class="collection-item avatar">        {% if list.user.profile_image %}            <img class="circle" src="{% static "upload/profile_images/" %}{{ list.user.profile_image }}"> {% endif %}        <span class="title">{{ list.user.first_name }} {{ list.user.last_name }}</span> <a target="_blank" href="{{ base_url }}/usuario/get/{{ list.user.id }}" class=""><i class="material-icons activator">search</i></a>   </li>{% endfor %}    </ul></div>';

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

$('.confirm-delete-member-modal-trigger').leanModal({
    dismissible: false,
    ready: function(modal, trigger) { // Callback for Modal open. Modal and trigger parameters available.

        //$('#').clone().appendTo('#list-user-delete');
        //$('#display_user_delete')

    },
    complete: function(){
        $('#list-user-delete').html('');
    }
    
});

function update_delete_modal(user_id){

    $('#user_to_delete').val(user_id);

    $('div#user-added-info-'+user_id).clone().appendTo('#list-user-delete');


}

