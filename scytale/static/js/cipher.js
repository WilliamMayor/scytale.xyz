var xgcd = function(a,b ) {
     if (b === 0) {
        return [1, 0, a];
    } else {
        temp = xgcd(b, a % b);
        x = temp[0];
        y = temp[1];
        d = temp[2];
        return [y, x - y * Math.floor(a / b), d];
    }
};
var ciphers = {
    affine: {
        init: function() {
            $("#a").val(7).change();
            $("#b").val(10).change();
        }, update: function() {
            var a = $("#a").val();
            var b = $("#b").val();
            var c = NaN;
            if ($.isNumeric(a)) {
                a = parseInt(a);
                var r = xgcd(a, 100);
                c = r[0];
                var d = r[2];
                if (d !== 1) {
                    c = NaN;
                } else if (c < 0) {
                    c += 100;
                }
                if (parseInt($("#c").val()) !== c) {
                    $("#c").val(c).change();
                }
                if ($.isNumeric(b) && $.isNumeric(c)) {
                    b = parseInt(b);
                    c = parseInt(c);
                    $(".e1").text(a * 22 + b);
                    var cipher = (a * 22 + b) % 100;
                    $(".e2").text(cipher);
                    $(".e3").text(padding.to_letters(cipher));
                    $(".e4").text(c * (cipher - b));
                }
            } else {
                $("#c").val(NaN);
            }
        }
    }
};
$(document).ready(function() {
    if ($("body.cipher").length) {
        $(".key input").on("change input", function() {
            var name = $(this).attr("id");
            var value = $(this).val();
            if (!$.isNumeric(value)) {
                value = name;
            }
            $("span." + name).text(value);
            _.each($("body").attr("class").split(" "), function(c) {
                if (ciphers[c]) {
                    ciphers[c].update();
                }
            });
        });
        _.each($("body").attr("class").split(" "), function(c) {
            if (ciphers[c]) {
                ciphers[c].init();
            }
        });
    }
});
