# Addition Game

Working on the Riddle Game I had a problem. When a second user logs into the game
the information is not separated between the users. This messes up the information
for the first player.

This is the issue I want to tackle.

I will be using classes and generate a new object for each logged in user. I will 
still hold permanent information in json files.


## Heroku Deployment

Preparation:
~~~~
echo web: python game.py > Procfile  
sudo pip3 freeze --local > requirements.txt
~~~~

Logged in to heroku. (Need email and password)  
See list of the apps I already have.   
Creat a new app with the title "my-addition-game".  

Creation of a new app can be done through the Heroku interface.


This can also be done using the following command lines. Please note that this
will not set the Region to Europe but to United States instead.
~~~~
heroku login
heroku apps
heroku apps:create my-addition-game
~~~~
  
Logging into heroku and creating an app will also add a git remote. This can be 
viewed by listing the git remotes. 
[This requires that git has already been initialised.]
~~~~
git remote -v
~~~~

The result of the last command is:
~~~~
    heroku  https://git.heroku.com/riddle-guessing-game.git (fetch)
    heroku  https://git.heroku.com/riddle-guessing-game.git (push)
    origin  https://github.com/abonello/riddle-game-app.git (fetch)
    origin  https://github.com/abonello/riddle-game-app.git (push)
~~~~

Next I will push the project to heroku.
~~~~
git push -u heroku master
~~~~

Successfully installed Flask-0.12.2 Jinja2-2.10 MarkupSafe-1.0 Werkzeug-0.14.1 click-6.7 itsdangerous-0.24
https://riddle-guessing-game.herokuapp.com/ deployed to Heroku
remote: Verifying deploy... done.
To [Riddle-Guessing-Game](https://git.heroku.com/riddle-guessing-game.git)

Create a watcher in heroku.
~~~~
heroku ps:scale web=1
~~~~

Next we need to go to the Heroku site. Select the app. From settings, click on 
*Reveal Config Vars*. Here you need to create some configuration variables.
Set the following key : value pairs
IP 0.0.0.0
PORT 5000

These will be the IP and PORT used in the following line of code in run.py
~~~~python
app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)
~~~~