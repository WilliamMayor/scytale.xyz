(function($, APP) {
    APP.checkerboard = function(selector, alphabet) {
        var inputs = $(selector).find("table td input");
        var key = $(selector).find(".key pre");
        var first_empty = $(selector).find(".empty.first");
        var second_empty = $(selector).find(".empty.second");

        var update = function() {
            var blanks = 0;
            var text = inputs.map(function(i, e) {
                e = $(e);
                APP.clean(e, alphabet);
                var v = e.val();
                if (v === "") {v = " ";}
                if (i < 10) {
                    if (v === " ") {
                        if (blanks === 0) {
                            first_empty.text(i);
                            blanks++;
                        } else {
                            second_empty.text(i);
                        }
                    }
                }
                return v;
            }).get().join("");
            key.text(text);
            APP.encrypt($(".plaintext pre").text(), text, $(".ciphertext pre"));
        };

        inputs.on("change input", update);
        update();
    };
})(jQuery, APP || {});
