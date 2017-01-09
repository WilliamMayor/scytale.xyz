(function($, APP) {
    APP.railfence = function(selector) {
        var input = $(selector).find("#rails");
        var table = $(selector).find("table");
        var generate_table = function() {
            var rails_count = parseInt(input.val());
            table.find("tr").remove();
            for (var i = 0; i < rails_count; i++) {
                var tr = $("<tr>");
                var count = rails_count - 1;
                for (var j = 0; j < 17; j++) {
                    var x_dist = j % (2 * count);
                    var y_dist = (x_dist > count) ? x_dist - count + i : x_dist + count - i;
                    var td = $("<td>");
                    if (y_dist === count) {
                        td.addClass("X");
                    }
                    tr.append(td);
                }
                table.append(tr);
            }
            APP.encrypt($(".plaintext pre").text(), rails_count, $(".ciphertext pre"));
        };
        input.on("change input", generate_table);
        generate_table();
    };
})(jQuery, APP || {});
