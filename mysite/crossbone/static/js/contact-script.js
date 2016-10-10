$(function() {
    var paraTag = $('input#submit').parent('p');
    $(paraTag).children('input').remove();
    $(paraTag).append('<input type="button" name="submit" id="submit" class="mtr-btn button-fab ripple" value="Send"/>');

    $('#contactform input#submit').on('click', function(event) {
    $('#contactform').append('<img src="images/ajax-loader.gif" class="loaderIcon" alt="Sending..." />');

        var name = $('input#name').val();
        var email = $('input#email').val();
        var phone = $('input#phone').val();
        var comments = $('textarea#comments').val();

        $.ajax({
            type: 'post',
            url: 'sendmail.php',
            data: 'name=' + name + '&email=' + email + '&phone=' + phone + '&comments=' + comments,

            success: function(results) {
                $('#contactform img.loaderIcon').fadeOut(1000);
                $('#sendstatus').html(results);
				//clear fields
                $('input[type="text"],textarea').val('');
            }

        }); // end ajax
    });
});
