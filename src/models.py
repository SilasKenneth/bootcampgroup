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


class Admin(Moderator):
    def __init__(self):
        super(Admin, self).__init__()


class Comment(object):
    def __init__(self, body):
        if len(db.logged_in) == 0:
            print("You must log in to comment")
            User.default()
        self.body = body
        self.comment_id = 1
        if db.comment_last_id != -1:
            self.comment_id = db.comment_last_id + 1
        self.owner = db.logged_in[0]
        self.replies = []

    def print(self):
        print(self)
        for reply in self.replies:
            print(reply)

    def __repr__(self):
        return "%s %s by (%s)".format(self.id, self.body, self.owner.username)

    def delete(self):
        pass

    def edit(self, comment_id, newbody=""):
        if len(db.logged_in) == 0:
            User.login()
        if newbody.strip() == "":
            print("You never provided any new body so we left the comment as was")

    @classmethod
    def comment(cls, parent=None):
        if parent is None:
            pass
    @classmethod
    def reply(cls, comment_id):
        pass

    @classmethod
    def print_all(cls):
        pass


User.default()