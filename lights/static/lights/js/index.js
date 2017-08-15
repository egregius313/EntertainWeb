var form_enabled = true; //Prevent button spamming
var overlay;
var color_picker_btn;
var palette;
var remote_buttons;
var css_style_str;
var last_button;

$(document).ready(function () {
    overlay = $("#loading-overlay");
    color_picker_btn = $('#color_picker_btn');
    palette = $('#palette');
    remote_buttons = $('.remote_button');
    css_style_str = 'rgb(' + color_picker_btn.attr('data-message') + ')';

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

    color_picker_btn.click(function () {
        last_button = color_picker_btn;
        if (color_picker_btn.text() === 'Custom Color') {
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
                    complete: function (data) {

                        parse_response(data.responseText, color_picker_btn.attr('data-message'));
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

});


function parse_response(master_response, color_str) {
    form_enabled = true;
    palette.iris('hide');
    color_picker_btn.text('Custom Color');
    overlay.toggleClass("loading-anim");

    var response = JSON.parse(master_response);
    if (response['master_response'] !== 'bad request' && response['master_response'] !== 'timeout') {
        css_style_str = 'rgb(' + color_str + ')';

        $(document.body).css('background', css_style_str);
        remote_buttons.css('color', css_style_str);
        remote_buttons.css('border', '5px outset ' + css_style_str);

        if($('.is_mobile_device').css('display') === 'none')
            last_button.css('background', '#FFF');
    }
}


function button_pressed(button) {
    last_button = $(button);
    palette.iris('hide'); // Closes color drawer and resets button
    color_picker_btn.text('Custom Color');

    if (form_enabled) {
        form_enabled = false;
        var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function () {
            if (this.readyState === 4 && this.status === 200) {
                var related_color = JSON.parse(this.responseText)['related_color'];
                parse_response(this.responseText, related_color)
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