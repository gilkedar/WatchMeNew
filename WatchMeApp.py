from PyQt4 import QtGui  # Import the PyQt4 module we'll need
import sys  # We need sys so that we can pass argv to QApplication

from UI.LogIn import Ui_Login
from UI.WatchMe import Ui_WatchMe
from UI.SignUp import Ui_SignUp

from Session import Session

from Main import Main
import Config
import Errors

# This file holds our MainWindow and all design related things

# it also keeps events etc that we defined in Qt Designer
import os  # For listing directory methods


MainManager = Main()


class LogIn_UI_Class(QtGui.QMainWindow, Ui_Login):
    def __init__(self):
        # Explaining super is out of the scope of this article
        # So please google it if you're not familar with it
        # Simple reason why we use it here is that it allows us to
        # access variables, methods etc in the design.py file
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in design.py file automatically
        # It sets up layout and widgets that are defined

        self.logInBtn.clicked.connect(self.login_btn_pushed)
        self.signUpBtn.clicked.connect(self.signup_btn_pushed)

    def signup_btn_pushed(self):

        signup_form.show()
        login_form.hide()


    def login_btn_pushed(self):

        user_name = str(self.userNameLine.text())
        if not user_name:
            raise Errors.EmptyFieldError("username")
        password = str(self.passwordLine.text())
        if not password:
            raise Errors.EmptyFieldError("password")

        MainManager.log_in(user_name,password)
        login_form.hide()
        watchme_form.show()


class WatchMe_UI_Class(QtGui.QMainWindow, Ui_WatchMe):
    def __init__(self):
        # Explaining super is out of the scope of this article
        # So please google it if you're not familar with it
        # Simple reason why we use it here is that it allows us to
        # access variables, methods etc in the design.py file
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in design.py file automatically
        # It sets up layout and widgets that are defined

class SignUp_UI_Class(QtGui.QFrame, Ui_SignUp):

    MIN_USERNAME_CHARS = 3

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        self.btn_signup.clicked.connect(self.callback__btn_signup)
        self.btn_login.clicked.connect(self.callback__btn_login)


    def verify_password(self,pass1,pass2):

        if pass1 == pass2:
            return True
        else:
            raise Errors.PasswordsDoNotMatch()

    def verify_username(self,username):

        num_of_chars = len(username)
        if num_of_chars < self.MIN_USERNAME_CHARS:
            raise Errors.InvalidUsernameError(self.MIN_USERNAME_CHARS)

    def verify_email(self,email):

        if "@" in email:
            user = email.split("@")[0]
            if not user:
                raise Errors.InvalidEmail("username@domain.com")
            domain = email.split("@")[1]
            if not domain:
                raise Errors.InvalidEmail("username@domain.something")
            if "." not in domain:
                raise Errors.InvalidEmail(".")
        else:
            raise Errors.InvalidEmail("@")


    def callback__btn_signup(self):


        user_name = str(self.line_username.text())
        if not user_name:
            raise Errors.EmptyFieldError("username")
        password = str(self.line_password.text())
        if not password:
            raise Errors.EmptyFieldError("password")
        confirmed = str(self.line_confirm_password.text())
        if not confirmed:
            raise Errors.EmptyFieldError("Confirm Password")
        email = str(self.line_email.text())
        if not email:
            raise Errors.EmptyFieldError("Email")

        self.verify_username(user_name)
        self.verify_password(password,confirmed)
        self.verify_email(email)

        MainManager.sign_up(user_name,password)
        signup_form.hide()
        login_form.userNameLine.setText(user_name)
        login_form.passwordLine.setText(password)
        login_form.show()

    def callback__btn_login(self):

        signup_form.hide()
        login_form.show()








def run_first_session():

    print "starting first user session"
    try:
        MainManager.load_series_data_base()
        signup_form.show()
        app.exec_()  # and execute the app

    except Exception as ex:
        pass


#shuold have a user already signed in
def run_user_session():

    print "starting session for user - {}".format(MainManager.user.user_name)

    watchme_form.show()

    app.exec_()  # and execute the app


def get_session_dependencies():

    MainManager.users_data_base.load_data_base()
    MainManager.choose_user()
    MainManager.load_series_data_base()



if __name__ == '__main__':  # if we're running file directly and not importing it

    app = QtGui.QApplication(sys.argv)  # A new instance of QApplication

    login_form = LogIn_UI_Class()  # We set the form to be our ExampleApp (design)
    watchme_form = WatchMe_UI_Class()
    signup_form = SignUp_UI_Class()

    # app.exec_()  # and execute the app
    dependencies_ok = True
    try:
        get_session_dependencies()

    except Errors.DataBaseNotFound as ex:
        print "user db not found"
        dependencies_ok = False

    num_of_days_since_last_session = MainManager.user.last_visit.get_num_of_days_since_my_date()
    print "Num of days since last visit - {}".format(num_of_days_since_last_session)

    if num_of_days_since_last_session > Config.LAST_VISIT_MAX_DAYS_OK :
        print "user was not signed for too long"
        dependencies_ok = False

    try:
        if dependencies_ok:
            run_user_session()
        else:
            run_first_session()


    except Exception as ex:
        print "Exception! - {}".format(ex.message)
        raise ex

    finally:
        MainManager.finish_session()
