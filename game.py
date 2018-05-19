import os
import copy
import random
import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
loggedUsers = {}

class User:
    logged_users = 0
    
    def __init__(self, username, password, is_logged, session, total_points, games_played):
        self.username = username
        self.password = password
        self.is_logged = is_logged
        self.total_points = total_points
        self.points_this_game = 0
        self.games_played = games_played
        self.game = ""
        self.session = session
        
        User.logged_users += 1
        
        def addLoggedUser(self):
            global loggedUsers
            loggedUsers[self.username] = self
            
        def setSession(self):
            sess=0
            while True:
                # sess = random.randint(1,10)
                # print("sess: {}".format(sess))
                sess = 1
                if sess != session:
                    break
            self.session = sess
        
        setSession(self)
        addLoggedUser(self)

class Game:
    def __init__(self):
        self.numbers = self.generateNumbers()
        self.index = 0
        
    def generateNumbers(self):
        nums = []
        for i in range(10):
            x=[random.randint(-10, 10), random.randint(-10, 10)]
            nums.append(x)
        return nums

defaultUser = User("Please type a username to log in or register", "", False, 100, 0, [])

def read_from_file(file_name):
    store=""
    file = "data/" + file_name
    with open(file, "r") as readdata:
        store = readdata.read()
    return store

def createUser(name):
    tempUser = User(name, "asdf", True, 100, 0, [])
    vars()[name] = copy.deepcopy(tempUser)
    loggedUsers[name] = copy.deepcopy(tempUser)
    return vars()[name]

@app.route("/")
def home():
    # allusers = read_from_file("users.txt")
    allusers = json.loads(read_from_file("users.json"))
    
    
    ''' For Testing only '''
    for username in dict(allusers):
        print(allusers[username]['username'])
        print(allusers[username]['password'])
    
    ''' End testing '''
    
    
    
    thisUser=defaultUser
    return render_template("home.html", thisUser=thisUser)
    
@app.route('/prepare_register', methods=['GET','POST'])
def prepare_register():
    print("reached prepare_register route")
    if request.method == 'POST':
        buttons={}
        buttons['register_active'] ="btn-deactivated btn-hide"
        buttons["check_active"] = ""
        return render_template("register.html", buttons=buttons, thisUser="" )

@app.route('/register', methods=['GET','POST'])
def register():
    print("Reached register route")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # allusers = read_from_file("users.txt")
        allusers = json.loads(read_from_file("users.json"))
        print("AllUsers: {}".format(allusers))
            
        if 'check' in request.form:
            print("Check is requested")
            # Check that username is not empty
            if username == "":
                buttons={}
                buttons['register_active'] ="btn-deactivated btn-hide"
                buttons["check_active"] = ""
                message="Please type in a username and check its availability."
                attr=""
            elif username in allusers:
                buttons={}
                buttons['register_active'] ="btn-deactivated btn-hide"
                buttons["check_active"] = ""
                message="Username already exist try another one."
                attr=""
            else:
                buttons={}
                buttons['register_active'] =""
                buttons["check_active"] = "btn-deactivated btn-hide"
                message="Username available. Please click the register button."
                attr="required"
            return render_template("register.html", username=username, buttons=buttons, message=message, thisUser="", attr=attr)
        
        if 'register' in request.form:
            if username == "":
                buttons={}
                buttons['register_active'] ="btn-deactivated btn-hide"
                buttons["check_active"] = ""
                message="Please type in a username and check its availability."
                return render_template("register.html", username=username, buttons=buttons, message=message)
            else:
                # new_user = username + ": { username: " + username +", password: " + password +", total_points: 0 }"
                allusers[username]= { "username": username, "password": password, "total_points": 0, "results": [] }
                with open("data/users.json", "w") as outfile:
                    json.dump(allusers, outfile,  sort_keys=True, indent=4)

                return render_template("home.html", thisUser=username)

@app.route('/login', methods=['GET','POST'])
def login():
    thisUser=""

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        allusers = json.loads(read_from_file("users.json"))
        
        if username == "":
            allusers = ""
            message = "Please type in your username to login"
            return render_template("home.html", thisUser=defaultUser, message=message)
            
        elif password == "":
            allusers = ""
            message = "Please type in a password to login"
            return render_template("home.html", thisUser=defaultUser, message=message)
        
        elif username in allusers:
            '''
            for username in dict(allusers):
                print(allusers[username]['username'])
                print(allusers[username]['password'])  '''
            
            
            # Is user already logged in?
            if username in loggedUsers.keys():
                message = username + " is already logged in. Do you want to proceed? If you proceed the previous session will be destroyed."
                return render_template("proceed_login.html", thisUser="", username=username, message=message)
            
            #Check that password matches
            if password == allusers[username]['password']:
                x = createUser(username)
                loggedUsers[username].total_points = allusers[username]['total_points']
                loggedUsers[username].games_played = allusers[username]['results']
                return render_template("home.html", thisUser = loggedUsers[username])
        else:
            message = "You need to register before you can login"
            return render_template("home.html", thisUser=defaultUser, message1=message)
    
    return "What has happened - {}".format(username)

@app.route('/proceed_login/<username>', methods=['GET','POST'])
def proceed_login(username):
    loggedUsers[username].session += 1
    return render_template("home.html", thisUser = loggedUsers[username])

