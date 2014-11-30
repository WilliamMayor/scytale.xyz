var padding = {
    scheme: {
        " ": "00", "!": "01", "\"": "02", "#": "03", "$": "04", "%": "05", "&": "06", "'": "07", "(": "08", ")": "09",
        "*": "10", "+": "11", ",": "12", "-": "13", ".": "14", "/": "15", ":": "16", ";": "17", "<": "18", "=": "19",
        ">": "20", "?": "21", "@": "22", "[": "23", "\\": "24", "]": "25", "^": "26", "_": "27", "`": "28", "{": "29",
        "£": "30", "}": "31", "~": "32", "0": "33", "1": "34", "2": "35", "3": "36", "4": "37", "5": "38", "6": "39",
        "7": "40", "8": "41", "9": "42", "A": "43", "B": "44", "C": "45", "D": "46", "E": "47", "F": "48", "G": "49",
        "H": "50", "I": "51", "J": "52", "K": "53", "L": "54", "M": "55", "N": "56", "O": "57", "P": "58", "Q": "59",
        "R": "60", "S": "61", "T": "62", "U": "63", "V": "64", "W": "65", "X": "66", "Y": "67", "Z": "68", "a": "69",
        "b": "70", "c": "71", "d": "72", "e": "73", "f": "74", "g": "75", "h": "76", "i": "77", "j": "78", "k": "79",
        "l": "80", "m": "81", "n": "82", "o": "83", "p": "84", "q": "85", "r": "86", "s": "87", "t": "88", "u": "89",
        "v": "90", "w": "91", "x": "92", "y": "93", "z": "94", "ϕ": "95", "ϴ": "96", "Ω": "97", "β": "98", "ε": "99"
    },
    to_numbers: function(letters) {
        return _.map(letters, function(l) {
            return padding.scheme[l];
        }).join("");
    },
    to_letters: function(numbers) {
        if ($.isNumeric(numbers)) {
            numbers = "" + numbers;
        }
        if (numbers.length % 2 !== 0) {
            numbers = "0" + numbers;
        }
        numbers = numbers.match(/(..?)/g);
        return _.map(numbers, function(n) {
            return padding.reverse_scheme[n];
        }).join("");
    }
};
padding.reverse_scheme = _.invert(padding.scheme);
$(document).ready(function() {
    if ($("body.padding").length) {
        $("#letters").on("change input", function() {
            $("#letters-output").text(padding.to_numbers($(this).val()));
        });
        $("#numbers").on("change input", function() {
            $("#numbers-output").text(padding.to_letters($(this).val()));
        });

        $("#letters").val("Hello!").change();
        $("#numbers").val(padding.to_numbers("Hello!")).change();
    }
});
