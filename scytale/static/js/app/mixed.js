(function($, APP) {
    APP.mixed = function(selector, alphabet) {
        var update = function() {
            APP.clean($(selector), alphabet);
            APP.encrypt(
                $(".plaintext pre").text(),
                $(selector).val(),
                $(".ciphertext pre"));
        };
        $(selector).on("change input", update);
        update();
    };
})(jQuery, APP || {});
