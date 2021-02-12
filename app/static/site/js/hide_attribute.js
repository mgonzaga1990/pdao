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
        //default
        $('.field-others').hide();

        if (django.jQuery('#id_status_0').is(':checked')) {
            show();
        } else {
            hide();
        }

         django.jQuery('#id_occupation').click(function() {
            var id = $("#id_occupation").val();
            if(id == 10){
                $('.field-others').show();
            }else{
                $('.field-others').hide();
            }
        });

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