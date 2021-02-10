window.addEventListener("load", function() {

    (function($) {
        // hide brgy first
        django.jQuery(".field-barangay").hide();
        django.jQuery('#id_municipality').change(function() {
            var municipalId = $(this).val();
            console.log('selected municipal ' + municipalId);

            django.jQuery.ajax({
                url: '/ajax/fetch_brgy/' + municipalId,
                success: function(data) {
                    console.log(JSON.stringify(data))
                    django.jQuery("#id_barangay").empty();
                    django.jQuery.each(data, function(key, value) {
                        var id = value['pk'];
                        var name = value['fields']['name'];
                        django.jQuery("#id_barangay").append('<option value=' + id + '>' + name + '</option>')
                    });
                    django.jQuery(".field-barangay").show();
                }
            })
        });
    })(django.jQuery);
});