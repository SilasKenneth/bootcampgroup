from src.db import db
from werkzeug.security import generate_password_hash, check_password_hash
import datetime


class User(object):
    def __init__(self, username=None, password=None):
        self.password = password
        self.username = username
        self.lastLoggedIn = None
        self.logged_in = False
        self.role = "normal"

    @classmethod
    def login(cls):
        provide_username = input("Enter a username: ").strip()
        provided_password = input("Enter a password: ").strip()
        if provide_username == "":
            print("Provide a username")
            cls.login()
        user = cls.find_by_username(provide_username)
        if user is None:
            print("The username or password is incorrect.")
            cls.login()
        try:
            verified = check_password_hash(user.password, provided_password)
            if verified:
                db.logged_in = []
                db.logged_in.append(user)
                user.logged_in = True
                user.lastLoggedIn = datetime.datetime.utcnow()
                cls.dashboard()
            else:
                print("The username or password is incorrect.")
                cls.login()
        except Exception as ex:
            print("There was problem verifying the user. Please try again later")
            exit(0)

    @classmethod
    def find_by_username(cls, username):
        user_found = db.users.get(username, None)
        if username is None:
            return None
        return user_found

    def hash_password(self):
        self.password = generate_password_hash(self.password)

    def promote(self):
        """Promote the user from the normal user to the moderator"""
        self.role = "moderator"

    @classmethod
    def signup(cls):
        username = input("Enter a username: ").strip()
        password = input("Enter password: ").strip()
        if username == "" or password == "":
            print("Please enter a username and a password")
            cls.signup()
        user = User(username=username, password=password)
        user.hash_password()
        if user.username in db.users:
            print("The username is already in use")
            cls.signup()
        db.users.update({username: user})
        print("You successfully signed up. Login to get started")
        User.login()

    @classmethod
    def dashboard(cls):
        if len(db.logged_in) == 0:
            cls.login()
        else:
            current = db.logged_in[0]
            if not isinstance(current, (User, Moderator, Admin)):
                cls.login()
            print("Welcome to your home page %s" % current.username)
            print("1. Add comment")
            print("2. View all comments")
            selected = input("Select one of the above options")
            if not selected.isnumeric():
                print("Invalid option. Try again")
                cls.dashboard()
            selected = int(selected)
            if selected == 1:
                Comment.comment()
            elif selected == 2:
                Comment.print_all()

    @classmethod
    def default(cls):
        print("welcome to our comment System.")
        print("You can easily share your thoughts by creating a comment."
              " or replying to a specific comment.")
        print("These are the basic options enter one of them to get started")
        print("1. Log in")
        print("2. Sign up")
        response = input().strip()
        if not response.isnumeric():
            print("You entered an invalid option")
            cls.default()
        response = int(response)
        if response == 1:
            User.login()
        elif response == 2:
            User.signup()
        else:
            print("You entered an invalid option")
            cls.default()


class Moderator(User):
    def __init__(self):
        super(Moderator, self).__init__()

    def promote(self):
        self.role = "admin"

