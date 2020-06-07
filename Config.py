import sys
import os
import getpass

USER_PATH = os.getcwd()
USER_NAME = getpass.getuser()

DB_FOLDER_NAME = "db"
ALL_SHOWS_FILE_PATH = os.path.join(USER_PATH,"All_Shows")
USERS_DATA_BASE_FILE_PATH = os.path.join(USER_PATH,DB_FOLDER_NAME,"UsersDataBase[pickle]")
SERIES_DATA_BASE_FILE_PATH = os.path.join(USER_PATH,DB_FOLDER_NAME, "SeriesDataBase[pickle]")

WEBSITES_TIMEOUT_IN_SECONDS = 7
LAST_VISIT_MAX_DAYS_OK = 3

class ConfigClass:

    def __init__(self):

        self.ONLY_HD_QUALITY_FLAG = True
        self.NUM_OF_TORRENTS_TO_FIND = 5
        self.NUM_OF_IN_SEEDERS = 5
