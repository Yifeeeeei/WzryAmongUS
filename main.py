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

    def update_time(self):
        self.last_operate_time = time.time()

    def add_player(self, user_id):
        self.update_time()
        if len(self.player_list) == 5:
            return False

        self.player_list.append(Player(user_id))
        return True

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
            print("draw_success!!!")

            self.ready = True

    def get_player(self, user_id):
        for player in self.player_list:
            if player.number == user_id:
                return player


class RegistrationTable:
    def __init__(self):
        self.table = dict()

    def invalid_user_id(self, user_id):
        if user_id < 0:
            return True
        else:
            return False

    def register(self, user_id):
        if user_id not in self.table.keys() or self.invalid_user_id(user_id):
            new_user_id = random.randint(10000000, 99999999)
            while new_user_id in self.table.keys():
                new_user_id = random.randint(10000000, 99999999)
            self.table[new_user_id] = -1
            return new_user_id

        else:
            return user_id

    def mark(self, user_id, game_number):
        if user_id in self.table.keys():
            self.table[user_id] = game_number
            return True
        else:
            return False

    def get(self, user_id):
        if user_id in self.table.keys():
            return self.table[user_id]
        else:
            return None


class GameList:
    def __init__(self):
        self.game_list = []

    def add_game(self, new_game: Game):
        self.game_list.append(new_game)

    def has_game(self, game_number):
        for game in self.game_list:
            if game.game_number == game_number:
                return True
        return False

    def fit_into_room(self, user_id, game_number):
        for i in range(len(self.game_list)):
            if self.game_list[i].game_number == game_number:
                # existed room
                if not self.game_list[i].add_player(user_id):
                    # add failed, room full
                    return False
                else:
                    # add success
                    return True

        new_game = Game(game_number)
        new_game.add_player(user_id)
        self.game_list.append(new_game)
        return True

    def draw(self, game_number):

        for i in range(len(self.game_list)):
            if self.game_list[i].game_number == game_number:
                self.game_list[i].draw()
                return True
        return False

    def get_players(self, game_number):
        for i in range(len(self.game_list)):
            if self.game_list[i].game_number == game_number:
                if self.game_list[i].ready:
                    return self.game_list[i].player_list
                break
        return len(self.game_list[i].player_list)


app = Flask(__name__)
app.config["SCHEDULER_API_ENABLED"] = True

# scheduler = APScheduler()
# scheduler.init_app(app)


hero_data = parse_all_heros.get_hero_data()
registration_table = RegistrationTable()
game_list = GameList()


@app.route("/")
def wzry():
    return render_template("index.html")


"""
in: 'user_id':int, 'game_number':int
out: dict()
    status: success or expired or full
    if suceess: 
        game_number: int
        user_id:int
    if expired:
        user_id:int
    if full:
        user_id:int
            
"""


@app.route("/register")
def register():
    user_id = int(request.args.get("user_id"))
    game_number = int(request.args.get("game_number"))

    user_id = registration_table.register(user_id)

    if game_number == registration_table.get(user_id):
        # get his old room
        if game_list.has_game(game_number):
            return_dict = dict()
            return_dict["status"] = "success"
            return_dict["game_number"] = game_number
            return_dict["user_id"] = user_id
            return json.dumps(return_dict)

    # try to get the target_room
    fit_result = game_list.fit_into_room(user_id, game_number)
    if not fit_result:
        return_dict = dict()
        return_dict["status"] = "full"
        return_dict["user_id"] = user_id
        return json.dumps(return_dict)
    # successfully fit into room
    return_dict = dict()
    return_dict["status"] = "success"
    return_dict["game_number"] = game_number
    return_dict["user_id"] = user_id
    # register to registration table
    registration_table.mark(user_id, game_number)
    return json.dumps(return_dict)


"""
in: 'user_id':int
out: 'status': 'success' or 'failed'
"""


@app.route("/draw")
def draw():
    user_id = int(request.args.get("user_id"))
    game_number = registration_table.get(user_id)

    draw_result = game_list.draw(game_number)
    if not draw_result:
        # draw failed
        return_dict = dict()
        return_dict["status"] = "failed"
        return json.dumps(return_dict)
    # draw success
    return_dict = dict()
    return_dict["status"] = "success"
    return json.dumps(return_dict)


"""
in: 'user_id':int
out: 'status': 'success' or 'failed' or 'expired'
    'people_in_game': int
    if success:
        'identity': str,
        'players': list of dict:
            "player_number": int,
            "hero": str,
            "road": str

"""


@app.route("/show")
def show():
    user_id = int(request.args.get("user_id"))
    game_number = registration_table.get(user_id)
    if game_number is None:
        return_dict = dict()
        return_dict["status"] = "expired"
        return json.dumps(return_dict)

    player_list = game_list.get_players(game_number)
    if type(player_list) is int:
        return_dict = dict()
        return_dict["status"] = "failed"
        return_dict["people_in_game"] = player_list
        return json.dumps(return_dict)
    return_dict = dict()
    return_dict["status"] = "success"
    return_dict["players"] = []
    return_dict["people_in_game"] = len(player_list)
    for player in player_list:
        if player.number == user_id:
            return_dict["identity"] = player.identity
            return_dict["players"].append(
                {
                    "player_number": player.number,
                    "hero": player.hero,
                    "road": player.road,
                }
            )
        else:
            return_dict["players"].append(
                {
                    "player_number": -1,
                    "hero": player.hero,
                    "road": player.road,
                }
            )
    return json.dumps(return_dict)


app.run(host="0.0.0.0", port=80, debug=True)
