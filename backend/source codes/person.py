class Person:
    def __init__(self, user_id, user_name, password, user_type):
        self.id = user_id
        self.user_name = user_name
        self.password = password
        self.user_type = user_type

    def get_id(self):
        return self.id

    def get_user_name(self):
        return self.user_name

    def get_user_type(self):
        return self.user_type
