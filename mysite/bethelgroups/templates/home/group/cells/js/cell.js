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
            url: "http://localhost:10/bethelgroups/add_member_list_save",
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
        url: "http://localhost:10/bethelgroups/remove_member_list_save",
        data: { userid: user_selected, origin: group, origin_id: group_id}
        })
        .fail(function( ){
            $('#loader-member-cell-added').hide();
            alert("Erro");
        })                        
        .done(function( msg ) {

            remove_user(user_id);
            $('#loader-member-cell-added').hide();
            alert("removido com sucesso");

        });

}

//Google Maps
var map;


function initMap() {
    var myLatLng = {lat: -30.1291731, lng: -51.315149};

    var map = new google.maps.Map(document.getElementById('map'), {
      zoom: 15,
      center: myLatLng
    });

    var marker = new Array();

    marker[0] = new google.maps.Marker({
      position: {lat: -30.1291731, lng: -51.315149},
      map: map,
      title: 'Hello World!',
      //icon:'{% static "upload/profile_images/" %}douglas.jpg'
    });
    marker[1] = new google.maps.Marker({
      position: {lat: -30.1312171, lng: -51.3143318},
      map: map,
      title: 'Hello World!'
    });
    marker[2] = new google.maps.Marker({
      position: {lat: -30.1515134802915, lng: -51.3381549802915},
      map: map,
      title: 'Hello World!'
    });

    var bounds = new google.maps.LatLngBounds();
    for (var i = 0; i < marker.length; i++) {
     bounds.extend(marker[i].getPosition());
    }

    map.fitBounds(bounds);    

}