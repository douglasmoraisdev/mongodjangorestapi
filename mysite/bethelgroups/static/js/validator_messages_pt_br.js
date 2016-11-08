jQuery.extend(jQuery.validator.messages, {
    required:"Campo obrigatório",
	minlength: jQuery.validator.format("Minimo {0} caracteres"),
	maxlength: jQuery.validator.format("Máximo {0} caracteres")    
});