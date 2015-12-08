// http://md5online.net/
// HINT   |  Only query2[8] has more than one character.
document.getElementById("panel").onclick = function() {
    document.getElementById("message").innerHTML = "Checking...";
    setTimeout(function() {
        try {
            if (location.search.length != 25) throw Error();
            var query = location.search.substring(1).split(/{|}/);
            if (query[0] != "flag") throw Error();
            // flag format: flag{xxxxxxxxxxxxxxxxxx}
            if (query[2]) throw Error();
            var message = ("The " + query[0] + " is a string.").split(" ");
            var query2 = query[1].split("$");
            if (query2[8].split("").map(function(k) {
                    return k.charCodeAt(0);
                }).reduce(function(y, n) {
                    return y + Math.pow(n ^ 95, 4);
                }) != 0x2f7b81) throw Error();
            for (var i in message) {
                if (i != false) {
                    var q = message.splice(i, 1).join("");
                    var h = CryptoJS.MD5(message.splice(i + 1).join("") + message.join("%"));
                    var z = h.toString() + h.words.splice(0, 1);
                    break;
                }
            }
            var funcs = [String.fromCharCode, Object.getOwnPropertyNames, function(x) {
                return (x == query2[2]) ? 0b11 : x;
            }, function(c) {
                return [query2[4], 0x9c, 0xe6, ~~(query2[6].charCodeAt(0) * 2)].reduce(c);
            }];
            var m = new MersenneTwister((funcs[0] + "" [~~(query2[0] / 21)]).split(/\s/).join("").split("").map(function(x) {
                return x.charCodeAt(0);
            }).reduce(function(a, b) {
                return a + b;
            }) + 0xa0);
            var string = [(function(n) {
                return n.split("").map(funcs[query2[5].charCodeAt(0) ^ 66]).join("") + n.charAt(query2[6].charCodeAt(0) - query2[7].charCodeAt(0));
            })(funcs[1](Array.prototype).sort()[query2[1].charCodeAt(0) - 0x65].substring(0, 6)), funcs[query2[8].charCodeAt(1) - 0x72](function(m, n) {
                return m + (funcs[0](n ^ h.words.splice(0, 1) & 0xff));
            }), [181, 78, 28, query2[0].charCodeAt(0), 225, 129].map(function(x) {
                return funcs[0](((m.genrand_int32() * Math.sqrt(m.random())) & 0xff) ^ x);
            }).join("")].join(funcs[0](query2[3].charCodeAt(0) + 0xF));
            if (CryptoJS.MD5(string).toString() == "0f957300a52431c2d0de0da9fc7223c9") {
                document.getElementById("message").innerHTML = "Correct!";
            } else {
                throw Error();
            }
        } catch (e) {
            document.getElementById("message").innerHTML = "Nope. :(";
        }
    }, 1000);
};
