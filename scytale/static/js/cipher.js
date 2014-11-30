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
                    if (cipher < 0) cipher += 100;
                    $(".e2").text(cipher);
                    $(".e3").text(padding.to_letters(cipher));
                    $(".e4").text(c * (cipher - b));
                }
            } else {
                $("#c").val(NaN);
            }
        }, encrypt: function(a, b, plaintext) {
            var ciphertext = [];
            _.each(plaintext, function(c) {
                var n = parseInt(padding.to_numbers(c));
                var m = (a * n + b) % 100;
                if (m < 0) m += 100;
                ciphertext.push(padding.to_letters(m));
            });
            return ciphertext.join("");
        }, decrypt: function(c, b, ciphertext) {
            var plaintext = [];
            _.each(ciphertext, function(d) {
                var n = parseInt(padding.to_numbers(d));
                var m = (c*(n - b)) % 100;
                if (m < 0) m += 100;
                plaintext.push(padding.to_letters(m));
            });
            return plaintext.join("");
        }, test: function() {
            console.log("Affine tests pass: " + _.every([
                "hello" === ciphers.affine.decrypt(43,10,ciphers.affine.encrypt(7,10,"hello")),
                "hello" === ciphers.affine.decrypt(43,-99,ciphers.affine.encrypt(7,-99,"hello")),
                "hello" === ciphers.affine.decrypt(43,23456,ciphers.affine.encrypt(7,23456,"hello")),
            ]));
        }
    }, fleissner: {
        init: function() {
            $("#x").val(8).change().change();
        }, update: function() {
            var x = $("#x").val();
            if ($.isNumeric(x)) {
                if (x !== ciphers.fleissner.x) {
                    ciphers.fleissner.x = x;
                    $("#y").val(x);
                    x = parseInt(x);
                    var m = Math.floor(x / 2);
                    var is_odd = (x % 2) !== 0;
                    $(".key table tr").remove();
                    for (var i = 0; i < x; i++) {
                        var tds = [];
                        for (var j = 0; j < x; j++) {
                            var qx, qy;
                            if (is_odd ) {
                                var si = i, sj = j;
                                if (si > m) {
                                    si--;
                                }
                                if (sj > m) {
                                    sj--;
                                }
                                if (i === m) {
                                    qx = 'm';
                                    qy = Math.abs(m - j);
                                } else if (j === m) {
                                    qx = 'm';
                                    qy = Math.abs(m - i);
                                } else {
                                    qx = sj % m;
                                    qy = si % m;
                                }
                            } else {
                                qx = j % m;
                                qy = i % m;
                            }
                            var name = [qx, qy].join("-");
                            tds.push("<td><input type='radio' name='" + name + "'" + ((is_odd && i === m && j === m) ? "disabled" : "checked") + " /></td>");
                        }
                        $(".key table").append("<tr>" + tds.join("") + "</tr>");
                    }
                } else {
                    var grille = _.map($(".key table input"), function(radio) {
                        return ($(radio).is(":checked")) ? 1 : 0;
                    });
                    $(".e1").text(ciphers.fleissner.encrypt(grille, 1, "Hello"));
                }
            }
        }, encrypt: function(grille, rotation, plaintext) {
            var space_at;
            var page = 0;
            var rotations = 0;
            var size = Math.ceil(plaintext.length / grille.length) * grille.length;
            var ciphertext = new Array(size);
            plaintext += _.map(new Array(size - plaintext.length), function(_) {
                return padding.to_letters(Math.floor(Math.random() * 100));
            }).join("");
            _.each(plaintext, function(c) {
                space_at = grille.indexOf(1, space_at + 1);
                if (space_at === -1) {
                    grille = ciphers.fleissner.rotate(grille, rotation);
                    space_at = grille.indexOf(1, space_at + 1);
                    rotations++;
                    if (rotations === 4) {
                        rotations = 0;
                        page++;
                    }
                }
                ciphertext[page * grille.length + space_at] = plaintext[0];
                plaintext = plaintext.slice(1);
            });
            return ciphertext.join("");
        }, decrypt: function(grille, rotation, ciphertext) {
            var plaintext = [];
            var size = ciphertext.length;
            var space_at;
            var page = 0;
            var rotations = 0;
            while (plaintext.length !== size) {
                space_at = grille.indexOf(1, space_at + 1);
                if (space_at === -1) {
                    grille = ciphers.fleissner.rotate(grille, rotation);
                    space_at = grille.indexOf(1, space_at + 1);
                    rotations++;
                    if (rotations === 4) {
                        rotations = 0;
                        page++;
                    }
                }
                plaintext.push(ciphertext[page * grille.length + space_at]);
            }
            return plaintext.join("");
        }, rotate: function(grille, direction) {
            var rotated = new Array(grille.length);
            var rowLength = Math.sqrt(grille.length);
            for (var i = 0; i < grille.length; i++) {
                //convert to x/y
                var x = i % rowLength;
                var y = Math.floor(i / rowLength);
                //find new x/y
                var newX, newY;
                if (direction === 1) {
                    newX = rowLength - y - 1;
                    newY = x;
                } else {
                    newY = rowLength - x - 1;
                    newX = y;
                }
                //convert back to index
                var newPosition = newY * rowLength + newX;
                rotated[newPosition] = grille[i];
            }
            return rotated;
        }, test: function() {
            var grille = [
                0,0,0,1,0,0,0,1,
                0,0,0,1,0,0,0,1,
                1,1,0,0,0,1,0,0,
                0,0,0,0,0,1,0,0,
                0,0,0,1,0,0,0,1,
                0,0,0,1,0,0,0,0,
                0,1,0,1,0,1,0,1,
                0,0,0,0,0,1,0,0];
            var from_wiki = "thefleissnergrillecanbeturnedtoeightdifferentpositionsstephenc&c";
            console.log("Fleissner tests pass: " + _.every([
                _.isEqual(ciphers.fleissner.rotate([1,2,3,4], 1), [3,1,4,2]),
                _.isEqual(ciphers.fleissner.rotate([1,2,3,4], -1), [2,4,1,3]),
                _.isEqual(ciphers.fleissner.rotate([1,2,3,4,5,6,7,8,9], 1), [7,4,1,8,5,2,9,6,3]),
                _.isEqual(ciphers.fleissner.rotate([1,2,3,4,5,6,7,8,9], -1), [3,6,9,2,5,8,1,4,7]),
                ciphers.fleissner.encrypt([1,0,0,0], 1, "abcd") === "abdc",
                ciphers.fleissner.encrypt([0,1,0,0], 1, "abcd") === "dacb",
                ciphers.fleissner.encrypt([0,1,0,0], -1, "abcd") === "bacd",
                ciphers.fleissner.encrypt([0,1,0,0], 1, "abcdefgh") === "dacbhegf",
                ciphers.fleissner.encrypt([0,1,0,0], 1, "abc").slice(1) === "acb",
                !_.isEqual(ciphers.fleissner.encrypt([0,1,0,0], 1, "abc"), ciphers.fleissner.encrypt([0,1,0,0], 1, "abc")),
                ciphers.fleissner.decrypt([1,0,0,0], 1, "abdc") === "abcd",
                ciphers.fleissner.decrypt([0,1,0,0], 1, "dacb") === "abcd",
                ciphers.fleissner.decrypt([0,1,0,0], -1, "bacd") === "abcd",
                ciphers.fleissner.decrypt([0,1,0,0], 1, "dacbhegf") === "abcdefgh",
                ciphers.fleissner.decrypt(grille, 1, "ititilohgehetcdflensiistfanbfsetepeshennurreneentrcgpr&iodctsloe") === from_wiki,
                ciphers.fleissner.decrypt(grille, -1, "leitciahgthetidflenbiietfonsfssturesnednepreheentrtgproionecsl&c") === from_wiki
            ]));
        }
    }
};
$(document).ready(function() {
    if ($("body.cipher").length) {
        $(".key").on("change input", "input", function() {
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
                ciphers[c].test();
                ciphers[c].init();
            }
        });
    }
});
