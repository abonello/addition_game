import os
from flask import Flask, render_template

app = Flask(__name__)

class User:
    
    logged_users = 0
    
    def __init__(self, username, password, number):
        self.username = username
        self.password = password
        self.is_logged = True
        self.number = number
        self.total_points = 0
        self.points_this_game = 0
        self.games_list = []
        
        User.logged_users += 1
        
    def reference(self):
        return "{}.{}".format(self.username, self.password)

class Game:
    
    def __init__(self):
        self.numbers = [3, 6, 2, 7, 1, 4, 2, 8, 0, -5, 3, 4]
        self.index = 0
    

# user1 = User()
# user1.username = "FirstUser"

# user2 = User()
# user2.username = "SecondUser"

user1 = User("UserFirst", "asdf", 32)
user2 = User("UserSecond", "qwerty", 87)
user1_game = Game()

@app.route("/")
def home():
    # print("Username is: {0}".format(user1.username))
    # print("password for {0} is: {1}".format(user1.username, user1.password))
    # print("number {0}").format(user1.number)
    # print("Username is: {0}".format(user2.username))
    # print("password for {0} is: {1}".format(user2.username, user2.password))
    # print("number {0}").format(user2.number)
    # print("Username is: {0}".format(user2.username))
    print("Reference for {} is: {}".format(user1.username, user1.reference()))
    # return "<h1>Addition Game</h1>"
    # return render_template("home.html", user1 = user1.username, user2 = user2.username)
    game_numbers = [user1_game.numbers[user1_game.index], user1_game.numbers[user1_game.index + 1]]
    user1_game.index += 2
    
    return render_template("home.html", user = User, user1 = user1, user2 = user2, info = 0, numbers = game_numbers)

@app.route("/game", methods=['GET', 'POST'])
def game():
    return "Answer was submitted"

if __name__ == '__main__':
    app.run(host=os.getenv('IP'), port=int(os.getenv('PORT', 8080)), debug=True)