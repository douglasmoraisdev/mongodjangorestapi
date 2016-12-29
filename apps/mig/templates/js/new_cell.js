$('select').material_select();


function anyThing() {
    setTimeout(function() {
        $('.stepper').nextStep();
    }, 150);
}

$(function() {
    $('.stepper').activateStepper();    
});


$(document).ready(function () {
    // the "href" attribute of .modal-trigger must specify the modal ID that wants to be triggered
    $('#servant-modal-trigger').leanModal({
        dismissible: false,
        ready: function(modal, trigger) { // Callback for Modal open. Modal and trigger parameters available.

            $('#cell-role-multiple').prop('selectedIndex', 0); //Sets the first option as selected
            $('#cell-role-multiple').material_select();    

            $('#result-search-users').html('');
        },                
        complete: function(){

            $('#user_searched_selected').val('');
            $('#cell-role-multiple').val('');

        }
    });

    $('#member-modal-trigger').leanModal({
        dismissible: false,
        ready: function(modal, trigger) { // Callback for Modal open. Modal and trigger parameters available.

            $('#cell-role-multiple').prop('selectedIndex', 0); //Sets the first option as selected
            $('#cell-role-multiple').material_select();    

            $('#result-search-users').html('');
        },                
        complete: function(){


            user_selected = $('#member_searched_selected').val();
            roles_selected = $('#member_role_selected').val();

            $('#loader-member-cell-added').show();                    

            $.ajax({
                method: "GET",
                dataType: "html",
                url: "{{ base_url }}/usuario/add_member_list",
                data: { userid: user_selected, rolesid: roles_selected}
                })
                .fail(function(){
                    $('#loader-member-cell-added').hide();
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



/* Field validators */
jQuery.validator.setDefaults({

  rules: {

    'cell-name': {
      required: true,
      minlength: 3,
      maxlength: 25
    },
    'cell-date':'required',
    'cell-zip':'required',
	'cell-state':{
		required:true,
		minlength: 2,
		maxlength: 25
	},
	'cell-city':{
		required:true,
		minlength: 3,
		maxlength: 25
	},
	'cell-neigh':{
		required:true,
		minlength: 3,
		maxlength: 25
	},	
	'cell-street':{
		required:true,
		minlength: 3,
		maxlength: 25
	},		
	'cell-street-number':{
		required:true,
		maxlength: 25
	},	
  }
});

jQuery(function($){
   $("#cell-zip").mask("99999-999");
});    
