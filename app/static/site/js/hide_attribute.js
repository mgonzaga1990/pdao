window.addEventListener("load", function() {

    function hide() {
        django.jQuery(".field-category").hide();
        django.jQuery(".field-type_of_emp").hide();
        django.jQuery(".field-occupation").hide();
    }

    function show() {
        django.jQuery(".field-category").show();
        django.jQuery(".field-type_of_emp").show();
        django.jQuery(".field-occupation").show();
    }

    (function($) {
        if (django.jQuery('#id_status_0').is(':checked')) {
            show();
        } else {
            hide();
        }

        django.jQuery('#id_status_0').click(function() {
            if ($('#id_status_0').is(':checked')) {
                show();
            }
        });

        django.jQuery('#id_status_1').click(function() {
            if ($('#id_status_1').is(':checked')) {
                hide();
            }
        });
    })(django.jQuery);
});