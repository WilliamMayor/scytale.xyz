$(document).ready(function() {
    if ($("body.modulo").length) {
        var calculate = function() {
            $("#b").text($("#a").val() % $("#n").val());
        };
        $("#a").on("change input", calculate);
        $("#n").on("change input", calculate);

        $("#a").val(15);
        $("#n").val(12).change();
    }
});
