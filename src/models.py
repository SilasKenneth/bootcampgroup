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
            cls.dashboard()

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
            print("3. Log out")
            selected = input("Select one of the above options")
            if not selected.isnumeric():
                print("Invalid option. Try again")
                cls.dashboard()
            selected = int(selected)
            if selected == 1:
                Comment.comment()
            elif selected == 2:
                Comment.print_all()
            elif selected == 3:
                User.logout()

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
    @classmethod
    def logout(cls):
        db.logged_in = []
        User.default()

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
        self.id = db.comment_last_id + 1
        if len(db.logged_in) == 0:
            print("You must log in to comment")
            User.default()
        self.body = body
        self.comment_id = 1
        if db.comment_last_id != -1:
            self.comment_id = db.comment_last_id + 1
        self.owner = db.logged_in[0]
        self.replies = []
        self.timestamp = datetime.datetime.utcnow()

    def __repr__(self):
        return "%s %s %s by (%s) input %s to reply."%(self.id, self.body, str(self.timestamp), self.owner.username, str(self.id+1000))
    def print_this(self):
        print("*"*20)
        print("%s %s %s by (%s) input %s to reply."%(self.id, self.body, str(self.timestamp), self.owner.username, str(self.id+1000)))
        if len(self.replies) == 0:
            print("No comments")
        else:
            print("Comments")
        for repl in self.replies:
            print(repl)
        print("="*20)
    def delete(self):
        pass

    def edit(self, comment_id, newbody=""):
        if len(db.logged_in) == 0:
            User.login()
        if newbody.strip() == "":
            print("You never provided any new body so we left the comment as was")
            
    @classmethod
    def comment(cls):
        body = input("Enter the comment: ").strip()
        if body == "":
            print("Please enter a comment body.")
            cls.comment()
        next_id = db.comment_last_id + 1
        comment_c = Comment(body)
        comment_c.id = next_id
        db.comments.update({next_id: comment_c})
        db.comment_last_id = next_id
        User.dashboard()
    @classmethod
    def reply(cls, commenter):
        if not isinstance(commenter, (Comment)):
            print("Something went wrong processing your request")
            User.dashboard()
        repl = input("Enter the reply body")
        commenter.replies.append(repl)
        print("Reply added")
        User.dashboard()

    @classmethod
    def print_all(cls):
        for comment_id in db.comments:
            print(db.comments.get(comment_id).print_this())
        print("Input the reply id to comment.")
        id_selected = input("Enter the id. ")
        if not id_selected.isnumeric():
            print("Wrong input. Try again")
            cls.print_all()
        id_selected = int(id_selected)
        comm = db.comments.get(id_selected - 1000, None)
        if comm is not None:
            cls.reply(comm)
        User.dashboard()




