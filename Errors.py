
ERR_USER_ALREADY_EXISTS = "User Already Exists"
ERR_WEBSITE_UNRESPONSIVE = "Could Not Read Website"




class InvalidEmail(Exception):
    def __init__(self,char):
        self.message = "Email must contain '{}' .Please try again".format(char)

class InvalidUsernameError(Exception):
    def __init__(self,min_chars):
        self.message = "Username must be longer than {} letters.Please try again".format(min_chars)

class PasswordsDoNotMatch(Exception):
    def __init__(self):
        self.message = "Password do not match. Please try again"

class EmptyFieldError(Exception):
    def __init__(self,field_name):
        self.message = " {} - is empty. please fill it and try again".format(field_name)

class TorrentMagnetError(Exception):
    def __init__(self,torrent):
        self.message = "Error Downloading magnet for : {}".format(torrent.item_name)

class PirateBayError(Exception):
    def __init__(self,item):
        self.message = "Error searching for '{}' torrent".format(item.name)

class DataBaseNotFound(Exception):
    def __init__(self):
        self.message = "Data base not found"

class WebSiteDead(Exception):

    def __init__(self,url):
        self.message = "'{}' is dead".format(url)

class CouldNotUpdateShows(Exception):

    def __init__(self):
        self.message = "Could not update shows data base"

class ShowNotInDataBase(Exception):

    def __init__(self,show):
        self.message = "Could not find '{}' in data base".format(show)

class BadShowId(Exception):

    def __init__(self,sbowName):
        self.message = "Could not get show ID for '{}'".format(sbowName)

class TVDBError(Exception):

    def __init__(self):
        self.message = "Could not connect to database. Check internet connection"

class WebSiteUnresponsive(Exception):

    def __init__(self,url):
        self.message = "'{}' is dead".format(url)

class UserAlreadyExists(Exception):
    def __init__(self, username):
        self.message = "User '{}' Already Exists ".format(username)

class UserDoesnExist(Exception):
    def __init__(self, username):
        self.message = "User '{}' Doesnt Exist ".format(username)

class AlreadyFollowingSeries(Exception):
    def __init__(self, series_name):
        self.message = "you are already following '{}' ".format(series_name)

class InvalidPassword(Exception):
    def __init__(self,user_name):
        self.message = "password for user '{}' is incorrect".format(user_name)

# class TVDBError(Exception):
#     def __init__(self,show_name):
#         self.message = "Show '{}' not found in TVDB dataBase".format(show_name)

class MultiThreadingError(Exception):
    def __init__(self,ex,item):
        self.message = "Error with thread responsible for '{}'".format(ex,item)
