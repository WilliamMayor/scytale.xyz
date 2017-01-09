var APP = {
    encrypt: function(plaintext, key, out_elem) {
        out_elem.text("Encrypting...");
        APP.error("");
        var req = $.post("", {plaintext: plaintext, key: key});
        req.success(function(ciphertext) {
            out_elem.text(ciphertext);
        });
        req.fail(function(msg) {
            out_elem.text("Error!");
            APP.error(msg.responseText);
        });
    },

    error: function(msg) {
        $(".error").text(msg);
    }
};
