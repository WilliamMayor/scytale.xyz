(function($, APP) {
    APP.checkerboard = function(selector) {
        var inputs = $(selector).find("table td input");
        var key = $(selector).find(".key code");
        var generate_key = function() {
            var text = inputs.map(function(i, e) {
                return $(e).val();
            }).get().join("");
            key.text(text);
        };
        inputs.on("change input", generate_key);
        generate_key();
    };
})(jQuery, APP || {});
