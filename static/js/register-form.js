$(document).ready(function(){
    $('form[name="register-form"]').submit(function(event) {
        var recaptcha = grecaptcha.getResponse();
        if (recaptcha === "") {
            event.preventDefault();
            $(".g-recaptcha").css({"border": "1px solid #a94442", "border-radius": "4px"});
        }
    });
});