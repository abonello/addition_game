import os
import copy
import random
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

loggedUsers = {}

# print("START NEW GAME\n\n\n+++++++++++++++++++")
# print("Logged Users: {}\n\n===================".format(loggedUsers))

class User:
    logged_users = 0
    
    def __init__(self, username, password, is_logged, session):
        self.username = username
        self.password = password
        self.is_logged = is_logged
        self.total_points = 0
        self.points_this_game = 0
        self.games_played = []
        self.game = ""
        self.session = session
        
        User.logged_users += 1
        
        def addLoggedUser(self):
            global loggedUsers
            loggedUsers[self.username] = self
            # print(loggedUsers)
            
        def setSession(self):
            print("setSession has been called")
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
        # print("Session: {} set for User: {}".format(self.session, self.username))
        # print(loggedUsers)
        
    def reference(self):
        return "{}.{}".format(self.username, self.password)

class Game:
    def __init__(self):
        # self.numbers = [[3, 6], [2, 7], [1, 4], [2, 8], [0, -5], [3, 4], [-3, 5], [1, 9], [2, 2], [6, 1]]
        # self.numbers = []
        self.numbers = self.generateNumbers()
        self.index = 0
        
        # self.generateNumbers()
        print(self.numbers)
        
    def generateNumbers(self):
        nums = []
        for i in range(10):
            x=[random.randint(-10, 10), random.randint(-10, 10)]
            nums.append(x)
        return nums

defaultUser = User("Please type a username to log in or register", "", False, 100)

def read_from_file(file_name):
    store=""
    file = "data/" + file_name
    with open(file, "r") as readdata:
        store = readdata.read()
    return store

def createUser(name):
    tempUser = User(name, "asdf", True, 100)
    # x = name
    # print("5. x = {}".format(x))
    # print("6. Type of x is {}".format(type(x)))
    
    # print("7. tempUser = {}".format(tempUser))
    # print("8. Type of tempUser is {}".format(type(tempUser)))
    
    vars()[name] = copy.deepcopy(tempUser)
    loggedUsers[name] = copy.deepcopy(tempUser)
    
    # print("9. vars()[name] = {}".format(vars()[name]))
    # print("10. Type of vars()[name] is {}".format(type(vars()[name])))
    return vars()[name]

@app.route("/")
def home():
    thisUser=defaultUser
    return render_template("home.html", thisUser=thisUser)
    
@app.route('/prepare_register', methods=['GET','POST'])
def prepare_register():
    if request.method == 'POST':
        buttons={}
        buttons['register_active'] ="btn-deactivated btn-hide"
        buttons["check_active"] = ""
        # print("Buttons prepared: {}".format(buttons))
        return render_template("register.html", buttons=buttons, thisUser="")

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        allusers = read_from_file("users.txt")
            
        if 'check' in request.form:
            # Check that username is not empty
            if username == "":
                buttons={}
                buttons['register_active'] ="btn-deactivated btn-hide"
                buttons["check_active"] = ""
                message="Please type in a username and check its availability."
            elif username in allusers:
                buttons={}
                buttons['register_active'] ="btn-deactivated btn-hide"
                buttons["check_active"] = ""
                message="Username already exist try another one."
            else:
                buttons={}
                buttons['register_active'] =""
                buttons["check_active"] = "btn-deactivated btn-hide"
                message="Username available. Please click the register button."
            return render_template("register.html", username=username, buttons=buttons, message=message, thisUser="")
        
        if 'register' in request.form:
            if username == "":
                buttons={}
                buttons['register_active'] ="btn-deactivated btn-hide"
                buttons["check_active"] = ""
                message="Please type in a username and check its availability."
                return render_template("register.html", username=username, buttons=buttons, message=message)
            else:
                with open("data/users.txt", "a") as addusernames:
                    addusernames.write(username + "\n")
                return render_template("home.html", thisUser=username)
    # return render_template("register.html")

@app.route('/login', methods=['GET','POST'])
def login():
    # thisUser=defaultUser
    thisUser=""
    # print("1. thisUser is {}".format(thisUser))
    # print("2. Type of thisUser is {}".format(type(thisUser)))
    
    
    if request.method == 'POST':
        username = request.form['username']
        # print("================")
        # print("The Username that is passed is: {}".format(username))
        # print("================")
        allusers = read_from_file("users.txt")
        
        # print("3. Username: {}".format(username))
        # print("4. All registered users: \n{}".format(allusers))
        
        if username == "":
            allusers = ""
            #     app_info["logged"] = False                I do not need this I think
            #     username = "Enter a username to log in"  Display a message
            message = "Please type in your username to login"
            return render_template("home.html", thisUser=defaultUser, message=message)
        
        elif username in allusers:
            
            # Is user already logged in?
            if username in loggedUsers.keys():
                message = username + " is already logged in. Do you want to proceed? If you proceed the previous session will be destroyed."
                return render_template("proceed_login.html", thisUser="", username=username, message=message)
            
            x = createUser(username)
            # print("11. {}".format(loggedUsers))
            # print("12. Number of Logged users: {}".format(User.logged_users))
            return render_template("home.html", thisUser = loggedUsers[username])
        
        else: # I will have to change this when I write the code for registration.
            
            # x = createUser(username)
            # loggedUsers[username] = x
            # print("11. {}".format(loggedUsers))
            # print("12. Number of Logged users: {}".format(User.logged_users))
            # print("13. Current User from Instance: {}".format(loggedUsers[username].username))
            # print(loggedUsers["Test_USER_4"].username)
            # return render_template("home.html", thisUser = vars()[username])
            message = "You need to register before you can login"
            return render_template("home.html", thisUser=defaultUser, message1=message)
            # return render_template("home.html", thisUser="", message1=message)
    
    return "What has happened - {}".format(username)

