from flask import Flask, render_template, request
import joblib
import random
import json

from flask_apscheduler import APScheduler
import time

# try:
#     hero_data = joblib.load("hero_data.pkl")
# except:
import parse_all_heros

hero_data = parse_all_heros.get_hero_data()

registration_table = []


class RegistrationEntry:
    def __init__(self):
        self.game_number = -2
        self.player_number = -2


# hero_data = joblib.load("hero_data.pkl")


class Player:
    def __init__(self, number):
        self.number = number
        self.hero = None
        self.road = None
        self.identity = None


class Game:
    def __init__(self, game_number):
        self.last_operate_time = time.time()
        self.game_number = game_number
        # self.all_heros = joblib.load("names.pkl")
        self.player_list = []
        self.ready = False
        self.all_roads = ["上路", "中路", "下路", "打野", "游走"]
        self.all_identities = ["良民", "良民", "良民", "呆呆鸟", "卧底"]
        self.mapping = dict()

    def update_time(self):
        self.last_operate_time = time.time()

    def add_player(self):
        self.update_time()
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
        self.update_time()
        if len(self.player_list) != 5:
            self.ready = False
        else:
            random.shuffle(self.all_roads)
            random.shuffle(self.all_identities)
            chosen_heros = []
            for i in range(5):
                self.player_list[i].road = self.all_roads[i]
                self.player_list[i].identity = self.all_identities[i]
                random_hero = random.sample(hero_data[self.all_roads[i]], 1)[0]
                while random_hero in chosen_heros:
                    random_hero = random.sample(hero_data[self.all_roads[i]], 1)[0]
                chosen_heros.append(random_hero)
                self.player_list[i].hero = random_hero

            self.ready = True

    def get_player(self, player_number):
        print(self.mapping.keys())
        if str(player_number) not in self.mapping.keys():
            return None
        return self.player_list[self.mapping[str(player_number)]]


app = Flask(__name__)
app.config["SCHEDULER_API_ENABLED"] = True

scheduler = APScheduler()
scheduler.init_app(app)
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
    user_id = str(request.args.get("user_id"))
    if user_id == "" or int(user_id) >= len(registration_table):
        # create_new_user_id
        user_id = str(len(registration_table))
        re = RegistrationEntry()
        registration_table.append(re)
        return_dic["user_id"] = user_id
    else:
        # if it matches
        if registration_table[int(user_id)].game_number == game_number:
            return_dic["game_number"] = game_number

            pn = registration_table[int(user_id)].player_number
            if pn == -2:
                return_dic["status"] = "failed"
                return_dic["player_number"] = pn
                return_dic["user_id"] = user_id
                return return_dic

            return_dic["player_number"] = pn
            return_dic["user_id"] = user_id
            return return_dic

    player_number = 0
    for i in range(len(game_list)):
        if game_list[i].game_number == game_number:
            print("existed")
            player_number = game_list[i].add_player()
            print(player_number)
            if player_number == -1:
                return_dic["status"] = "failed"
            return_dic["player_number"] = player_number
            return_dic["user_id"] = user_id

            return json.dumps(return_dic)
    print("new one")
    new_game = Game(game_number)
    game_list.append(new_game)
    player_number = new_game.add_player()
    return_dic["status"] = "success"
    return_dic["game_number"] = game_number
    return_dic["player_number"] = player_number
    return_dic["user_id"] = user_id

    registration_table[int(user_id)].game_number = game_number
    registration_table[int(user_id)].player_number = player_number
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
    if real_game_number == -1:
        return_dict["status"] = "failed"
        return json.dumps(return_dict)

    if len(game_list[real_game_number].player_list) != 5:
        return_dict["status"] = "missing_people"
        # return_dict["people_in_game"] = len(game_list[real_game_number].player_list)
        return json.dumps(return_dict)
    game_list[real_game_number].draw()

    player_number = int(request.args.get("player_number"))
    real_game_number = -1
    for i in range(len(game_list)):
        if game_list[i].game_number == game_number:
            real_game_number = i
            break
    tmp_player = game_list[real_game_number].get_player(player_number)
    if tmp_player is None:
        return_dict["status"] = "failed"
        return json.dumps(return_dict)

    return_dic = {
        "identity": tmp_player.identity,
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
    if real_game_number == -1:
        return_dic = {
            "status": "failed",
            # "identity": game_list[real_game_number].get_player(player_number).identity,
            # "players": [],
            # "people_in_game": len(game_list[real_game_number].player_list),
        }
        return return_dic
    tmp_player = game_list[real_game_number].get_player(player_number)
    return_dict = {}
    if tmp_player is None:
        return_dict["status"] = "failed"
        return json.dumps(return_dict)

    return_dic = {
        "status": "success",
        "identity": tmp_player.identity,
        "players": [],
        "people_in_game": len(game_list[real_game_number].player_list),
    }
    if return_dic["people_in_game"] != 5:
        return json.dumps(return_dic)

    game_list[real_game_number].update_time()

    for player in game_list[real_game_number].player_list:
        if player.number == player_number:
            return_dic["players"].append(
                {
                    "player_number": player.number,
                    "hero": player.hero,
                    "road": player.road,
                }
            )
        else:
            return_dic["players"].append(
                {"player_number": -1, "hero": player.hero, "road": player.road}
            )

    return json.dumps(return_dic)


def maintain_game_list():
    print("maintain")
    games_to_be_deleted = []
    for i in range(len(game_list)):
        if time.time() - game_list[i].last_operate_time > 60 * 30:
            games_to_be_deleted.append(i)
    games_to_be_deleted.reverse()
    for i in games_to_be_deleted:
        print("deleting")
        game_list.pop(i)


@scheduler.task("cron", id="maintain", minute=59)
def cron_maintain():
    print("croning")
    maintain_game_list()


scheduler.start()

app.run(host="0.0.0.0", port=80, debug=True)
# scheduler = BlockingScheduler()
# scheduler.add_job(maintain_game_list, "interval", seconds=1)
