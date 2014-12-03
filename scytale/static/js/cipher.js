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
    }, mixed: {
        init: function() {
            var mappings = _.map(padding.scheme, function(value, key) {
                value = ciphers.mixed.escape(padding.to_letters((parseInt(value) + 10) % 100));
                return "<td class='map-" + key + "'>" + key + "</td><td class='map-" + key + "'><input data-plain='" + key + "' type='text' value='" + value + "' /></td>";
            });
            var t = $(".key table");
            var tr = "<tr>";
            _.each(mappings, function(pair, i) {
                if (i > 0 && i % 6 === 0) {
                    tr += "</tr>";
                    t.append($(tr));
                    tr = "<tr>";
                }
                tr += pair;
            });
            tr += "</tr>";
            t.append($(tr));
            ciphers.mixed.update();
        }, escape: function(c) {
            var entityMap = {
                "&": "&amp;",
                "<": "&lt;",
                ">": "&gt;",
                '"': '&quot;',
                "'": '&#39;',
                "/": '&#x2F;'
            };
            return String(c).replace(/[&<>"'\/]/g, function (s) {
                return entityMap[s];
            });
        }, update: function() {
            var key = {};
            _.each($(".key table input"), function(input) {
                input = $(input);
                var cipher = input.val();
                var plain = input.data("plain");
                if (!cipher || _.values(key).indexOf(cipher) !== -1) {
                    input.addClass("error");
                    input.val("");
                } else {
                    key[plain] = cipher;
                    input.removeClass("error");
                }
            });
            var all = _.keys(padding.scheme);
            var values = _.values(key);
            var missing = _.filter(all, function(c) {
                return (values.indexOf(c) === -1);
            });
            $(".key .missing span").text(missing.join(""));
            $(".e1").text(ciphers.mixed.encrypt(key, "Hello"));
        }, encrypt: function(key, plain) {
            return _.map(plain, function(letter) {
                return key[letter];
            }).join("");
        }, decrypt: function(key, cipher) {
            key = _.invert(key);
            return _.map(cipher, function(letter) {
                return key[letter];
            }).join("");
        }, test: function() {
            var key = {};
            _.each(padding.scheme, function(v, k) {
                v = padding.to_letters((parseInt(v) + 1) % 100);
                key[k] = v;
            });
            console.log("Mixed alphabet tests pass: " + _.every([
                "Hello" === ciphers.mixed.decrypt(key, ciphers.mixed.encrypt(key, "Hello"))
            ]));
        }
    }, pigpen: {
        init: function() {
            ciphers.pigpen.update();
        }, update: function() {
            var key = {};
            _.each($(".key table input"), function(input) {
                input = $(input);
                var plain = input.val();
                var cipher = input.data("cipher");
                if (!plain || _.keys(key).indexOf(plain) !== -1) {
                    input.addClass("error");
                    input.val("");
                } else {
                    key[plain] = cipher;
                    input.removeClass("error");
                }
            });
            var all = " ABCDEFGHIJKLMNOPQRSTUVWXYZ";
            var values = _.keys(key);
            var missing = _.filter(all, function(c) {
                return (values.indexOf(c) === -1);
            });
            $(".key .missing span").text(missing.join(""));
            $(".e1").text(ciphers.mixed.encrypt(key, "HELLO"));
        }, encrypt: function(key, plain) {
            return ciphers.mixed.encrypt(key, plain);
        }, decrypt: function(key, cipher) {
            return ciphers.mixed.decrypt(key, cipher);
        }, test: function() {

        }
    }, playfair: {
        init: function() {
            ciphers.playfair.update();
        }, update: function() {
            var key = [];
            _.each($(".key table input"), function(input) {
                input = $(input);
                var value = input.val();
                if (!value) {
                    input.addClass("error");
                } else {
                    input.removeClass("error");
                    key.push(value);
                }
            });
            var all = "ABCDEFGHIJKLMNOPRSTUVWXYZ";
            var missing = _.filter(all, function(c) {
                return (key.indexOf(c) === -1);
            });
            $(".key .missing span").text(missing.join(""));
            $(".e1").text(ciphers.playfair.encrypt(key, "HELLO"));
            $(".e2").text(ciphers.playfair.decrypt(key, ciphers.playfair.encrypt(key, "HELLO")));
        }, encrypt: function(key, plain) {
            var cipher = [];
            for (var i = 0; i < plain.length; i+=2) {
                var first = plain[i];
                var second;
                if (i+1 === plain.length) {
                    second = 'X';
                } else {
                    second = plain[i+1];
                }
                if (first === second) {
                    second = 'X';
                    i--;
                }
                var first_i = key.indexOf(first);
                var first_x = first_i % 5;
                var first_y = Math.floor(first_i / 5);
                var second_i = key.indexOf(second);
                var second_x = second_i % 5;
                var second_y = Math.floor(second_i / 5);
                if (first_x === second_x) {
                    first_y = (first_y + 1) % 5;
                    second_y = (second_y + 1) % 5;
                } else if (first_y === second_y) {
                    first_x = (first_x + 1) % 5;
                    second_x = (second_x + 1) % 5;
                } else {
                    var temp_x = first_x;
                    first_x = second_x;
                    second_x = temp_x;
                }
                cipher.push(key[first_y * 5 + first_x]);
                cipher.push(key[second_y * 5 + second_x]);
            }
            return cipher.join("");
        }, decrypt: function(key, cipher) {
            var plain = [];
            for (var i = 0; i < cipher.length; i+=2) {
                var first = cipher[i];
                var second = cipher[i+1];
                var first_i = key.indexOf(first);
                var first_x = first_i % 5;
                var first_y = Math.floor(first_i / 5);
                var second_i = key.indexOf(second);
                var second_x = second_i % 5;
                var second_y = Math.floor(second_i / 5);
                if (first_x === second_x) {
                    first_y = (first_y + 4) % 5;
                    second_y = (second_y + 4) % 5;
                } else if (first_y === second_y) {
                    first_x = (first_x + 4) % 5;
                    second_x = (second_x + 4) % 5;
                } else {
                    var temp_x = first_x;
                    first_x = second_x;
                    second_x = temp_x;
                }
                plain.push(key[first_y * 5 + first_x]);
                plain.push(key[second_y * 5 + second_x]);
            }
            return plain.join("");
        }, test: function() {
            var key = "WELCOMTVIRSPAKBDFGHNJUXYZ";
            var key2 = [];
            _.each($(".key table input"), function(input) {
                input = $(input);
                var value = input.val();
                if (!value) {
                    input.addClass("error");
                } else {
                    input.removeClass("error");
                    key2.push(value);
                }
            });
            console.log("Playfair tests pass: " + _.every([
                "GLGL" === ciphers.playfair.encrypt(key, "AA"),
                "AUAU" === ciphers.playfair.encrypt(key, "PP"),
                "OJ" === ciphers.playfair.encrypt(key, "WZ"),
                "FU" === ciphers.playfair.encrypt(key, "PF"),
                "AK" === ciphers.playfair.encrypt(key, "PA"),
                "UE" === ciphers.playfair.encrypt(key, "FU"),
                "ND" === ciphers.playfair.encrypt(key, "HN"),
                "GU" === ciphers.playfair.encrypt(key, "F"),
                "FCVLCW" === ciphers.playfair.encrypt(key, "HELLO"),
                "AXAX" === ciphers.playfair.decrypt(key, ciphers.playfair.encrypt(key, "AA")),
                "PXPX" === ciphers.playfair.decrypt(key, ciphers.playfair.encrypt(key, "PP")),
                "WZ" === ciphers.playfair.decrypt(key, ciphers.playfair.encrypt(key, "WZ")),
                "PF" === ciphers.playfair.decrypt(key, ciphers.playfair.encrypt(key, "PF")),
                "PA" === ciphers.playfair.decrypt(key, ciphers.playfair.encrypt(key, "PA")),
                "FU" === ciphers.playfair.decrypt(key, ciphers.playfair.encrypt(key, "FU")),
                "HN" === ciphers.playfair.decrypt(key, ciphers.playfair.encrypt(key, "HN")),
                "FX" === ciphers.playfair.decrypt(key, ciphers.playfair.encrypt(key, "F")),
                "HELXLO" === ciphers.playfair.decrypt(key, ciphers.playfair.encrypt(key, "HELLO"))
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