# @app.route('/proceed_login', methods=['GET','POST'])
@app.route('/proceed_login/<username>', methods=['GET','POST'])
def proceed_login(username):
    print("Proceed_login FOUND")
    print("Username passed is {}".format(username))
    loggedUsers[username].session += 1
    print("This is user {}.".format(loggedUsers[username].username))
    return render_template("home.html", thisUser = loggedUsers[username])

@app.route("/logout/<currentUser>/<sessionNo>", methods=['GET', 'POST'])
def logout(currentUser, sessionNo):
    try:
        thisUser = loggedUsers[currentUser] 
    except Exception as e:
        # print(e)
        return "This session has expired. {} has been logged out from somewhere else.".format(e)

    
    # print("1. {}".format(thisUser.game.numbers) )
    # print("Current User received: {}".format(currentUser))
    # print("Session received: {}".format(sessionNo))
    # print("Type of Session received: {}".format(type(sessionNo)))
    # print("This User's session: {}".format(thisUser.session))
    # print("Type of User's session: {}".format(type(thisUser.session)))
    # print("This User's username: {}".format(thisUser.username))
    
    if int(sessionNo) == thisUser.session:
        # IF GAME OBJECT EXIST DEL OTHERWISE NOTHING
        if game== "":
            pass
        else:
            del thisUser.game
        
        # print("2. {}".format(thisUser.game.numbers) )
        # print("3. {}".format(thisUser))
        del thisUser
        # print("4. {}".format(thisUser))
        # thisUser = defaultUser
        del loggedUsers[currentUser]
        
        # return "{} is now logged out. Current user is {}.".format(currentUser, thisUser.username)
        # return render_template("home.html", thisUser=defaultUser)
        return redirect(url_for("home"))
    else:
        # return "This session has been disabled. You are logged in somewhere else."
        message = "This session has been disabled. You are logged in somewhere else."
        return redirect(url_for("home", message1=message))

@app.route("/createNewGame/<currentUser>/<sessionNo>", methods=['GET', 'POST'])
def createNewGame(currentUser, sessionNo):
    # thisUser = loggedUsers[currentUser]
    try:
        thisUser = loggedUsers[currentUser] 
    except Exception as e:
        # print(e)
        return "This session has expired. {} has been logged out from somewhere else.".format(e)
        # message = "This session has expired. {} has been logged out from somewhere else.".format(e)
        # return redirect(url_for("home", message=message))
    
    
    
    if int(sessionNo) == thisUser.session:
        thisUser.points_this_game = 0    # Reset Points
    
        if thisUser.is_logged:
            # print("=======================")
            # print("1. thisUser is {}".format(thisUser))
            # print("2. Type of thisUser is {}".format(type(thisUser)))
            thisGame=thisUser.game = Game()
            # print("3. thisGame is {}".format(thisGame))
            # print("4. Type of thisGame is {}".format(type(thisGame)))
            # print("5. Game List = {}".format(thisGame.numbers))
            # print("6. Game Index = {}".format(thisGame.index))
            
            message = ""
            nums = [thisGame.numbers[thisGame.index][0], thisGame.numbers[thisGame.index][1]]
            # print("7. Numbers for this game are {}".format(nums))
            
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
    # USER 1 playing
    # thisGame=user1_game
    
    # USER 2 playing
    # thisGame=user2_game
    
    
    # for key, value in loggedUsers.items():
    #     if key == currentUser:
    #         thisUser = value
    # thisUser = loggedUsers[currentUser]
    try:
        thisUser = loggedUsers[currentUser]
        thisGame=thisUser.game
    except Exception as e:
        print(e)
        return "This session has expired. {} has been logged out from somewhere else.".format(currentUser)
    
    
    if int(sessionNo)  == thisUser.session:
            
        if request.method == 'POST':
            # currentUser = request.form['username']
            # print("POST received")
            # print(currentUser)
            # print(user1.number)
            # num1 = user1_game.numbers[user1_game.index]
            # num2 = user1_game.numbers[user1_game.index + 1]
            # nums = [user1_game.numbers[user1_game.index], user1_game.numbers[user1_game.index + 1]]
            nums = [thisGame.numbers[thisGame.index][0], thisGame.numbers[thisGame.index][1]]
            
            # user1_game.index += 2
            # return "Current user is {}. POST submitted. Add the following: {}, {}".format(currentUser, user1_game.numbers[user1_game.index], user1_game.numbers[user1_game.index + 1])
            return render_template("game.html", thisUser=thisUser, nums=nums, index=thisGame.index +1)
    else:
        return "This session has been disabled. You are logged in somewhere else."
    
    # return "Answer was submitted"
    # return render_template("game.html", thisUser=user1, index=user1_game.index, nums=nums) #num1=num1, num2=num2)
    # return render_template("game.html", thisUser=thisUser, nums=nums, index=thisGame.index +1)

