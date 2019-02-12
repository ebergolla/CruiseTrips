/**
 * Created by R41m3L on 07/17/2015.
 */
$(function(){

    $.each($(".bg-image"), function (){
        $(this).css({
            "background-image" : "linear-gradient(to bottom, rgba(255,255,255,1), rgba(255,255,255,0) 65%), url(" + $(this).find(".to-bg").attr("src") + ")"
        });
    });

    $("#header-suscription").on("click", function (e) {
        e.preventDefault();
        $("#header-get").slideToggle();
    });

    $("#footer-suscription").on("click", function(e) {
        e.preventDefault();
        $("#footer-get").fadeToggle();
    });

    $(".search-trigger").on("click", function (e) {
        e.preventDefault();
        $(".search-box").slideToggle(200);
    });

    $("#bt-search-mobile").click(function(e){
        e.preventDefault();
         $(".navigation-list").slideToggle(200);
    });

    $("#menu-trigger").on("click", function () {
        $(".navigation-list").slideToggle(200);
        $("#search-mobile").fadeOut(200);

    });

    $(".main-navigation").height($(".main-logo").outerHeight());

    $(".details-prices").css("min-height", $(".details-info").outerHeight()+"px");

    $(".chosen-select").chosen({disable_search_threshold: 5});
    $(".chosen-select-sort").chosen({disable_search_threshold: 5});

    //view prices trigger
    /*$(".view-prices").on("click", function (e) {
        e.preventDefault();
        $(this).parents(".sail-offer").find(".prices-form-wrapper").stop(true, true).slideToggle();
    });*/

    var floatBtn = $(".floating-btn");
    $(document).on("scroll", function() {
        if ($(document).scrollTop() > $(".site-header").outerHeight() && $(document).scrollTop() < $(".site-footer").offset().top - 70 ) {
            floatBtn.css("right", "0")
        } else {
            floatBtn.removeClass("open").css("right", "-25px");
        }
    });

    floatBtn.find("img").on("click", function(e) {
        e.preventDefault();
        floatBtn.toggleClass("open");
    });

    //carousels
    $("#main-carousel").slick({
        arrows: false,
        dots: false,
        fade: true,
        autoplay: true,
        autoplaySpeed: 3000,
        pauseOnHover: false, 
        slidesToShow: 1,
        slidesToScroll: 1
    });


    //set columns to same height
    var row = $('.equalize');
    $.each(row, function() {
        var maxh=0;
        $.each($(this).find('div[class^="col-"]'), function() {
            if($(this).height() > maxh)
                maxh=$(this).height();
        });
        $.each($(this).find('div[class^="col-"]'), function() {
            $(this).height(maxh);
        });
    });


    var box = $('.box-equalized');
    var maxh=0;
    $.each(box, function() {
        if ($(this).height() > maxh) {
            maxh=$(this).height();
        }
    });
    $.each(box, function() {
        $(this).height(maxh);
    });
});
