function searchExecute(){

	if ($('#globalsearch').val().trim() != ''){
	    $.ajax({
	        method: "GET",
	        dataType: "html",
	        url: "/globalsearch/"+$('#globalsearch').val(),
	        })
	        .fail(function( ){
	            alert("Erro");
	            closeSearch();
	        })                        
	        .done(function( msg ) {

				showCloseSearchButton();

	        	$('#main-row').hide(500);

	        	$('#globalsearch-result').html(msg)

	        });  
	}

}



function globalSearch(e){


        if(e.keyCode === 13){
            e.preventDefault();

			if ($('#globalsearch').val().trim() != ''){

				searchExecute();
          
			}

        }
        if (e.keyCode === 27){

			closeSearch();

        }

}

function showCloseSearchButton(){
			$("#btn-close-search").show();
			$("#icon-search").hide();
}

function closeSearch(){
	$("#btn-close-search").hide();
	$("#icon-search").show();

	$('#globalsearch').val('');
	$('#main-row').show(500);
	$('#globalsearch-result').html('')

}

