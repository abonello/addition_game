class User:
    def __init__(self, username, password, number):
        self.username=username
        self.password=password
        self.number=number
    
user1=User("USER1", "qwer", 98)
print("user1 is {}".format(user1))
# <__main__.User object at 0x102ac34e0>
print("")
print("user1.username is {}".format(user1.username))
# 'USER1'
print("user1.password is {}".format(user1.password))
# 'qwer'
print("user1.number is {}".format(user1.number))
# 98

print("")
user2=User("USER2", "asdf", 34)
print("user2 is {}".format(user2))
# <__main__.User instance at 0x7fc035925cb0>
print("")
print("user2.username is {}".format(user2.username))
# 'USER2'
print("user2.password is {}".format(user2.password))
# 'asdf'
print("user2.number is {}".format(user2.number))
# 34
print("")
print("")

print("user1.username is {}".format(user1.username))
# 'USER1'

u = "user1"
print("u stores the name of an instance as a string.")
print("u is {}".format(u))
# 'user1'
print("Type of u is {}".format(type(u)))
# <type 'str'>

print("Change u to point to the instance of user1.")
print("vars()[u].username")
print("Then, u.username is {}".format(vars()[u].username))
# 'USER1'
print("Then, u.password is {}".format(vars()[u].password))
# 'qwer'
print("Then, u.number is {}".format(vars()[u].number))
# 98

print("")
print("")
print("")
print("I can make the 'string' pointing to the instance and store it in new variable.")
print("thisUser = vars()[u]")
thisUser = vars()[u]
print("")
print("Then:")
print("thisUser.username will be {}".format(thisUser.username))
# 'USER1'
print("thisUser.password will be {}".format(thisUser.password))
# 'qwer'
print("thisUser.number will be {}".format(thisUser.number))
# 98
