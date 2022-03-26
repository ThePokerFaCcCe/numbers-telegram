from ..model import Model


class Admin(Model):
    user_id = int

    def __init__(self, user_id):
        self.user_id = user_id
