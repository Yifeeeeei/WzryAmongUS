// var game_number = document.getElementById("game_number");
// var player_number = document.getElementById("player_number");
// var identity = document.getElementById("identity");

// var road = document.getElementById("road");
// var hero = document.getElementById("hero");
// var all_players = document.getElementsByClassName("all_players");

// var base_url = "https://wzryamongus.yifeeeeei.repl.co/";
console.log("trigger.js loaded");

// var register = document.getElementById("register");
// var draw = document.getElementById("draw");
// var show = document.getElementById("show");

// register.addEventListener("click", register_game);
// draw.addEventListener("click", draw);
// show.addEventListener("click", show);

// merge data for get request into the url
function get_request_url(url, datas) {
    var new_url = url + "?";
    for (var k in datas) {
        new_url = new_url + k + "=" + datas[k] + "&";
    }
    return new_url.slice(0, -1);
}

function register_game() {
    var game_number = document.getElementById("game_number");
    var player_number = document.getElementById("player_number");
    var identity = document.getElementById("identity");

    var road = document.getElementById("road");
    var hero = document.getElementById("hero");
    var all_players = document.getElementsByClassName("all_players");

    var base_url = "https://wzryamongus.yifeeeeei.repl.co/";

    console.log("registering");
    var game_number_val = game_number.value;
    var httpRequest = new XMLHttpRequest(); //第一步：建立所需的对象
    httpRequest.open(
        "GET",
        get_request_url("/register", { game_number: game_number_val }),
        true
    ); //第二步：打开连接  将请求参数写在url中  ps:"http://localhost:8080/rest/xxx"
    httpRequest.send(); //第三步：发送请求  将请求参数写在URL中
    /**
     * 获取数据后的处理程序
     */
    httpRequest.onreadystatechange = function () {
        if (httpRequest.readyState == 4 && httpRequest.status == 200) {
            var json = httpRequest.responseText; //获取到json字符串，还需解析
            console.log(json);
            var obj = JSON.parse(json);
            if (obj["status"] == "success") {
                player_number.innerText = obj["player_number"];
            } else {
                alert("room full");
            }
        }
    };
}

function draw() {
    var game_number = document.getElementById("game_number");
    var player_number = document.getElementById("player_number");
    var identity = document.getElementById("identity");

    var road = document.getElementById("road");
    var hero = document.getElementById("hero");
    var all_players = document.getElementsByClassName("all_players");

    var base_url = "https://wzryamongus.yifeeeeei.repl.co/";

    console.log("drawing");
    var game_number_val = parseInt(game_number.value);
    var player_number_val = parseInt(player_number.innerText);
    var httpRequest = new XMLHttpRequest(); //第一步：建立所需的对象
    httpRequest.open(
        "GET",
        get_request_url("/draw", {
            game_number: game_number_val,
            player_number: player_number_val,
        }),
        true
    ); //第二步：打开连接  将请求参数写在url中  ps:"http://localhost:8080/rest/xxx"
    httpRequest.send(); //第三步：发送请求  将请求参数写在URL中
    /**
     * 获取数据后的处理程序
     */
    httpRequest.onreadystatechange = function () {
        if (httpRequest.readyState == 4 && httpRequest.status == 200) {
            // var json = httpRequest.responseText;//获取到json字符串，还需解析
            show();
        }
    };
}
function show() {
    var game_number = document.getElementById("game_number");
    var player_number = document.getElementById("player_number");
    var identity = document.getElementById("identity");

    var road = document.getElementById("road");
    var hero = document.getElementById("hero");
    var all_players = document.getElementsByClassName("all_players");

    var base_url = "https://wzryamongus.yifeeeeei.repl.co/";

    console.log("showing");
    var game_number_val = parseInt(game_number.value);
    var player_number_val = parseInt(player_number.innerText);
    var httpRequest = new XMLHttpRequest(); //第一步：建立所需的对象
    httpRequest.open(
        "GET",
        get_request_url("/show", {
            game_number: game_number_val,
            player_number: player_number_val,
        }),
        true
    ); //第二步：打开连接  将请求参数写在url中  ps:"http://localhost:8080/rest/xxx"
    httpRequest.send(); //第三步：发送请求  将请求参数写在URL中
    /**
     * 获取数据后的处理程序
     */
    httpRequest.onreadystatechange = function () {
        if (httpRequest.readyState == 4 && httpRequest.status == 200) {
            var json = httpRequest.responseText; //获取到json字符串，还需解析
            console.log(json);
            var obj = JSON.parse(json);
            if (obj["identity"] == null) {
                alert("not ready yet");
                return;
            }

            identity.innerHTML = obj["identity"];

            for (var i = 0; i < obj["players"].length; i++) {
                all_players[i].getElementsByClassName(
                    "all_player_number"
                )[0].innerText = obj["players"][i]["player_number"];
                all_players[i].getElementsByClassName("all_hero")[0].innerText =
                    obj["players"][i]["hero"];
                all_players[i].getElementsByClassName("all_road")[0].innerText =
                    obj["players"][i]["road"];
            }
        }
    };
}
