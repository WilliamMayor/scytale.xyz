(function($, APP) {
    APP.fleissner = function(selector, key_input, init_key) {
        var cells = $(selector).find("table td");
        var key = $(selector).find(".key pre");

        var generate_key = function() {
            var text = cells.map(function(i, e) {
                if ($(e).hasClass("X")) {
                    return "X";
                }
                return "o";
            }).get().join("");
            key.text(text);
            if (key_input) {
                $(key_input).val(text);
            }
            if (key.length) {
                APP.encrypt($(".plaintext pre").text(), text, $(".ciphertext pre"));
            }
        };

        var toggle_cell = function(cell) {
            if (cell.hasClass("X")) {
                cell.removeClass("X");
            } else {
                var id = cell.data("id");
                $("td[data-id='" + id + "']").removeClass("X");
                cell.addClass("X");
            }
            generate_key();
        };

        cells.click(function() {
            var cell = $(this);
            toggle_cell(cell);
        });

        if (init_key) {
            for (var i=0; i < init_key.length; i++) {
                if (init_key[i] === "X") {
                    toggle_cell(cells.eq(i));
                } else {
                    cells.eq(i).removeClass("X");
                }
            }
        }
        generate_key();
    };
})(jQuery, APP || {});
