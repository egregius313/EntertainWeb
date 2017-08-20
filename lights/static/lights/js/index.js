var form_enabled = true; //Prevent button spamming
var overlay;
var color_picker_btn;
var palette;
var remote_buttons;
var access_code_btn;
var sign_in_overlay;
var access_code_container;
var sign_in_container;
var access_code_life;
var token_input;

var access_code = "";
var last_button;

var css_style_str;
var code_close_icon;
var code_lock_icon;
var custom_color_text;
var wait; //delays token submission
var static_dir;


$(document).ready(function () {
    overlay = $("#loading-overlay");
    color_picker_btn = $('#color_picker_btn');
    palette = $('#palette');
    access_code_btn = $('#access_code_btn');
    sign_in_overlay = $('#sign-in-overlay');
    access_code_container = $('#access-code-container');
    sign_in_container = $('#sign-in-container');
    access_code_life = $('#access_code_life');
    token_input = $('#token_input');
    remote_buttons = $('.remote_button');
    static_dir = $('#static-dir').attr('data-static-dir');


    custom_color_text = color_picker_btn.text();
    css_style_str = 'rgb(' + color_picker_btn.attr('data-message') + ')';
    code_lock_icon = access_code_btn.attr('src');
    code_close_icon = access_code_btn.attr('data-close-icon');

    palette.iris({
        hide: true,
        color: '#0e83cd',
        palettes: true,
        change: function (event, ui) {
            color_picker_btn.css('border-color', ui.color.toString());
            var rgb = ui.color.toRgb();
            color_picker_btn.attr('data-message', pad_str(rgb.r.toString(), 3) + ',' + pad_str(rgb.g.toString(), 3) + ',' + pad_str(rgb.b.toString(), 3));
        }
    });


    //Initial info request on page load
    status_request();


    color_picker_btn.click(function () {
        last_button = color_picker_btn;
        if (color_picker_btn.text() === custom_color_text) {
            palette.iris('show');
            color_picker_btn.text('Send');
        } else if (color_picker_btn.text() === 'Send') {
            if (form_enabled) {
                form_enabled = false;
                var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
                overlay.toggleClass("loading-anim");

                $.ajax({
                    url: color_picker_btn.attr('data-ajax-url'),
                    method: 'POST',
                    data: {
                        'color': color_picker_btn.attr('data-message')
                    },
                    dataType: 'json',
                    beforeSend: function (xhr) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    },
                    success: function (data) {

                        parse_server_response(data['master_response'],
                            'rgb(' + color_picker_btn.attr('data-message') + ')');
                    }
                });
            }
        }
    });

    remote_buttons.hover(function () {
            $(this).css('background', css_style_str);
            $(this).css('color', '#FFF');
        },
        function () {
            $(this).css('background', '#FFF');
            $(this).css('color', css_style_str);
        });


    access_code_btn.click(function () {

        sign_in_container.show();
        access_code_container.hide();
        access_code = "";
        $('#access_code').text("");

        sign_in_overlay.toggleClass('sign-in-anim');

        if (access_code_btn.attr('src') === code_lock_icon)
            access_code_btn.attr('src', code_close_icon);
        else
            access_code_btn.attr('src', code_lock_icon);
    });


    $('#code-submit').click(function () {
        if (form_enabled) {
            form_enabled = false;
            var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
            overlay.toggleClass("loading-anim");

            $.ajax({
                url: $('#code-submit').attr('data-ajax-url'),
                method: 'POST',
                data: {
                    'password': $('#code-password').val()
                },
                dataType: 'json',
                beforeSend: function (xhr) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                },
                success: function (data) {
                    form_enabled = true;
                    overlay.toggleClass("loading-anim");

                    if (data.responseJSON['access_token'] !== 'bad request') {
                        access_code = data.responseJSON['access_token'];
                        $('#sign-in-container').hide();

                        $('#access_code').text(access_code);
                        access_code_container.show();
                    }
                }
            });
        }
    });


    $('#life-submit').click(function () {
        if (form_enabled) {
            form_enabled = false;
            var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
            overlay.toggleClass("loading-anim");

            $.ajax({
                url: $('#life-submit').attr('data-ajax-url'),
                method: 'POST',
                data: {
                    'hours': access_code_life.val(),
                    'access_token': access_code
                },
                dataType: 'json',
                beforeSend: function (xhr) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                },
                success: function (data) {
                    form_enabled = true;
                    overlay.toggleClass("loading-anim");
                    if (data.responseJSON['response'] === 'success')
                        access_code_life.css('border-color', '#02d570');
                    else
                        access_code_life.css('border-color', '#ff4303');
                }
            });
        }
    });


    access_code_life.change(function () {
        if (access_code_life.val() > 1)
            $('#hour_label').html('&nbsp;hours.');
        else
            $('#hour_label').html('&nbsp;hour.');
    });


    token_input.change(function () {
        if (token_input.val().length === 4) {
            var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
            overlay.toggleClass("loading-anim");

            $.ajax({
                url: token_input.attr('data-ajax-url'),
                method: 'POST',
                data: {
                    'token': token_input.val()
                },
                dataType: 'json',
                beforeSend: function (xhr) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                },
                success: function (data) {
                    if (data.responseJSON['response'] === 'success') {
                        token_input.css('border-color', '#02d570');
                        location.reload();
                    }
                    else
                        token_input.css('border-color', '#ff4303');
                }
            });
        }
    });
});

