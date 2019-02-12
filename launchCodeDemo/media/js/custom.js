/**
 * Created by ernesto on 8/26/15.
 */
$body = $("body");

$(document).on({
    ajaxStart: function() { $body.addClass("loading");  },
    ajaxStop: function() { $body.removeClass("loading"); }
});

$(".view-prices").on("click", function (e) {
    e.preventDefault();

    obj = $(this);

    if(obj.parents(".sail-offer").find(".prices-form-wrapper").is(':visible'))
    {
        obj.parents(".sail-offer").removeClass('dropup');
        obj.html('View All Sailings & Pricing '+'<span class="caret"></span>');
        obj.parents(".sail-offer").find(".prices-form-wrapper").stop(true, true).slideToggle();
    }
    else{
        $.get('/all-pricing/', {
                    't_unique_id':$(this).attr('unique_id')
                            },
            function(data){
                obj.parents(".sail-offer").find(".prices-form-wrapper").html(data);
                obj.parents(".sail-offer").find(".prices-form-wrapper").stop(true, true).slideToggle();
            }
        );
        obj.parents(".sail-offer").addClass('dropup');
        obj.html('Hide Pricing '+'<span class="caret"></span>');
    }

});

$("#cruise-line-filter").change(function(e){

    var obj = $('#'+e.currentTarget.id+' option:selected');
    $.get('/ship-by-cruise/',
            {
                cruise_line_id: $('#'+e.currentTarget.id+' option:selected').attr('cruiseid')
            },
            function(data)
            {
                $('#ship-filter').html('<option value="0">');
                for(key in data)
                {
                    var option = $('<option>')
                    option.attr('value', data[key].name);
                    option.html(data[key].name);
                    $('#ship-filter').append(option);
                }
                $('#ship-filter').trigger("chosen:updated");
            },
        'json'
    )
});

$(".filter-form").submit(function(e) {
        ($(this).find('select').each(function(){
            var option_select = $(this).children('option:selected').attr('value');
            if(option_select == '0')
            {
                $(this).attr('disabled', 'disabled')
            }

        }));
    });

$(".menu_contact").click(function(){
    var height = $(document).height();
    height = height + 'px';
    $("html, body").animate({scrollTop: height}, speed = 0);
});

$(".follow_us").click(function(){
    var height = $(document).height()-750;
    height = height + 'px';
    console.log(height)
    $("html, body").animate({scrollTop: height}, speed = 0);
    //$(location).attr('href',  $(location).attr('href')+'#footer-socials');
});

$(".get-deals-button").click(function () {
    var input = $(".get-deals-button").parents('form').find(".input-mail-address")
    var email = input.val();
    var floatBtn = $(".get-deals-button").parents('.floating-btn')
    if (email_validation(email)) {
        $.post('/add_subscriber/', {email: email, 'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val()},
            function (data) {
                if (data.success == 1) {
                    floatBtn.removeClass("open");
                    input.val('');
                    $('#menu_error_label').hide()
                } else
                    $('#menu_error_label').show()
            }, 'json'
        )
    }

});

$("#header-deal-submit").click(function () {
    var input = $("#header-deal-submit").parents('form').find(".input-mail-address")
    var email = input.val();
    if (email_validation(email)) {
        $.post('/add_subscriber/', {email: email, 'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val()},
            function (data) {
                if (data.success == 1) {
                    $("#header-get").slideToggle();
                    input.val('');
                    $('#menu_error_label').hide()
                } else
                    $('#menu_error_label').show()
            }, 'json'
        )
    }

});



function email_validation(email_value)
{
    var filter = /[\w-\.]{3,}@([\w-]{2,}\.)*([\w-]{2,}\.)[\w-]{2,4}/;
    if(filter.test(email_value))
    {
        return true;
    }
    else
    {
        return false;
    }
}

$(document).ready(function(){

    if (window.matchMedia('(max-width: 960px)').matches) {
        $('.search-button').html('search')
    } else {
        $('.search-button').html('search your cruise')
    }

    loc = $(location).attr('href');
    if (window.matchMedia('(max-width: 540px)').matches && loc.search('/search/') > 0) {
        $('.blue-section').css('margin-top', '100px');
    }

    $("#footer-deal-submit").click(function(){
        var input = $("#footer-deal-submit").parents('form').find(".input-mail-address")
        var email = input.val();
        if(email_validation(email))
        {
            $.post('/add_subscriber/',
                            {
                                email: email,
                                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                            },
                function(data)
                {
                    if(data.success == 1)
                    {
                        $("#footer-get").fadeToggle();
                        input.val('');
                        $("#menu_error_label_bottom").hide();
                    }
                    else{
                        $("#menu_error_label_bottom").show();
                    }

                }
            )
        }

    });

    $("#deal-submit").click(function () {
        var email = $("#get-deals").val();
        //console.log(email);
        if (email_validation(email)) {
            $.post('/add_subscriber/', {
                    email: email,
                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
                },
                function (data) {
                    if (data.success == 1) {
                        $("#get-deals").val('');
                        $('label[for=get-deals]').html('Get weekly cruise deals')
                    } else {
                        $('label[for=get-deals]').html('This email already exist!')
                    }
                }
            )
        }

    })

    $("#accordion").on('show.bs.collapse', function() {
        $("#accordion").find('.collapse.in').collapse('hide');
    });


    $("#datepicker").MonthPicker(
        {
            MinMonth: 0,
            StartYear: Date.year,
            Button: false,
            defaultValue: new Date(),


        });

    $("#login").click(function(){
        var username = $("#username").val();
        var password = $("#password").val();

        $.post('/login/', {
                    username: username,
                    password: password,
                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
                },
                function (data) {
                    if (data.success == 0) {
                        $("#loginerror").html(data.message);
                        $("#loginerror").show();
                    }
                    else{
                        location.reload();
                    }
                }
            )
    });

    $("#createUserButton").click(function(){
        var username = $("#email").val();
        var cpassword = $("#cpassword").val();
        var crpassword = $("#crpassword").val();
        var is_valid = true;
        $("#signUPerror").html("");
        if(username == '' || !email_validation(username))
        {
            $("#signUPerror").html("Invalid Email!<br>");
            is_valid = false;
        }
        if (cpassword != crpassword) {
            $("#signUPerror").html($("#signUPerror").html() + "The password doesn't match")
            is_valid = false;
        }
        if(is_valid== false){
            $("#signUPerror").show();
            return;
        }else {

            $.post('/create_user/', {
                    username: username,
                    password: cpassword,
                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
                },
                function (data) {
                    if (data.success == 0) {
                        $("#loginerror").html(data.message);
                        $("#loginerror").show();
                    }
                }
            )
        }
    });

    $(".signUP").click(function(){
        $('#tablistUser li:nth-child(2) a').tab('show')
        $(".navigation-list").slideToggle(200);
    })
    $(".login").click(function(){
        $(".navigation-list").slideToggle(200);
        $('#tablistUser li:nth-child(1) a').tab('show')
    })

    $(".toggle-save-travel").click(function(e){
        var attr = $(this).attr('delete_row');
        var travel_id = $(this).attr('travel_id');
        $.get('/save-travel?',
            {
                'travel_id': travel_id
            },

            function(data){

                if(typeof attr !== typeof undefined && attr !== false){
                    $("#travel_row_id" + travel_id).fadeOut(500);
                }

                if(data.success == 1)
                {
                   $(".saved" + travel_id).show();
                   $(".unsave"  + travel_id).hide();


                }
                if (data.success == 2){

                   $(".saved"  + travel_id).hide();
                   $(".unsave"  + travel_id).show();
                }

            })

    })

})
