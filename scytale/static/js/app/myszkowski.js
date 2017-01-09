(function($, APP) {
    APP.myszkowski = function(selector) {
        var update = function() {
            APP.encrypt(
                $(".plaintext pre").text(),
                $(selector).val(),
                $(".ciphertext pre"));
        };
        $(selector).on("change input", update);
        update();
    };
})(jQuery, APP || {});