function status_request() {
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    overlay.toggleClass("loading-anim");

    $.ajax({
        url: $('#status_request').attr('data-ajax-url'),
        method: 'POST',
        data: {
            'request': 'status'
        },
        dataType: 'json',
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function (data) {
            if (data['master_response'] !== 'bad request') {
                parse_status_request(data['master_response'])
            }
        }
    });
}


function parse_status_request(master_response) {
    var color_str;
    if (master_response !== 'bad request' && master_response !== 'timeout') {
        if (master_response.charAt(0) === 'c') { // 'c' would be a custom color
            color_str = 'rgb(' + master_response.substring(2) + ')';
        }
        else
            color_str = $('.' + master_response + '-bg').css('background-color');

        parse_server_response(master_response, color_str);
    }
}


function parse_server_response(master_response, color_str, svg_image) {
    svg_image = svg_image || 'none';

    form_enabled = true;
    palette.iris('hide');
    color_picker_btn.text(custom_color_text);
    overlay.toggleClass("loading-anim");
    if (master_response !== 'bad request' && master_response !== 'timeout') {
        css_style_str = color_str;

        if (master_response.charAt(0) !== 'c' && $('.' + master_response + '-bg').length) {
            $(document.body).removeAttr('style');
            $(document.body).removeClass();
            $(document.body).addClass(master_response + '-bg')
        }
        else {
            $(document.body).removeAttr('style');
            $(document.body).removeClass();
            $(document.body).css('background-color', css_style_str);
            if (svg_image !== 'none')
                $(document.body).css('background-image', 'url(' + static_dir + 'lights/media/bg/' +  svg_image + '),' + 'url(' + static_dir + 'lights/media/bg/' + svg_image + ')');
        }

        remote_buttons.css('color', css_style_str);
        remote_buttons.css('border', '5px outset ' + css_style_str);

        // if ($('.is_mobile_device').css('display') !== 'none')
        if (last_button)
            last_button.css('background', '#FFF');
    }
}


function button_pressed(button) {
    last_button = $(button);
    palette.iris('hide'); // Closes color drawer and resets button
    color_picker_btn.text(custom_color_text);

    if (form_enabled) {
        form_enabled = false;
        var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function () {
            if (this.readyState === 4 && this.status === 200) {
                var related_color = 'rgb(' + JSON.parse(this.responseText)['related_color'] + ')';
                var response = JSON.parse(this.responseText);
                parse_server_response(response['master_response'], related_color, response['svg_image'])
            }
        };
        xhttp.open("POST", document.getElementById('button-pressed-url').getAttribute('data-ajax-url'), true);
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhttp.setRequestHeader("X-CSRFToken", csrftoken);
        xhttp.send("button_id=" + button.getAttribute('data-message'));

        overlay.toggleClass("loading-anim")

    }
}


function pad_str(str, max) {
    str = str.toString();
    return str.length < max ? pad_str("0" + str, max) : str;
}