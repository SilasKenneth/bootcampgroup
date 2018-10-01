class DB(object):
    """The database class"""
    def __init__(self):
        """The database constructor"""
        self.users = {}
        self.comments = {}
        self.logged_in = []
        self.comment_last_id = -1
        self.users_last_id = -1


db = DB()
