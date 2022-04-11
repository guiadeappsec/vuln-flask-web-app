class UserDbModel:
    def __init__(self, db_result):
        self.id = db_result[0]
        self.username = db_result[1]
        self.password = db_result[2]
        self.is_admin = db_result[3] == 1


class DbModels:
    def __init__(self):
        self.UserDbModel = UserDbModel


db_models = DbModels()