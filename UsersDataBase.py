import Errors
from User import User
import pickle
import os
import Config
from Series import Series
import Helpers

class UsersDataBase:

    def __init__(self):

        self.dic_of_users = {}  # user_name : User

    def load_data_base(self):
        if not os.path.exists(Config.USERS_DATA_BASE_FILE_PATH):
            raise Errors.DataBaseNotFound()
        file_ob = open(Config.USERS_DATA_BASE_FILE_PATH, 'r')
        self.dic_of_users = pickle.load(file_ob)
        print "dic of users - {}".format(repr(self.dic_of_users))
        file_ob.close()

    def save_data_base(self):
        Helpers.dump_to_pickle_object(Config.USERS_DATA_BASE_FILE_PATH, self.dic_of_users)

    def get_new_user_id(self):
        num_of_current_users = len(self.dic_of_users)
        id = num_of_current_users + 1
        return id

    def check_if_user_exist(self,username):
        ans = False
        if username in self.dic_of_users:
            ans = True

        return ans

    def validate_password(self,username,password):
        ans = False
        if self.dic_of_users[username].password == password:
            ans = True
        return ans

    def sign_up(self,username,password):

        if self.check_if_user_exist(username):
            raise Errors.UserAlreadyExists(username)

        new_user = User(username,password)
        new_user.id = self.get_new_user_id()
        self.dic_of_users[username] = new_user