@app.route("/checkAnswer/<currentUser>/<sessionNo>", methods=['GET', 'POST'])
def checkAnswer(currentUser, sessionNo):
    global loggedUsers
    nums=[]
    message=""
    thisUser=""
    # USER 1 playing
    # thisGame=user1_game
    
    # USER 2 playing
    # thisGame=user2_game
    
    # for key, value in loggedUsers.items():
    #     if key == currentUser:
    #         thisUser = value
    # thisUser = loggedUsers[currentUser]        
    # thisGame=thisUser.game
    try:
        thisUser = loggedUsers[currentUser]
        thisGame=thisUser.game
    except Exception as e:
        print(e)
        return "This session has expired. {} has been logged out from somewhere else.".format(currentUser)
    
    if int(sessionNo)  == thisUser.session:
        if request.method == 'POST':
            
            # num1 = user1_game.numbers[user1_game.index]
            # num2 = user1_game.numbers[user1_game.index + 1]
            nums = [thisGame.numbers[thisGame.index][0], thisGame.numbers[thisGame.index][1]]
            
            answer = request.form['ans']
            # Check that there is an answer
            if answer == "":
                message = "You need to fill in your answer before submitting."
                return render_template("game.html", thisUser=thisUser, nums=nums, index=thisGame.index+1, message = message)
            # elif not type(answer) == int:
            #     message = "Your answer must be an integer."
            #     return render_template("game.html", thisUser=thisUser, nums=nums, index=thisGame.index+1, message = message)
            
            # correctAnswer = num1 + num2
            correctAnswer = nums[0] + nums[1]
            
            if int(answer) == correctAnswer:
                message = "correct"
                thisUser.points_this_game += 5  # Add 5 points for each correct answer
                print(thisUser.points_this_game)
            else:
                message = "wrong"
                print(thisUser.points_this_game)
    else:
        return "This session has been disabled. You are logged in somewhere else."
        
    # return "{}, answer submitted is {}. You were asked to add {} and {} and your answer is {}.".format(currentUser, answer, num1, num2, message)
    # return render_template("answer.html", thisUser = user1, answer=answer, num1=num1, num2=num2, message=message)
    
    if thisGame.index + 1 == 10:
        print("->")
        print(thisUser.points_this_game)
        thisUser.games_played.append(thisUser.points_this_game)
    
    return render_template("answer.html", thisUser = thisUser, answer=answer, index=thisGame.index+1, nums = nums, message=message)

@app.route("/nextGame/<currentUser>/<sessionNo>", methods=['GET', 'POST'])
def nextGame(currentUser,sessionNo):
    global loggedUsers
    nums=[]
    thisUser=""
     # USER 1 playing
    # thisGame=user1_game
    
    # USER 2 playing
    # thisGame=user2_game
    message =""
    
    # for key, value in loggedUsers.items():
    #     if key == currentUser:
    #         thisUser = value
    # thisUser = loggedUsers[currentUser]
    # thisGame=thisUser.game
    try:
        thisUser = loggedUsers[currentUser]
        thisGame=thisUser.game
    except Exception as e:
        print(e)
        return "This session has expired. {} has been logged out from somewhere else.".format(currentUser)
    
    # print(thisUser)
    # print(thisUser.username)
    # print(thisUser.password)
    # print(thisUser.number)
    # user1_game.index += 1
    if int(sessionNo)  == thisUser.session:
        thisGame.index += 1
        
        if thisGame.index+1 > len(thisGame.numbers):
            thisGame.index = 0
            message="Game Over. Would you like to play again?"
            return render_template("home.html", thisUser = thisUser, message=message)
        elif thisGame.index+1 == len(thisGame.numbers):
            message = "Last Game"
        
        # nums = [user1_game.numbers[user1_game.index], user1_game.numbers[user1_game.index + 1]]
        nums = [thisGame.numbers[thisGame.index][0], thisGame.numbers[thisGame.index][1]]
        
        # return render_template("game.html", thisUser=user1, index=user1_game.index, nums=nums) #num1=num1, num2=num2)
        return render_template("game.html", thisUser=thisUser, nums=nums, index=thisGame.index+1, message = message)
    else:
        return "This session has been disabled. You are logged in somewhere else."
    
if __name__ == '__main__':
    app.run(host=os.getenv('IP'), port=int(os.getenv('PORT', 8080)), debug=True)