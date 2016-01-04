(function($, APP) {
    APP.fleissner = function(selector) {
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
        };

        cells.click(function() {
            var cell = $(this);
            if (cell.hasClass("X")) {
                cell.removeClass("X");
            } else {
                var id = cell.data("id");
                $("td[data-id='" + id + "']").removeClass("X");
                cell.addClass("X");
            }
            generate_key();
        });
        generate_key();
    };
})(jQuery, APP || {});
