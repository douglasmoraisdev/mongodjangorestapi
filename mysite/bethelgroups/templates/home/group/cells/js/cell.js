
$(document).ready(function () {
    // the "href" attribute of .modal-trigger must specify the modal ID that wants to be triggered
    
    $('#member-modal-trigger').leanModal({
        dismissible: false,
        ready: function(modal, trigger) { // Callback for Modal open. Modal and trigger parameters available.

            alert('teste');
            $('#cell-role-multiple').prop('selectedIndex', 0); //Sets the first option as selected
            $('#cell-role-multiple').material_select();    

            $('#result-search-users').html('');
        },                
        complete: function(){


            user_selected = $('#user_searched_selected').val();
            roles_selectec = $('#cell-role-multiple').val();

            $('#loader-member-cell-added').show();                    

            $.ajax({
                method: "GET",
                dataType: "html",
                url: "http://localhost:10/bethelgroups/add_member_list",
                data: { userid: user_selected, rolesid: roles_selectec}
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

});


function add_day_group(){

    $.get( "day_group_hmtl_frag", function( data ) {
      $( "#days_list" ).append( data );

    });          

};        


function remove_user(list_id){

    $('#'+list_id).remove();
};