@app.route("/logout/<currentUser>/<sessionNo>", methods=['GET', 'POST'])
def logout(currentUser, sessionNo):
    try:
        thisUser = loggedUsers[currentUser] 
    except Exception as e:
        return "This session has expired. {} has been logged out from somewhere else.".format(e)
    
    if int(sessionNo) == thisUser.session:
        # Store info in JSON
        allusers = json.loads(read_from_file("users.json"))
        playing_user = allusers[thisUser.username]
        playing_user["total_points"] = thisUser.total_points
        playing_user["results"] = thisUser.games_played
        
        allusers[thisUser.username]= playing_user
        with open("data/users.json", "w") as outfile:
            json.dump(allusers, outfile,  sort_keys=True, indent=4)
        
        # IF GAME OBJECT EXIST DEL OTHERWISE NOTHING
        if game== "":
            pass
        else:
            del thisUser.game

        del thisUser
        del loggedUsers[currentUser]
        
        return redirect(url_for("home"))
    else:
        message = "This session has been disabled. You are logged in somewhere else."
        return redirect(url_for("home", message1=message))

@app.route("/createNewGame/<currentUser>/<sessionNo>", methods=['GET', 'POST'])
def createNewGame(currentUser, sessionNo):
    try:
        thisUser = loggedUsers[currentUser] 
    except Exception as e:
        return "This session has expired. {} has been logged out from somewhere else.".format(e)
    
    if int(sessionNo) == thisUser.session:
        thisUser.points_this_game = 0    # Reset Points
    
        if thisUser.is_logged:
            thisGame=thisUser.game = Game()
            message = ""
            nums = [thisGame.numbers[thisGame.index][0], thisGame.numbers[thisGame.index][1]]
            return render_template("game.html", thisUser=thisUser, nums=nums, index=thisGame.index+1, message = message)
        else:
            return render_template("home.html", thisUser=defaultUser)
    else:
        return "This session has been disabled. You are logged in somewhere else."

@app.route("/game/<currentUser>/<sessionNo>", methods=['GET', 'POST'])
def game(currentUser, sessionNo):
    global loggedUsers
    nums=[]
    thisUser=""

    try:
        thisUser = loggedUsers[currentUser]
        thisGame=thisUser.game
    except Exception as e:
        print(e)
        return "This session has expired. {} has been logged out from somewhere else.".format(currentUser)
    
    
    if int(sessionNo)  == thisUser.session:
            
        if request.method == 'POST':
            nums = [thisGame.numbers[thisGame.index][0], thisGame.numbers[thisGame.index][1]]
            return render_template("game.html", thisUser=thisUser, nums=nums, index=thisGame.index +1)
    else:
        return "This session has been disabled. You are logged in somewhere else."

@app.route("/checkAnswer/<currentUser>/<sessionNo>", methods=['GET', 'POST'])
def checkAnswer(currentUser, sessionNo):
    global loggedUsers
    nums=[]
    message=""
    thisUser=""

    try:
        thisUser = loggedUsers[currentUser]
        thisGame=thisUser.game
    except Exception as e:
        return "This session has expired. {} has been logged out from somewhere else.".format(currentUser)
    
    if int(sessionNo)  == thisUser.session:
        if request.method == 'POST':
            nums = [thisGame.numbers[thisGame.index][0], thisGame.numbers[thisGame.index][1]]
            answer = request.form['ans']
            # Check that there is an answer
            if answer == "":
                message = "You need to fill in your answer before submitting."
                return render_template("game.html", thisUser=thisUser, nums=nums, index=thisGame.index+1, message = message)

            correctAnswer = nums[0] + nums[1]
            
            if int(answer) == correctAnswer:
                message = "correct"
                thisUser.points_this_game += 5  # Add 5 points for each correct answer
            else:
                message = "wrong"
    else:
        return "This session has been disabled. You are logged in somewhere else."
    
    if thisGame.index + 1 == 10:
        thisUser.games_played.insert(0, thisUser.points_this_game)
        # Keep the latest 10 results
        while len(thisUser.games_played) > 10:
            thisUser.games_played.pop()
        thisUser.total_points += thisUser.points_this_game
    
    return render_template("answer.html", thisUser = thisUser, answer=answer, index=thisGame.index+1, nums = nums, message=message)

@app.route("/nextGame/<currentUser>/<sessionNo>", methods=['GET', 'POST'])
def nextGame(currentUser,sessionNo):
    global loggedUsers
    nums=[]
    thisUser=""
    message =""

    try:
        thisUser = loggedUsers[currentUser]
        thisGame=thisUser.game
    except Exception as e:
        return "This session has expired. {} has been logged out from somewhere else.".format(currentUser)

    if int(sessionNo)  == thisUser.session:
        thisGame.index += 1
        
        if thisGame.index+1 > len(thisGame.numbers):
            thisGame.index = 0
            message="Game Over. Would you like to play again?"
            return render_template("home.html", thisUser = thisUser, message=message)
        elif thisGame.index+1 == len(thisGame.numbers):
            message = "Last Game"
        
        nums = [thisGame.numbers[thisGame.index][0], thisGame.numbers[thisGame.index][1]]
        
        return render_template("game.html", thisUser=thisUser, nums=nums, index=thisGame.index+1, message = message)
    else:
        return "This session has been disabled. You are logged in somewhere else."
    
if __name__ == '__main__':
    app.run(host=os.getenv('IP'), port=int(os.getenv('PORT', 8080)), debug=True)