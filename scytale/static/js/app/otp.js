(function($, APP) {

    function encrypt(plain, pad, alphabet) {
        var cipher = $.map(plain.split(""), function(pl, i) {
            var pa = pad[i % pad.length];
            pl = alphabet.indexOf(pl);
            pa = alphabet.indexOf(pa);
            var c = (pl + pa) % alphabet.length;
            return alphabet[c];
        });
        return cipher.join("");
    }

    function decrypt(cipher, pad, alphabet) {
        var plain = $.map(cipher.split(""), function(c, i) {
            var pa = pad[i % pad.length];
            c = alphabet.indexOf(c);
            pa = alphabet.indexOf(pa);
            // Need to add alphabet.length in order to force result to be
            // positive.
            var pl = (c - pa + alphabet.length) % alphabet.length;
            return alphabet[pl];
        });
        return plain.join("");
    }

    function clean(elm, alphabet) {
        var val = elm.val().toUpperCase(),
            not_alphabet = new RegExp("[^" + alphabet + "]", "g");
        val = val.replace(not_alphabet, "");
        elm.val(val);
    }

    APP.otp = function(alphabet) {
        var plain = $("#plaintext");
        var pad = $("#pad");
        var cipher = $("#ciphertext");

        plain.on("change input", function() {
            clean(plain, alphabet);
            cipher.val(encrypt(plain.val(), pad.val(), alphabet));
        });

        pad.on("change input", function() {
            clean(pad, alphabet);
            if (pad.val().length > 0) {
                cipher.val(encrypt(plain.val(), pad.val(), alphabet));
            }
        });

        cipher.on("change input", function() {
            clean(cipher, alphabet);
            plain.val(decrypt(cipher.val(), pad.val(), alphabet));
        });
    };
})(jQuery, APP || {});
