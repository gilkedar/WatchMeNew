from UsersDataBase import UsersDataBase
from SeriesDataBase import SeriesDataBase
from Date import Date
import Errors
import Config
import os
import pickle
from Session import Session
import Helpers


USERNAME = "gilkedar"
PASSWORD = "1234"


class Main:

    def __init__(self):

        self.users_data_base = UsersDataBase()
        self.series_data_base = None

        self.curr_session = None
        self.user = None

    def load_series_data_base(self):
        if not os.path.exists(Config.SERIES_DATA_BASE_FILE_PATH):
            # raise Errors.DataBaseNotFound()
            print "series data base not found"
            self.series_data_base = SeriesDataBase()
            # self.series_data_base.update_all_shows_dic()
            # self.series_data_base.save_series_data_base()
        else:
            self.series_data_base = Helpers.load_pickle_object(Config.SERIES_DATA_BASE_FILE_PATH)
            # self.series_data_base.update_data_base()# user should decide when to update

    def sign_up(self,username,password):

        self.users_data_base.sign_up(username,password)

    def log_in(self,username,password):
        print "login : {} {}".format(username,password)

        if not self.users_data_base.check_if_user_exist(username):
            raise Errors.UserDoesnExist(username)

        if not self.users_data_base.validate_password(username, password):
            raise Errors.InvalidPassword(username)

        self.user = self.users_data_base.dic_of_users[username]
        # return user
        # self.user.update_series_objects()

    # def save_series_data_base(self):
    #     Helpers.dump_to_pickle_object(Config.SERIES_DATA_BASE_FILE_PATH,self.series_data_base)
    #
    # def save_users_data_base(self):
    #     Helpers.dump_to_pickle_object(Config.USERS_DATA_BASE_FILE_PATH, self.users_data_base.dic_of_users)

    def finish_session(self):
        print "finishing session"
        if self.user:
            self.user.set_last_visit()
            self.users_data_base.dic_of_users[self.user.user_name] = self.user
            self.users_data_base.save_data_base()
            self.series_data_base.save_series_data_base()


    def choose_user(self):

        #for now choose only and first user in db dic

        print "choosing user"
        user_name = self.users_data_base.dic_of_users.keys()[0]
        self.user = self.users_data_base.dic_of_users[user_name]
        print self.user


    def start_first_session(self):

        pass



if __name__ == "__main__":

    print "Not executable"