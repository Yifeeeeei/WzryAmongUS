console.log("trigger.js loaded");

var register_btn = document.getElementById("register");
var draw_btn = document.getElementById("draw");

var global_game_number = -1;
var query_show;

register_btn.addEventListener("click", register_game);
draw_btn.addEventListener("click", draw);

function get_request_url(url, datas) {
    var new_url = url + "?";
    for (var k in datas) {
        new_url = new_url + k + "=" + datas[k] + "&";
    }
    return new_url.slice(0, -1);
}

var tmp_cookie = "user_id=";

console.log("tmp_cookie: " + tmp_cookie);

function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + exdays * 24 * 60 * 60 * 1000);
    var expires = "expires=" + d.toGMTString();
    document.cookie = cname + "=" + cvalue + "; " + expires;
    // tmp_cookie = cname + "=" + cvalue + "; " + expires;
}

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(";");
    // var ca = tmp_cookie.split(";");
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i].trim();
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}
function set_user_id(new_user_id) {
    setCookie("user_id", new_user_id, 1);
}
function get_user_id() {
    let ui = getCookie("user_id");
    try {
        let ui_res = parseInt(ui);
        if (isNaN(ui_res)) {
            return -1;
        }
        return ui_res;
    } catch (e) {
        return -1;
    }
}

function register_game() {
    var game_number = parseInt(document.getElementById("game_number").value);
    console.log("game_number: " + game_number);
    if (isNaN(game_number) || game_number <= 0) {
        alert("Please input a positive game number");
        return;
    }
    var user_id = get_user_id();

    var httpRequest = new XMLHttpRequest(); //第一步：建立所需的对象
    httpRequest.open(
        "GET",
        get_request_url("/register", {
            game_number: game_number,
            user_id: user_id,
        }),
        true
    );
    httpRequest.send();

    httpRequest.onreadystatechange = function () {
        if (httpRequest.readyState == 4 && httpRequest.status == 200) {
            var json = httpRequest.responseText; //获取到json字符串，还需解析
            // console.log(json);
            var obj = JSON.parse(json);
            if (obj["status"] == "full") {
                set_user_id(parseInt(obj["user_id"]));
                alert("This room is full");
                return;
            } else if (obj["status" == "expired"]) {
                set_user_id(parseInt(obj["user_id"]));
                alert("This room is expired");
                return;
            } else if (obj["status"] == "success") {
                set_user_id(parseInt(obj["user_id"]));
                global_game_number = parseInt(obj["game_number"]);
                query_show = self.setInterval("show()", 1000);
                return;
            }
        }
    };
}
function draw() {
    var user_id = get_user_id();

    var httpRequest = new XMLHttpRequest(); //第一步：建立所需的对象
    httpRequest.open(
        "GET",
        get_request_url("/draw", {
            user_id: user_id,
        }),
        true
    );
    httpRequest.send();

    httpRequest.onreadystatechange = function () {
        if (httpRequest.readyState == 4 && httpRequest.status == 200) {
            var json = httpRequest.responseText; //获取到json字符串，还需解析
            // console.log(json);
            var obj = JSON.parse(json);
            if (obj["status"] == "success") {
            } else if (obj["status"] == "failed") {
                alert("register first");
            }
        }
    };
}
function show() {
    var user_id = get_user_id();

    var httpRequest = new XMLHttpRequest(); //第一步：建立所需的对象
    httpRequest.open(
        "GET",
        get_request_url("/show", {
            user_id: user_id,
        }),
        true
    );
    httpRequest.send();

    httpRequest.onreadystatechange = function () {
        if (httpRequest.readyState == 4 && httpRequest.status == 200) {
            var json = httpRequest.responseText; //获取到json字符串，还需解析
            // console.log(json);
            var obj = JSON.parse(json);
            if (obj["status"] == "failed") {
                var people_in_game = document.getElementById("people_in_game");
                people_in_game.innerText =
                    obj["people_in_game"].toString() + " / 5";

                return;
            } else if (obj["status"] == "expired") {
                alert("This room is expired");
                clearInterval(query_show);
                return;
            } else if (obj["status"] == "success") {
                var all_players =
                    document.getElementsByClassName("all_players");
                var people_in_game = document.getElementById("people_in_game");
                people_in_game.innerText =
                    obj["people_in_game"].toString() + " / 5";
                var identity = document.getElementById("identity");
                identity.innerHTML = obj["identity"];

                for (var i = 0; i < obj["players"].length; i++) {
                    if (obj["players"][i]["player_number"] == user_id) {
                        if (!all_players[i].classList.contains("chosen")) {
                            all_players[i].classList.add("chosen");
                        }
                    } else {
                        if (all_players[i].classList.contains("chosen")) {
                            all_players[i].classList.remove("chosen");
                        }
                    }
                    all_players[i].getElementsByClassName(
                        "all_hero"
                    )[0].innerText = obj["players"][i]["hero"];
                    all_players[i].getElementsByClassName(
                        "all_road"
                    )[0].innerText = obj["players"][i]["road"];
                }
            }
        }
    };
}
