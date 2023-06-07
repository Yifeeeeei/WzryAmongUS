from flask import Flask, render_template, request
import joblib
import random
import json


class Player:
    def __init__(self, number):
        self.number = number
        self.hero = None
        self.road = None
        self.identity = None


class Game:
    def __init__(self, game_number):
        self.game_number = game_number
        self.all_heros = joblib.load("names.pkl")
        self.player_list = []
        self.ready = False
        self.all_roads = ["top", "mid", "bot", "jug", "sup"]
        self.all_identities = ["man", "man", "man", "man", "ghost"]
        self.mapping = dict()

    def add_player(self):
        if len(self.player_list) == 5:
            return -1
        player_number = random.randint(0, 10000)
        while player_number in self.mapping.keys():
            player_number = random.randint(0, 10000)
        self.player_list.append(Player(player_number))
        self.mapping[str(player_number)] = len(self.player_list) - 1
        print(self.mapping.keys())
        return player_number

    def draw(self):
        if len(self.player_list) != 5:
            self.ready = False
        else:
            random.shuffle(self.all_roads)
            tmp_heros = random.sample(self.all_heros, 5)
            random.shuffle(self.all_identities)
            for i in range(5):
                self.player_list[i].hero = tmp_heros[i]
                self.player_list[i].road = self.all_roads[i]
                self.player_list[i].identity = self.all_identities[i]
            self.ready = True

    def get_player(self, player_number):
        print(self.mapping.keys())
        return self.player_list[self.mapping[str(player_number)]]


app = Flask(__name__)

game_list = []


@app.route("/")
def wzry():
    return render_template("index.html")


# @app.route("/register_game")
# def register_game():
#     game_number = int(request.args.get("game_number"))

#     for g in game_list:
#         if g.game_number == game_number:
#             return game.game_number
#     game = Game(game_number)
#     game_list.append(game)
#     return game.game_number


# @app.route("/register_player")
# def register_player():
#     game_number = int(request.args.get("game_number"))
#     try:
#         player_num = game_list[game_number].add_player()
#         return player_num
#     except:
#         return "failed"


@app.route("/register")
def register():
    return_dic = {"status": "success", "game_number": 0, "player_number": 0}
    game_number = int(request.args.get("game_number"))
    player_number = 0
    for i in range(len(game_list)):
        if game_list[i].game_number == game_number:
            print("existed")
            player_number = game_list[i].add_player()
            print(player_number)
            if player_number == -1:
                return_dic["status"] = "failed"
            return_dic["player_number"] = player_number
            return json.dumps(return_dic)
    print("new one")
    new_game = Game(game_number)
    game_list.append(new_game)
    player_number = new_game.add_player()
    return_dic["status"] = "success"
    return_dic["game_number"] = game_number
    return_dic["player_number"] = player_number
    return json.dumps(return_dic)


@app.route("/draw")
def draw():
    game_number = int(request.args.get("game_number"))
    return_dict = {"status": "failed"}

    real_game_number = -1
    for i in range(len(game_list)):
        if game_list[i].game_number == game_number:
            real_game_number = i
            break
    if len(game_list[real_game_number].player_list) != 5:
        return json.dumps(return_dict)
    game_list[real_game_number].draw()

    player_number = int(request.args.get("player_number"))
    real_game_number = -1
    for i in range(len(game_list)):
        if game_list[i].game_number == game_number:
            real_game_number = i
            break

    return_dic = {
        "identity": game_list[real_game_number].get_player(player_number).identity,
        "players": [],
    }

    for player in game_list[real_game_number].player_list:
        return_dic["players"].append(
            {"player_number": player.number, "hero": player.hero, "road": player.road}
        )
    return json.dumps(return_dic)


@app.route("/show")
def show():
    game_number = int(request.args.get("game_number"))
    player_number = int(request.args.get("player_number"))
    real_game_number = -1
    for i in range(len(game_list)):
        if game_list[i].game_number == game_number:
            real_game_number = i
            break

    return_dic = {
        "identity": game_list[real_game_number].get_player(player_number).identity,
        "players": [],
    }

    for player in game_list[real_game_number].player_list:
        return_dic["players"].append(
            {"player_number": player.number, "hero": player.hero, "road": player.road}
        )
    return json.dumps(return_dic)


app.run(host="0.0.0.0", port=80, debug=True)
