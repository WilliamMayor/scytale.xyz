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
    },

    clean: function(elm, alphabet) {
        var val = elm.val().toUpperCase(),
            not_alphabet = new RegExp("[^" + alphabet + "]", "g");
        val = val.replace(not_alphabet, "");
        var start = elm[0].selectionStart;
        elm.val(val);
        elm[0].selectionStart = elm[0].selectionEnd = start;

    }
};
