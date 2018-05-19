import os
import copy
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

loggedUsers = {}

class User:
    
    logged_users = 0
    
    def __init__(self, username, password, is_logged, number):
        self.username = username
        self.password = password
        self.is_logged = False
        self.number = number
        self.total_points = 0
        self.points_this_game = 0
        # self.games_list = []
        self.game = ""
        
        User.logged_users += 1
        
        def addLoggedUser(self):
            global loggedUsers
            loggedUsers[self.username] = self
            # print(loggedUsers)
            
        addLoggedUser(self)
        
    def reference(self):
        return "{}.{}".format(self.username, self.password)
    
    # def createGame(self):
    #     self.games = Game()
    


class Game:
    def __init__(self):
        self.numbers = [[3, 6], [2, 7], [1, 4], [2, 8], [0, -5], [3, 4], [-3, 5], [1, 9], [2, 2], [6, 1]]
        self.index = 0
    

defaultUser = User("Please type a username to log in or register", "", False, 0)
user1 = User("user1", "asdf", True, 32)
user2 = User("user2", "qwerty", True, 87)
user1_game = Game()
user2_game = Game()

def read_from_file(file_name):
    store=""
    file = "data/" + file_name
    with open(file, "r") as readdata:
        store = readdata.read()
    return store

@app.route("/")
def home():
    thisUser=defaultUser
    return render_template("home.html", thisUser = thisUser)

def createUser(name):
    tempUser = User(name, "asdf", True, 32)
    x = name
    print("5. x = {}".format(x))
    print("6. Type of x is {}".format(type(x)))
    
    print("7. tempUser = {}".format(tempUser))
    print("8. Type of tempUser is {}".format(type(tempUser)))
    
    vars()[name] = copy.deepcopy(tempUser)
    loggedUsers[name] = copy.deepcopy(tempUser)
    
    print("9. vars()[name] = {}".format(vars()[name]))
    print("10. Type of vars()[name] is {}".format(type(vars()[name])))
    return vars()[name]
    
    

@app.route('/login', methods=['GET','POST'])
def login():
    thisUser=defaultUser
    print("1. thisUser is {}".format(thisUser))
    print("2. Type of thisUser is {}".format(type(thisUser)))
    
    
    if request.method == 'POST':
        username = request.form['username']
        allusers = read_from_file("users.txt")
        
        print("3. Username: {}".format(username))
        print("4. All registered users: \n{}".format(allusers))
        
        if username == "":
            allusers = ""
            #     app_info["logged"] = False                I do not need this I think
            #     username = "Enter a username to log in"  Display a message
            return redirect(url_for('home'))
        
        elif username in allusers:
            x = createUser(username)
            print("11. {}".format(loggedUsers))
            print("12. Number of Logged users: {}".format(User.logged_users))
            return render_template("home.html", thisUser = loggedUsers[username])
        
        else: # I will have to change this when I write the code for registration.
            x = createUser(username)
            # loggedUsers[username] = x
            print("11. {}".format(loggedUsers))
            print("12. Number of Logged users: {}".format(User.logged_users))
            print("13. Current User from Instance: {}".format(loggedUsers[username].username))
            # print(loggedUsers["Test_USER_4"].username)
            # return render_template("home.html", thisUser = vars()[username])
            return render_template("home.html", thisUser = loggedUsers[username])
            
        
        # if app_info["username"] == "":
        #     app_info["allusers"] = ""
        #     app_info["logged"] = False
        #     app_info["username"] = "Enter a username to log in"
        #     return redirect(url_for('index'))
        # elif app_info["username"] in app_info["allusers"]:
        #     app_info["logged"] = True
        #     session['logged_in'] = True
        #     return redirect(url_for('user'))
        # else:
        #     app_info["username"] = "That username does not exist. Please register first."
        #     app_info["logged"] = False
        #     return redirect(url_for('index'))
    
    return "What has happened - {}".format(username)

@app.route("/createNewGame/<currentUser>", methods=['GET', 'POST'])
def createNewGame(currentUser):
    thisUser = loggedUsers[currentUser]
    print("=======================")
    print("1. thisUser is {}".format(thisUser))
    print("2. Type of thisUser is {}".format(type(thisUser)))
    thisGame=thisUser.game = Game()
    print("3. thisGame is {}".format(thisGame))
    print("4. Type of thisGame is {}".format(type(thisGame)))
    print("5. Game List = {}".format(thisGame.numbers))
    print("6. Game Index = {}".format(thisGame.index))
    
    message = ""
    
    nums = [thisGame.numbers[thisGame.index][0], thisGame.numbers[thisGame.index][1]]
    
    print("7. Numbers for this game are {}".format(nums))
    
    return render_template("game.html", thisUser=thisUser, nums=nums, index=thisGame.index+1, message = message)

@app.route("/game/<currentUser>", methods=['GET', 'POST'])
def game(currentUser):
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
    thisUser = loggedUsers[currentUser]    
    thisGame=thisUser.game
            
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
    
    # return "Answer was submitted"
    # return render_template("game.html", thisUser=user1, index=user1_game.index, nums=nums) #num1=num1, num2=num2)
    return render_template("game.html", thisUser=thisUser, nums=nums, index=thisGame.index +1)
    
    
@app.route("/checkAnswer/<currentUser>", methods=['GET', 'POST'])
def checkAnswer(currentUser):
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
    thisUser = loggedUsers[currentUser]        
    thisGame=thisUser.game
            
    if request.method == 'POST':
        
        
        
        # num1 = user1_game.numbers[user1_game.index]
        # num2 = user1_game.numbers[user1_game.index + 1]
        nums = [thisGame.numbers[thisGame.index][0], thisGame.numbers[thisGame.index][1]]
        
        answer = request.form['ans']
        # Check that there is an answer
        if answer == "":
            message = "You need to fill in your answer before submitting."
            return render_template("game.html", thisUser=thisUser, nums=nums, index=thisGame.index+1, message = message)
        
        # correctAnswer = num1 + num2
        correctAnswer = nums[0] + nums[1]
        
        if int(answer) == correctAnswer:
            message = "correct"
        else:
            message = "wrong"
        
        
    # return "{}, answer submitted is {}. You were asked to add {} and {} and your answer is {}.".format(currentUser, answer, num1, num2, message)
    # return render_template("answer.html", thisUser = user1, answer=answer, num1=num1, num2=num2, message=message)
    return render_template("answer.html", thisUser = thisUser, answer=answer, nums = nums, message=message)

@app.route("/nextGame/<currentUser>", methods=['GET', 'POST'])
def nextGame(currentUser):
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
    thisUser = loggedUsers[currentUser]
    thisGame=thisUser.game
    
    # print(thisUser)
    # print(thisUser.username)
    # print(thisUser.password)
    # print(thisUser.number)
    # user1_game.index += 1
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

    

    
if __name__ == '__main__':
    app.run(host=os.getenv('IP'), port=int(os.getenv('PORT', 8080)), debug=True)