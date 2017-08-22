(function(){
    $(document).ready(function(){
        //setTimeout('$("div.flask-flash-message").fadeOut(1000)', 4000);
        $('html, body').animate({ scrollTop: $('.flask-flash-message').offset().top }, 'slow');
    });
})();