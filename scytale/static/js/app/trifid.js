(function($, APP) {
    APP.trifid = function(selector) {
        var inputs = $(selector).find("table td input");
        var key = $(selector).find(".key pre");
        var generate_key = function() {
            var text = inputs.map(function(i, e) {
                var v = $(e).val();
                if (v === "") {v = " ";}
                return v;
            }).get().join("");
            key.text(text);
            APP.encrypt($(".plaintext pre").text(), text, $(".ciphertext pre"));
        };
        inputs.on("change input", generate_key);
        generate_key();
    };
})(jQuery, APP || {});
