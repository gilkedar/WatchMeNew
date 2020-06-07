import urllib2
import requests
import os
import sys
import getpass
import datetime
import zipfile
import subprocess
import wx
import threading
import time
import emoji
from pytvdbapi import api
import webbrowser
import stat
import shutil
import dropbox
# from subprocess import Popen, PIPE
from Queue import Queue


MODE = 'ACTIVE'


"""
TO-DO

  -fix edit shows refresh
  -fix shutting down opening new window
  -fix duplicate windows
  -fix updateShowList Stuck multithreading
?-fix first apprearance
  - add delete button
  - fix add girls
  -scheduler since that day
  - you already have a scheduler
  - my shows folder button
- add retry button to utorrent move file
- silicon valley s04e10 subs bad !
- casual s0e08 subs stuck
  - create new branch!!
- house of cards season 5
  -upload whole session
- utorrent part file
- special requests
-slavins errors

  -yelow folder
  -hello gilke in center
-version updates
-fix permissions error
-fix shutdown_output_screen error
-fix organize shows (needs restart sometimes)
   -fix lock and print lock
   - fix shows like mr. robot
-- fix update issue
"""

# Configurations
APP_VERSION = "2.2"
USERNAME = getpass.getuser()
USER_PATH = os.getcwd()
APP_NAME = "WatchMe.exe"
SUB_LANGUAGES = ['english']
SHOW_FILE_LOCATION = USER_PATH + '/myShowList.txt'
SUBS_LOCATION = USER_PATH + '/Subs/'
LOG_PATH = USER_PATH + '/LogFile.txt'
PID_FILE_NAME = USER_PATH + '/pid.txt'
CLIENT_MSG_FILE_PATH = USER_PATH + "/supportMsg.txt"
LAST_SESSION_LOG_PATH = USER_PATH + '/LastSession.txt'
ADMIN_FILE_PATH = USER_PATH + '/Admin.txt'
HISTORY_PATH = USER_PATH + '/Download History.txt'
SUB_TMP_FILENAME = 'tempfile.zip'
BEST_SHOWS_FILE_PATH = USER_PATH + '/BestShows.txt'
ALL_SHOWS_FILE_PATH = USER_PATH + '/AllShows.txt'
USER_TERMS_AND_CONDITIONS_PATH = USER_PATH + "/Terms & Conditions.txt"
UTORRENT_ASSISTOR_FILE_NAME = "utorrent_assistor"
UTORRENT_EXE_FILE_PATH = 'C:\\users\\' + USERNAME + '\\AppData\\Roaming\\uTorrent\\utorrent.exe'
ORGANIZED_FOLDER_PATH = ''
NEW_DOWNLOADS_FOLDER_NAME = '--- New Downloads ---'
MOVIES_FOLDER_NAME = '--- Movies ---'
SUBS_FOLDER_NAME = '--- Subs ---'
DEFAULT_MY_SHOWS_FOLDER = 'C:\Users\%s\My Shows\\' % (USERNAME)
ICON_PATH ='magnet.ico'
FOLDER_IMAGE_NAME = "/yellow_folder.jpg"
EDIT_SHOWS_ICON_PATH = 'tvIcon.ico'
NUM_OF_SUB_FILES = 3
MIN_SEEDERS = 10
MAX_DAYS = 500
APP_SIZE = (380,500)
USER_DISPLAY_SIZE = None
OUTPUT_SCREEN_TITLE = "Eze Picho Shahaf"
UPCOMING_SHOWS_DEFUALT_DAYS = 7 #days
WEBSITES_TIMEOUT_IN_SECONDS = 10 #secs
MAX_QUEUE_THREADS = 10

HDR = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}

LAST_VISIT = ''
FILE_DATA = []
SHOWS_LIST_INPUT = []
MY_SHOWS = {}  # Global dictionary including the shows list and shows id
DATES = []  # Global list with all dates since last update
EPS_TO_DOWNLOAD_SINCE_UPDATE = {}  # Global list of all new episodes
REQUESTED_EPS_TO_DOWNLOAD = []
REQUESTED_SUBS_TO_DOWNLOAD = []
REQUESTED_SERIES_TO_DOWNLOAD = []
REQUESTED_MOVIES_TO_DOWNLOAD = []
TORRENTS_TO_DOWNLOAD_LST = []
TORRENTS_FILE_NAMES = {}
DOWNLOADED_SUBS = []
SUB_LINKS = []
ALREADY_HAVE_THESE_SUBS = []
SHOWS_NOT_FOUND = []
SUBS_NOT_FOUND = {}
EPS_NOT_FOUND = []
SEASONS_NOT_FOUND = []
MAGNETS_LIST = []
ALL_SHOWS = {}
LST_OF_FILES_TO_MOVE_LATER = []
UPCOMING_SHOWS = {}
START_TIME = ''
ONLY_HD_QUALITY_FLAG = True
ENABLE_SERIES_ORGANIZER = False
HAS_SCHEDULER = False
SCHEDULER_RUN_TIME = ""
FIRST_TIME = False
SHUTDOWN_OUTPUT_SCREEN = False
SPECIAL_REQUESTS_RUN = False
RUNTIME_ERRORS = []
BEST_SHOWS = {}
ADMIN_DIC = {}
GLOBAL_QUEUE_OF_THREADS = Queue()

UTORRENT_MOVE_TO_LOCATION = ''
UTORRENT_DOWNLOAD_LOCATION = ''
RELEASE_NAMES = ['dimension', 'fleet', 'immerse', 'avs', 'killers', 'deejayahmed','msd',
                 'megusta', 'psa', 'wifi', 'yify', 'fum', 'lol', 'turbo','publichd','subs'
                 'avs', 'shaanig', 'deflate','rmteam','skgtv', 'batv','belex', 'demand','nate']

TYPE_OPTIONS = ["   -- Type --","Series","Movie","Subtitles"]
SEASON_OPTIONS = [" -- Season --"]
EPISODE_OPTIONS = ["-- Episode --"]
TVDB_RESULT = None
SESSION_LOG_STR = ''
ALTERNATIVE_COMMANDS = ["install utorrent","update","password"]

TVDB_KEY = 'B43FF87DE395DF56'

# DROPBOX_ACCESS_TOKEN = '8Y39egp2gh0AAAAAAAARmhpEooR3O0E8zl-rDMfM-OYI9ihR5ry8uGlayg6rsfLn'
DROPBOX_ACCESS_TOKEN = 'DoxBuREoAUAAAAAAAAAABqakaDhUuLDlIJcCurfX4pzJ5QnjRcgqr0b3k7lYYc6w'
DROPBOX_LOG_FILES_FOLDER = '/User-Logs/'
DROPBOX_USER_MSGS_FOLDER = '/User-Msgs/'
DROPBOX_ADMIN_FILE = '/Admin/admin.txt'
DROPBOX_TERMS_AND_CONDITIONS_PATH = '/Admin/Terms & Conditions.txt'
CURRENT_APP_PASSWORD = ''
DROPBOX_WATCHME_INSTALL_FILE = "/Admin/installation"
LAST_SESSION_PID = ""


#is this the user's first time?
if not os.path.exists(HISTORY_PATH):
    FIRST_TIME = True



if not os.path.exists(SUBS_LOCATION):
    os.makedirs(SUBS_LOCATION)

    # if not os.path.exists(DEFAULT_MY_SHOWS_FOLDER):
    #     os.makedirs(DEFAULT_MY_SHOWS_FOLDER)
    # create subs location, first time only

# ---------------------------------------------------------------------------------------------------------------------
#
# def set_utorrent_download_locations(new_download_loc,new_move_to_loc):
#
#     if os.path.isfile(UTORRENT_FILE_PATH):
#         file_ob = open(UTORRENT_FILE_PATH, 'rb+')
#         data = file_ob.read().lower()
#         search_str1 = 'deviceslee19:'
#         search_str2 = 'dl_image_modified'
#         download_folder_index = data.find(search_str1) + len(search_str2)
#         added_txt = 'dir_active_download23:%s24:dir_active_download_flagi1e22:dir_completed_download22:%s:dir_completed_download_flagi1e22:' % (new_download_loc, new_move_to_loc)
#         download_folder_l_index = data.find(search_str2)
#         # data[download_folder_index :download_folder_l_index ]
#         # move_to_folder_index = data.find('download24:') + 11
#         # move_to_folder_l_index = data.find('27',move_to_folder_index)
#         # #data[move_to_folder_index + 11:move_to_folder_l_index] = new_move_to_loc
#         new_data = data[:download_folder_index] + added_txt +  data[download_folder_l_index:]
#         file_ob.seek(0)
#         file_ob.write(new_data)
#         file_ob.truncate()
#         file_ob.close()


def finals_actions_before_quit():

    write_session_to_lastSession_file()

    t = threading.Thread(target=frame.panel.dropBoxItem.upload_log_to_dropbox, args=(LAST_SESSION_LOG_PATH,))
    t.setDaemon(True)
    t.start()


def exception_routine(errMsg,errTitle="Error!",errSolution="Please Contact Support",errAction=""):
    global RUNTIME_ERRORS
    global SESSION_LOG_STR

    exc_type, exc_obj, exc_tb = sys.exc_info()
    line_number = []
    while exc_tb.tb_next:
        line_number.append(exc_tb.tb_lineno)
        exc_tb = exc_tb.tb_next
    line_number.append(exc_tb.tb_lineno)

    exception_log_msg = """\n\n***EXCEPTION***\n
Error Title   : {}
Exception Msg : {}
Error Message : {}
Error Solution: {}\n\n
Line Number   : {}
\n***************\n\n
""".format(errTitle,exc_obj,errMsg,errSolution,repr(line_number))

    SESSION_LOG_STR += exception_log_msg
    # write_session_to_lastSession_file()
    # error_thread = threading.Thread(target=frame.panel.dropBoxItem.upload_log_to_dropbox,args=LAST_SESSION_LOG_PATH)
    # error_thread.setDaemon(True)
    # error_thread.start()
    # sys.stderr

    if errAction == "exit":
        frame.panel.onError(errMsg + "\n" +errSolution,errTitle)

    elif errAction == "stop":
        prompt_user_with_error(errMsg + "\n" + errSolution,errTitle)

    elif errAction == "continue":
        prompt_user_with_message(errMsg + "\n" + errSolution,"FYI")

    else:
        #prompt_user_with_message(errMsg + errSolution,"FYI")
        err = "%s.  %s." % (errMsg,errSolution)
        RUNTIME_ERRORS.append(err)

    frame.panel.myEpisodesBtn.Enable()
    frame.panel.specialReqBtn.Enable()


def write_pid_to_file():
    global LAST_SESSION_PID

    try:
        if not os.path.exists(PID_FILE_NAME):
            file_ob = open(PID_FILE_NAME,'w+')
        else:
            file_ob = open(PID_FILE_NAME,'r+')
            LAST_SESSION_PID = file_ob.read().strip("\n")
            # os.kill(int(LAST_SESSION_PID))
            os.popen("TASKKILL /F /PID {}".format(LAST_SESSION_PID))
            file_ob.seek(0)
            file_ob.truncate()
        curr_pid = os.getpid()
        file_ob.write(str(curr_pid))
        file_ob.close()

        if HAS_SCHEDULER:
            create_scheduler_task()

    except Exception as ex:
        errTitle = ""
        errMsg = "There was an Error while shutting down other window by PID"
        errSolution = "I reccommend you shut down the programs and start again."
        errAction = "continue"
        exception_routine(errMsg, errTitle, errSolution, errAction)


def create_scheduler_task():

    now = datetime.datetime.today()
    now_str = str(now.hour) + ':' + str(now.minute) + ':' + str(now.second)
    runtime_str = SCHEDULER_RUN_TIME + ":00"
    FMT = '%H:%M:%S'
    tdelta = datetime.datetime.strptime(runtime_str, FMT) - datetime.datetime.strptime(now_str, FMT)
    delay = tdelta.seconds
    sched_thread = threading.Timer(delay, start_scheduler_routine)
    sched_thread.setDaemon(True)
    sched_thread.start()

def put_app_to_sleep():

    frame.panel.outPutTxtCtrl.Hide()
    if frame.panel.list_box:
        frame.panel.list_box.Hide()
    frame.Hide()

def wake_app():
    frame.Show()
    # frame.Raise()
    frame.panel.Show()
    frame.panel.outPutTxtCtrl.log.Clear()
    frame.panel.outPutTxtCtrl.Show()
    frame.panel.outPutTxtCtrl.Raise()
    SHUTDOWN_OUTPUT_SCREEN = False

    # frame.panel.outPutTxtCtrl.log.Clear()

def close_app_for_good():
    write_new_data_to_file('last_update')
    frame.panel.outPutTxtCtrl.Close()
    frame.panel.taksBarItem.RemoveIcon()
    frame.panel.taksBarItem.Destroy()
    # frame.panel.Close()
    # frame.panel.Destroy()
    # frame.Close()
    frame.Destroy()
    # sys.exit(1)
    return

def start_scheduler_routine():

    with lock:
        if read_webSite.first_thread_flag:
            return

        read_webSite.first_thread_flag = True
        if HAS_SCHEDULER:

            # wake_app()
            time.sleep(0.5)
            frame.panel.onDownloadEpisodes("Scheduler")
            time.sleep(1)
            create_scheduler_task()


def create_new_directories():
    try:

        if ENABLE_SERIES_ORGANIZER:
            if not os.path.exists(SUBS_LOCATION):
                os.makedirs(SUBS_LOCATION)
            if not os.path.exists(ORGANIZED_FOLDER_PATH + NEW_DOWNLOADS_FOLDER_NAME):
                os.makedirs(ORGANIZED_FOLDER_PATH + NEW_DOWNLOADS_FOLDER_NAME)
            if not os.path.exists(ORGANIZED_FOLDER_PATH + MOVIES_FOLDER_NAME):
                os.makedirs(ORGANIZED_FOLDER_PATH + MOVIES_FOLDER_NAME)
            if not os.path.exists(ORGANIZED_FOLDER_PATH + SUBS_FOLDER_NAME):
                os.makedirs(ORGANIZED_FOLDER_PATH + SUBS_FOLDER_NAME)

            for itemName, torrentName in TORRENTS_FILE_NAMES.items():
                itemName.replace("\'","")
                if 'season' in itemName:
                    if itemName[-7:] == 'season':
                        showName = itemName[:-11]
                    else:
                        showName = itemName[:itemName.rfind(" ")]
                        showName = showName[:showName.rfind(" ")]
                elif itemName[-1].isdigit():
                    showName = itemName[:itemName.rfind(" ")]
                else: #movie
                    showName = itemName
                    return

                itemPath = ORGANIZED_FOLDER_PATH + '\%s\\' % showName.title()
                if not os.path.exists(itemPath):
                    os.makedirs(itemPath)

    except Exception as ex:
        errTitle = ""
        errMsg = "There was an Error while creating new folders"
        errSolution = ""
        exception_routine(errMsg,errTitle,errSolution)


def get_item_name_from_video_file(fileName):
    try:

        words = fileName.lower().replace(' ','.').replace('-','.').split('.')
        if '720p' in words:
            idx = words.index('720p')
        elif '1080p' in words:
            idx = words.index('1080p')
        elif 'hdtv' in words:
            idx = words.index('hdtv')
        elif 'webrip' in words:
            idx = words.index('webrip')
        elif 'dvdrip' in words:
            idx = words.index('dvdrip')

        else:
            return fileName


        itemName = (' ').join(words[:idx])

        if 's0' not in itemName:
            return itemName

        if '201' in itemName:
            index = itemName.find("201")
            year = itemName[index:index+5]
            itemName = itemName.replace(year,'')

        while not itemName[-1].isdigit() :
            itemName = itemName[:itemName.rfind(' ')]

        if itemName == "":
            return fileName

        if "mr " in itemName:
            itemName = itemName.replace("mr ","mr. ")
        if "shameless us" in itemName:
            itemName = itemName.replace(" us","")

        return itemName

    except Exception as ex:
        errTitle = ""
        errMsg = "There was an Error while reading video files"
        errSolution = "Please contact support."
        errAction = "continue"
        exception_routine(errMsg,errTitle,errSolution,errAction)


def rename_existing_file(filePath):

    try:
        fileName = filePath[:-4]
        ending = filePath[-4:]
        counter = 1
        fileName += "(1)"
        while os.path.isfile(fileName + ending):
            fileName = fileName[:-4]
            counter += 1
            fileName +=" (%d)" % counter

        return fileName + ending

    except Exception as ex:
        errTitle = ""
        errMsg = "There was an Error while renaming existing files"
        errSolution = "Please contact support."
        errAction = "continue"
        exception_routine(errMsg,errTitle,errSolution,errAction)


def delete_file(path):
    try:
        os.chmod(path, stat.S_IWUSR)
        os.remove(path)

    except Exception as ex:
        errTitle = ""
        errMsg = "There was an Error while deleting files\n"
        errSolution = "Please contact support."
        errAction = "continue"
        exception_routine(errTitle,errMsg,errSolution,errAction)


def move_file_to_shows_folder(old_path,new_path,showName,fileName):
    global LST_OF_FILES_TO_MOVE_LATER

    orig_path = old_path[:old_path.rfind("\\")]
    try:
        if os.path.exists(ORGANIZED_FOLDER_PATH + showName + '\\'):
            new_path += showName + '\\'
        else: #movie
            new_path += MOVIES_FOLDER_NAME + "\\"
        new_path += fileName
        if os.path.isfile(new_path): # file already exists in path, delete it and move the new one
            delete_file(new_path)
            time.sleep(1)
            # new_path = rename_existing_file(new_path)
        os.rename(old_path, new_path)
        for tup in LST_OF_FILES_TO_MOVE_LATER:
            if fileName in tup[3]:
                LST_OF_FILES_TO_MOVE_LATER.remove(tup)


    except Exception as ex:
        tup = (old_path, new_path,showName,fileName)
        if tup not in LST_OF_FILES_TO_MOVE_LATER:
            LST_OF_FILES_TO_MOVE_LATER.append(tup)


def manage_shows_folder():
    global UTORRENT_DOWNLOAD_LOCATION
    global UTORRENT_MOVE_TO_LOCATION

    try:

        for root, dirs, files in os.walk(ORGANIZED_FOLDER_PATH + NEW_DOWNLOADS_FOLDER_NAME):
            files = [item.lower() for item in files]
            for fileName in files:
                if fileName.endswith('.mkv') or fileName.endswith(".avi") or fileName.endswith(".mp4") or fileName.endswith('.srt'):
                    release = get_release(fileName.lower()[:-4])
                    itemName = get_item_name_from_video_file(fileName)

                    itemName = itemName.replace("x264","")
                    itemName = itemName.replace("480p", "")

                    lastWord = itemName.split()[-1]
                    if len(lastWord) < 4: #wierd case
                        continue
                    if lastWord[0] == 's' and lastWord[3] == 'e': #episode
                        showName = itemName[:itemName.rfind(' ')].title()
                    else: #movie?
                        showName = itemName
                    ending = fileName[-4:]
                    new_file_name = change_to_proper_name(itemName,fileName,release,'.').title()
                    new_file_name += ending

                    if 'Sample' in new_file_name:
                        continue

                    new_file_path = ORGANIZED_FOLDER_PATH
                    old_file_path = root + "\\" + fileName
                    move_file_to_shows_folder(old_file_path,new_file_path,showName,new_file_name)
    except Exception as ex:
        errTitle = ""
        errMsg = "There was an Error while managing shows folder\n"
        errSolution = "Please contact support."
        errAction = "continue"
        exception_routine(errMsg, errTitle, errSolution, errAction)

def manage_subs_folder():

    for root, dirs, files in os.walk(ORGANIZED_FOLDER_PATH + SUBS_FOLDER_NAME):
        files = [item.lower() for item in files]
        for fileName in files:
            if fileName.endswith('.srt'):
                # release = get_release(fileName.lower()[:-4])
                itemName = get_item_name_from_video_file(fileName)
                release = get_release(fileName.lower()[:-4])
                if itemName == fileName:
                    delete_file(root + "\\" + fileName)

                if len(itemName.split()) > 1:
                    showName = itemName[:itemName.rfind(' ')]
                else:
                    showName = itemName

                ending = fileName[-4:]
                if " ( " in fileName:
                    new_file_name = fileName[:-4].title() + ending
                else:
                    new_file_name = change_to_proper_name(itemName,fileName,release,'.').title()
                    new_file_name += ending

                new_file_path = ORGANIZED_FOLDER_PATH
                old_file_path = root + "\\" + fileName
                move_file_to_shows_folder(old_file_path,new_file_path,showName,new_file_name)

def get_day_of_the_week(date):

    date_lst = date.split("-")
    year = date_lst[2]
    month = date_lst[1]
    day = date_lst[0]

    new_date = datetime.datetime.strptime('{} {}, {}'.format(month,day,year), '%b %d, %Y')
    weekday = new_date + datetime.timedelta(days=1) #when its available online
    return weekday.strftime('%A')

def print_upcoming_shows():

    print "\n\n" + "-" * 22 + " Upcoming Episodes " + "-" * 22 + "\n"

    if not UPCOMING_SHOWS:
        print "There are no new episodes coming soon.\n" \
              "Its time for a new Show :)\n"
    else:
        sorted_lst = sorted(UPCOMING_SHOWS, key=lambda x: datetime.datetime.strptime(UPCOMING_SHOWS[x], '%d-%b-%Y'))
        for key in sorted_lst:
            val = UPCOMING_SHOWS[key]
            day = get_day_of_the_week(val)
            name = key.title()
            line = "{}  ( {} )   -   {}".format(val, day, name)
            print line

    print "\n" + "-" * 66


def get_upcoming_shows(duration = UPCOMING_SHOWS_DEFUALT_DAYS):
    global EPS_TO_DOWNLOAD_SINCE_UPDATE
    global UPCOMING_SHOWS

    try:
        MONTHS = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        today = datetime.datetime.today()
        until = today + datetime.timedelta(days=duration)

        date_generated = [today + datetime.timedelta(days=x) for x in range(0, (until-today).days)]
        date_lst = []
        for day in date_generated:
            date_lst.append(str(day.day) + '-' + str(MONTHS[day.month]) + '-' + str(day.year))

        EPS_TO_DOWNLOAD_SINCE_UPDATE = {}
        multiThreading_routine(get_my_shows_since_update,date_lst)
        UPCOMING_SHOWS = dict(EPS_TO_DOWNLOAD_SINCE_UPDATE)
        EPS_TO_DOWNLOAD_SINCE_UPDATE = {}

    except Exception as ex:
        errTitle = "Error getting upcoming shows"
        errMsg = "There was an Error while getting upcoming shows folder.\n"
        errSolution = "Try again later."
        errAction = "continue"
        exception_routine(errMsg, errTitle, errSolution, errAction)

# def create_shortcut(src_folder_name, src_fileName,dst_folder_name,dst_fileName):
#     dst_new_fileName = dst_folder_name + dst_fileName + ".lnk"
#     path = dst_new_fileName
#     target = r"%s" % src_folder_name + src_fileName
#     wDir = r"%s" % src_folder_name
#     icon = target
#
#     shell = Dispatch('WScript.Shell')
#     shortcut = shell.CreateShortCut(path)
#     shortcut.Targetpath = target
#     shortcut.WorkingDirectory = wDir
#     shortcut.IconLocation = icon
#     shortcut.save()

#
# def move_seeding_files_shutdown_utorrent():
#     global RUNTIME_ERRORS
#     if not LST_OF_FILES_TO_MOVE_LATER:
#         return
#
#     msg = "I am trying to move files that you are seeding in Utorrent:\n\n" \
#           +"\n    *  ".join([tup[3] for tup in LST_OF_FILES_TO_MOVE_LATER]) + \
#           "\n\nDo you want me to close Utorrent for a second and re-open it?\n"\
#           "If not, click 'No' and I will try again next time:) "
#     try:
#         ans = prompt_user_with_question(msg,"Can't Relocate Files That are seeding in Utorrent" )
#         if ans:
#             os.system('TASKKILL /F /IM utorrent.exe')
#             time.sleep(1)
#             for tup in LST_OF_FILES_TO_MOVE_LATER:
#                 os.rename(tup[0], tup[1])
#                 EDITED_FOLDERS.append(tup[0])
#             time.sleep(1)
#             os.startfile('utorrent.exe')
#             prompt_user_with_message("Succesfuly moved all files", "Success!")
#         else:
#             return
#     except Exception as ex:
#         print ex.message
#         os.startfile('utorrent.exe')
#


def getFolderSize(folder):
    total_size = os.path.getsize(folder)
    for item in os.listdir(folder):
        itempath = os.path.join(folder, item)
        if os.path.isfile(itempath):
            total_size += os.path.getsize(itempath)
        elif os.path.isdir(itempath):
            total_size += os.path.getsize(itempath)
    return total_size


def remove_leftover_folders(path):

    for root, dirs, files in os.walk(path, topdown=False):
        try:

            for file in files:
                if file.endswith(".srt"):
                    continue
                fileSize = os.path.getsize(os.path.join(root,file))
                if fileSize > 10000000:
                    continue
                try:
                    if file in [item[3] for item in LST_OF_FILES_TO_MOVE_LATER]:
                        raise Exception("program shouldnt be here!")

                    filename = os.path.join(root, file)
                    os.chmod(filename, stat.S_IWUSR)
                    os.remove(filename)
                except Exception as ex:
                    errTitle = "Cant delete files"
                    errMsg = "I had a problem while deleting some leftover files.\n"
                    errSolution = "Try again later."
                    errAction = "continue"
                    exception_routine(errMsg, errTitle, errSolution, errAction)

            for dir in dirs:
                if getFolderSize(os.path.join(root, dir)) > 20000000:  # 20 mega - dont touch, still video in there
                    continue
                else:
                    shutil.rmtree(os.path.join(root, dir))
                #time.sleep(0.2)
        except Exception as ex:
            errTitle = ""
            errMsg = "There was an Error while removing leftover files.\n"
            errSolution = "Please contact support."
            errAction = "continue"
            exception_routine(errMsg, errTitle, errSolution, errAction)

# def remove_leftover_folders2():
#     global RUNTIME_ERRORS
#     for root, dirs, files in os.walk(ORGANIZED_FOLDER_PATH + NEW_DOWNLOADS_FOLDER_NAME, topdown=False):
#         if root in EDITED_FOLDERS or getFolderSize(root) < 5000000:
#             for name in files:
#                 try:
#                     filename = os.path.join(root, name)
#                     os.chmod(filename, stat.S_IWUSR)
#                     os.remove(filename)
#                 except Exception as ex:
#                     RUNTIME_ERRORS.append(ex)
#
#             for name in dirs:
#                 try:
#                     os.rmdir(os.path.join(root, name))
#                 except Exception as ex:
#                     RUNTIME_ERRORS.append(ex)
#
#



def prompt_user_with_question(msg,title):

    dlg = wx.MessageDialog(None, msg, title, wx.YES_NO | wx.ICON_QUESTION )
    dlg.Center()
    answer = dlg.ShowModal() == wx.ID_YES
    dlg.Destroy()
    return answer


def prompt_user_with_text_question(parent=None, message='', title="Answer Me!",default_value=''):
    try:
        dlg = wx.TextEntryDialog(parent, message,title, defaultValue=default_value)
        dlg.ShowModal()
        result = dlg.GetValue()
        dlg.Destroy()
        return result

    except Exception as ex:
        errTitle = "Internal Error"
        errMsg = "I wanted to ask you something but something happened.\n"
        errSolution = "Try again later."
        errAction = "continue"
        exception_routine(errMsg, errTitle, errSolution, errAction)

def prompt_user_with_error(msg, title = 'Error!',action = ''):
    global SHUTDOWN_OUTPUT_SCREEN

    errorDlg = wx.MessageDialog(None, msg, title, wx.OK | wx.ICON_WARNING )
    errorDlg.ShowModal()
    errorDlg.Center()
    errorDlg.Destroy()
    frame.panel.outPutTxtCtrl.log.Clear()
    frame.panel.outPutTxtCtrl.Hide()

    if action == 'exit':
        SHUTDOWN_OUTPUT_SCREEN = True
        sys.exit(1)

def prompt_user_with_message(msg, title = 'Hey There:)',action = ''):

    errorDlg = wx.MessageDialog(None, msg, title, wx.OK | wx.ICON_QUESTION  )
    errorDlg.ShowModal()
    errorDlg.Center()
    errorDlg.Destroy()

    if action == 'exit':
        sys.exit(1)

def prompt_user_with_retry_message(msg,title = 'Hey There:)', action = ''):
    pass


def get_list_of_relevant_shows(searchName):

    try:

        all_shows_file = open(ALL_SHOWS_FILE_PATH)
        shows = all_shows_file.readlines()
        all_shows_file.close()

        relevant_shows = []
        for show in shows:
            if searchName in show:
                show = show.strip('\n\\')
                relevant_shows.append(show)

        return relevant_shows

    except Exception as ex:
        errTitle = ""
        errMsg = "There was an Error while getting relevant shows"
        errSolution = "Please contact support."
        errAction = "continue"
        exception_routine(errMsg,errTitle,errSolution,errAction)

def read_best_shows_file():
    global BEST_SHOWS

    if not os.path.exists(BEST_SHOWS_FILE_PATH):
        msg = "Can't locate AllShows.txt\nPlease make sure file exists in running folder and run the app again."
        raise Exception(msg)

    # read myShowsFile
    file_ob = open(BEST_SHOWS_FILE_PATH, 'r')
    data = file_ob.readlines()
    file_ob.close()

    BEST_SHOWS.clear()
    for line in data:
        line = line.lower().strip('\n')
        details = line.split('::')
        if details[0] not in MY_SHOWS and line != '':
            BEST_SHOWS[details[0]] = details[1]

def read_show_file():
    global FILE_DATA
    global LAST_VISIT
    global SHOWS_LIST_INPUT
    global ORGANIZED_FOLDER_PATH
    global ENABLE_SERIES_ORGANIZER
    global SUBS_LOCATION
    global CURRENT_APP_PASSWORD
    global HAS_SCHEDULER
    global SCHEDULER_RUN_TIME
    global APP_VERSION

    # check if myShowFile exists in proper location
    if not os.path.exists(SHOW_FILE_LOCATION):
        msg = "Can't locate myShowFile.txt\nPlease make sure file exists in running folder"
        # prompt_user_with_message(msg,'exit')
        raise Exception(msg)

    # read myShowsFile
    file_ob = open(SHOW_FILE_LOCATION, 'r')
    FILE_DATA = file_ob.readlines()
    file_ob.close()

    LAST_VISIT = FILE_DATA[1][:-1]
    start_line = 0
    end_line = 0
    for lineNumber in range(2,len(FILE_DATA)): # get shows starting at dynamic line number
        if 'My Shows' in FILE_DATA[lineNumber]:
            start_line = lineNumber +1
            break
    for lineNumber in range(start_line, len(FILE_DATA)):  # get shows starting at dynamic line number
        if '---------' in FILE_DATA[lineNumber]:
            end_line = lineNumber
            break

    SHOWS_LIST_INPUT = FILE_DATA[start_line : end_line]

    for line in FILE_DATA[end_line+1:]:
        line = line.strip("\n")
        if 'Version' in line:
            APP_VERSION = line[line.find('"')+1:-1]
        if 'Enable shows organizer' in line:
            status = line[line.find('"')+1:-1]
            if status == 'True':
                ENABLE_SERIES_ORGANIZER = True
            else:
                ENABLE_SERIES_ORGANIZER = False
        elif 'Download Folder' in line:
            path = line[line.find('"')+1:-1]
            if FIRST_TIME and path == "":
                ORGANIZED_FOLDER_PATH = "C:\\users\\%s\\My Shows\\" % (USERNAME)
            else:
                ORGANIZED_FOLDER_PATH = path
        elif 'Password' in line:
            CURRENT_APP_PASSWORD = line[line.find('"')+1:-1]
        elif 'Scheduler' in line:
            status = line[line.find('"')+1:-1]
            if status == 'True':
                HAS_SCHEDULER = True
            else:
                HAS_SCHEDULER = False
        elif 'Run Time' in line:
            SCHEDULER_RUN_TIME = line[line.find('"') + 1 : -1]

    if ENABLE_SERIES_ORGANIZER:
        SUBS_LOCATION = ORGANIZED_FOLDER_PATH + SUBS_FOLDER_NAME + "\\"

def clear_parameters():
    global FILE_DATA
    global SHOWS_LIST_INPUT
    global DATES
    global EPS_TO_DOWNLOAD_SINCE_UPDATE
    global REQUESTED_EPS_TO_DOWNLOAD
    global REQUESTED_SUBS_TO_DOWNLOAD
    global REQUESTED_SERIES_TO_DOWNLOAD
    global REQUESTED_MOVIES_TO_DOWNLOAD
    global TORRENTS_TO_DOWNLOAD_LST
    global TORRENTS_FILE_NAMES
    global DOWNLOADED_SUBS
    global SUB_LINKS
    global SHOWS_NOT_FOUND
    global SUBS_NOT_FOUND
    global EPS_NOT_FOUND
    global SEASONS_NOT_FOUND
    global MAGNETS_LIST
    global START_TIME
    global END_TIME
    global ALREADY_HAVE_THESE_SUBS
    global RUNTIME_ERRORS
    global TYPE_OPTIONS
    global SEASON_OPTIONS
    global EPISODE_OPTIONS
    global SHUTDOWN_OUTPUT_SCREEN
    global GLOBAL_QUEUE_OF_THREADS
    global UPCOMING_SHOWS

    FILE_DATA = []
    SHOWS_LIST_INPUT = []
    DATES = []
    EPS_TO_DOWNLOAD_SINCE_UPDATE = {}
    REQUESTED_EPS_TO_DOWNLOAD = []
    REQUESTED_SUBS_TO_DOWNLOAD = []
    REQUESTED_SERIES_TO_DOWNLOAD = []
    REQUESTED_MOVIES_TO_DOWNLOAD = []
    TORRENTS_TO_DOWNLOAD_LST = []
    TORRENTS_FILE_NAMES = {}
    DOWNLOADED_SUBS = []
    SUB_LINKS = []
    ALREADY_HAVE_THESE_SUBS = []
    SHOWS_NOT_FOUND = []
    SUBS_NOT_FOUND = {}
    EPS_NOT_FOUND = []
    SEASONS_NOT_FOUND = []
    MAGNETS_LIST = []
    RUNTIME_ERRORS = []
    START_TIME = ''
    END_TIME = ''
    TYPE_OPTIONS = ["   -- Type --", "Series", "Movie", "Subtitles"]
    SEASON_OPTIONS = ["-- Season --"]
    EPISODE_OPTIONS = ["-- Episode --"]
    SHUTDOWN_OUTPUT_SCREEN = False
    GLOBAL_QUEUE_OF_THREADS = Queue()
    UPCOMING_SHOWS = {}

    read_webSite.first_thread_flag = False

def activateThreads():
    global GLOBAL_QUEUE_OF_THREADS

    try:
        while True:
            item = GLOBAL_QUEUE_OF_THREADS.get()
            download_exact_subtitles(item)
            GLOBAL_QUEUE_OF_THREADS.task_done()
    except Exception as ex:
        errTitle = "Internal Error"
        errMsg = "There was an Error while creating new threads.\n"
        errSolution = "Try again later. \n" \
                      "If error persists, please contact support."
        errAction = "stop"
        exception_routine(errMsg, errTitle, errSolution, errAction)

def MultiThreadingWithQueue(max_threads_num,func,relevant_lst):
    global GLOBAL_QUEUE_OF_THREADS

    new_items = []
    have_subs = [item[2] for item in SUB_LINKS]
    for showName in relevant_lst:
        if showName not in have_subs:
            new_items.append(showName)
    
    if not new_items:
        return

    # GLOBAL_QUEUE_OF_THREADS = Queue()

    try:
        if len(new_items) < max_threads_num:
            max_threads_num = len(new_items)
            
        for i in range(max_threads_num):
            t = threading.Thread(target=func)
            t.setDaemon(True)
            t.start()

        for item in new_items:
            GLOBAL_QUEUE_OF_THREADS.put(item)
            time.sleep(0.3)
        # time.sleep(0.5)

        GLOBAL_QUEUE_OF_THREADS.join()


    except Exception as ex:
        errTitle = "Internal Error"
        errMsg = "There was an Error while multi-threading with queue.\n"
        errSolution = "Try again later. \n" \
                      "If error persists, please contact support."
        errAction = "stop"
        exception_routine(errMsg, errTitle, errSolution, errAction)



#receives a function and a list of items to iterate to simplify the multithreading
def multiThreading_routine(func_name, relevant_list):
    global RUNTIME_ERRORS

    try:
        threads = [threading.Thread(target=func_name, args=(item,)) for item in relevant_list]
        for t in threads:
            t.setDaemon(True)
            t.start()
            if func_name is download_my_shows:
                time.sleep(0.3)
            elif func_name is get_subtitle_file:
                time.sleep(0.3)
            elif func_name is download_exact_subtitles:
                time.sleep(0.3)
        for t in threads:
            t.join()


        # except Exception as ex:
        #     errTitle = ""
        #     errMsg = "There was an Error while creating a new thread\n"
        #     errSolution = "Please contact support."
        #     errAction = "continue"
        #     exception_routine(errMsg, errTitle, errSolution, errAction)



    except Exception as ex:
        # if MODE == "DEBUG":
        #     print ex.message
        #
        errTitle = "Internal Error"
        errMsg = "There was an Error while running multiple threads.\n"
        errSolution = "Try again later. \n" \
                      "If error persists, please contact support."
        errAction = "stop"
        exception_routine(errMsg, errTitle, errSolution, errAction)

#update Download History Log
def add_session_to_history_file():

    try:

        history_file = open(HISTORY_PATH, 'a+')
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        history_file.write('\n\n' + '-'*31  + '  ' + str(nowTime) +'  ' + '-'*31 + '\n')

        for item in sorted(TORRENTS_FILE_NAMES.keys()):
            history_file.write("  -  " + item + '\n')

        history_file.write('-'*85 + '\n\n')
        history_file.close()
    except Exception as ex:
        errTitle = ""
        errMsg = "There was an Error while writing to history file"
        errSolution = "Please contact support."
        errAction = "continue"
        exception_routine(errMsg, errTitle, errSolution, errAction)


# def add_session_to_logFile():
#     log_file = open(LOG_PATH,'a+')
#     nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     log_file.write('-'*85 + '\n\n')
#     log_file.write('-'*31  + '  ' + str(nowTime) +'  ' + '-'*31 + '\n')
#
#     log_file.write(SESSION_LOG_STR)
#
#     log_file.close()

def write_session_to_lastSession_file():

    try:

        last_session = open(LAST_SESSION_LOG_PATH, 'w+')
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        last_session.write(str(nowTime))
        last_session.write("\n\n" + SESSION_LOG_STR)
        last_session.close()

    except Exception as ex:
        errTitle = "Error"
        errMsg = "There was an Error while writing to last session file"
        errSolution = "Please contact support."
        errAction = "continue"
        exception_routine(errMsg,errTitle,errSolution,errAction)

def first_time_screen():

    hello_str = "Hello " + USERNAME + " \n\n \
    I see this is your first time using WatchMe. Wise choice " + emoji.emojize(':wink:',use_aliases=True) + "\n\n \
    1) Do you have uTorrent or Tixati? \n \
    You Don't?? no worries:) \n \
    Click on 'More Options' at the top left corner of this screen \n \
    and then click on 'Install Utorrent'. \n\n \
    2) click \'Edit My Shows \' and add\\delete shows as you wish. \n \
    I put there some of my favorite shows just to get you started:) \n\n \
    3) Choose which date you want to start downloading shows from.\n\n \
    That's it, Your Ready! " + emoji.emojize(':smile:',use_aliases=True) + '   Click \'Download My Episodes\''

    "I also insist that you read our terms&conditions agreement: \n" \
    "The updated file is in your installation folder, 'terms&conditions.txt'"
    # 4) If you wish to download something specific, write it in the \n \
    # text box , choose type/season/episode and download special requests\n\n \
    return hello_str

#unused routine to raise and prompt errors
# def raise_error(error_message,error_action):
#     global RUNTIME_ERRORS
#     t_lock = threading.Lock()
#
#     if error_action is 'QUIT':
#         with t_lock:
#             err_event = SomeNewEvent(msg=error_message)
#             wx.PostEvent(frame.panel, err_event)
#             raise
#     elif error_action is 'APPEND':
#         with t_lock:
#             RUNTIME_ERRORS.append(error_message)

def check_user_permissions():
    global CURRENT_APP_PASSWORD

    try:
        if ADMIN_DIC['password'].lower() != CURRENT_APP_PASSWORD.lower():

            errMsg = "You do not have permissions to use this app!\n" \
                     "Type in the NEW password or go fish..."

            new_pass = prompt_user_with_text_question(message=errMsg, title="STOP!")
            if new_pass.lower() == ADMIN_DIC['password']:
                prompt_user_with_message("Correct:)\nPassword Updated Successfuly!",title= "Lucky you")
                CURRENT_APP_PASSWORD = ADMIN_DIC['password']
                write_new_data_to_file('last_update')
                return
            else:
                wrongPassErr = "Incorrect Password!\nPlease contact support"
                # prompt_user_with_error(wrongPassErr,"Go Fish!")
                frame.panel.onError(wrongPassErr,"Go Fish :\\")

    except Exception as ex:

        errTitle = "Sorry..."
        errMsg = "Error validating your password!\n"
        errSolution = "Please contact support."
        errAction = "exit"
        exception_routine(errMsg, errTitle, errSolution, errAction)


def read_webSite(url,timeout=WEBSITES_TIMEOUT_IN_SECONDS):
    global RUNTIME_ERRORS

    try:
        # start = time.time()
        time.sleep(0.1)
        req = requests.get(url, headers=HDR, verify=os.path.join('cacert.pem'),timeout=timeout)
        # end = time.time()
        # print "url: " + url
        # print "took: " + str(end-start)
        # print "\n"
        # raise Exception("Error test msg")

        if req.status_code == 404:
            return None
        if req.status_code == 409:
            return None

        return req


    except Exception as ex:
        with lock:
            if "next-episode" in url:
                return None

            if not read_webSite.first_thread_flag:
                read_webSite.first_thread_flag = True
                errTitle = ""
                errMsg = "Could not reach the necessary web sites :( "
                errSolution = "Make sure you are connected to the internet.\n\n" \
                              "Maybe one of the websites is down or unresponsive at the moment,\n" \
                              "so try again later."
                errAction = "stop"
                if "subscene" in url:
                    return None
                exception_routine(errMsg, errTitle, errSolution, errAction)
                return None
            else:
                return None


def read_tvdb_details(show):
    global TVDB_RESULT

    try:

        db = api.TVDB(TVDB_KEY)
        TVDB_RESULT = db.search(show, 'en')
        return True

    except Exception as ex:
        TVDB_RESULT = None
        errTitle = "TVDB Error!"
        errSolution = ''
        if show == "Error!":
            err_msg = "First Write down the name of the item you wish to download and press enter"
        elif "unable to connect" in ex[0].lower():
            err_msg = "There was an error getting the show's info\n"
            errSolution = "Make sure you are connected to the internet"
        else:
            err_msg = "The Show you entered does not exist!"
            errSolution = "Make sure the item name and the item type is correct :)"

        prompt_user_with_error(err_msg + errSolution,title=errTitle)
        frame.panel.typeChoice.SetSelection(0)
        return False

def get_release(fileName):
    global RUNTIME_ERRORS

    if fileName.endswith(".srt"):
        fileName = fileName[:-4]

    dash_idx = fileName.rfind('-')
    lastPart_idx = fileName.rfind('.')
    if lastPart_idx < 0:
        lastPart_idx = fileName.rfind("[")
    if lastPart_idx < 0:
        lastPart_idx = fileName.rfind("-")
    lastPart = fileName[lastPart_idx + 1: ]
    lastPart = lastPart.strip(' ')
    lastPart = lastPart.strip(']')
    # if lastPart[-1] == "]":

    try:
        if '-' in fileName or lastPart in RELEASE_NAMES:
            release = fileName[dash_idx + 1:]
            if lastPart in RELEASE_NAMES:
                return lastPart

            if release == "":
                return ""

            if release[0] == '.':
                release = release[1:]
            if release[0] == ' ':
                release = release[1:]
            if release[-1] == ' ':
                release = release[:-1]
            if '[' in release:
                release = release[:release.find('[')]
            if '.' in release:
                release = release[:release.find('.')]
            if ' ' in release:
                release = release[:release.find(' ')]
            if '-hi' in release:
                release = release[:release.find('-hi')]
            if release != 'dl':
                # if release not in RELEASE_NAMES:
                #     for possible_release in RELEASE_NAMES:
                #         if possible_release in fileName:
                #             return possible_release
                return release.lower()
        return ''

    except Exception as ex:
        # RUNTIME_ERRORS.append("Could not get release for '" + fileName )
        return ''


def show_utorrent_settings_instructions():

    # if not os.path.isfile(UTORRENT_EXE_FILE_PATH):
    #     raise Exception("Cant locate Utorrent. Install utorrent and try again.\n"
    #                     "You can install Utorrent by choosing 'More Options'\n"
    #                     "in the top lef corner of the main app screen \n"
    #                     "and then click 'Download Utorrent'\n")

    try:
        subprocess.Popen(['uTorrent.exe', UTORRENT_EXE_FILE_PATH])
    except BaseException as ex:
        errTitle = "Error Opening Utorrent"
        errMsg = "I had an error while opening utorrent for you.\n" \
                 "Are you sure utorrent is properly installed?\n\n" \
                 "If you are using a different torrent app,\n" \
                 "then follow the next instructions on your own client."
        errSolution = "I'm pretty sure you can handle it ;)\n\n" \
                      "If error persist,please contact support."
        errAction = "continue"
        exception_routine(errMsg, errTitle, errSolution, errAction)
    # if not os.path.isfile(UTORRENT_EXE_FILE_PATH):
    #     prompt_user_with_message("Could not locate assisting image\n"
    #                              "Im sure you will do just fine by your own:)","Oops..")
    # os.startfile(USER_PATH + "/{}_1.png".format(UTORRENT_ASSISTOR_FILE_NAME))
    # os.startfile(USER_PATH + "/{}_2.png".format(UTORRENT_ASSISTOR_FILE_NAME))

    ins_str = "    Its realy simple:)\n\n\
         I opened Utorrent for you, now let's reconfigure it: \n\n\
         1) Top left corner click 'Options' and then 'Preferences'\n \
        2) Choose 'Queuing' tab at the middle of the left panel \n \
        3) Under 'Seeding Goal' set all values to '0' \n \
        4) Also check the last checkbox 'Limit the upload rate'\n \
            and set the value again to '0'\n\n \
        5) Choose 'Directories' tab\n \
        6) check the 'Move completed downloads to:' checkbox, \n  \
           and paste the path below right under it\n\n \
   Click on 'OK' if you changed everything successfully\n"

        # *If you need assistance, there are 'utorrent_assistor'
    # 5) Choose 'Advanced' tab at the left panel \n \
    # 6) Scroll down to 'gui.default_del_action' \n \
    # 7) Set the value to '1' \n\n \
    #    Click 'OK' if you changed everything succesfuly"
    title = "YOU CAN DO IT ! "
    dlg = wx.TextEntryDialog(None,ins_str,title)
    dlg.SetValue("%s" % DEFAULT_MY_SHOWS_FOLDER + NEW_DOWNLOADS_FOLDER_NAME)
    dlg.Center()
    ans = dlg.ShowModal() == wx.ID_OK
    dlg.Destroy()

    return ans


#not used yet
# def get_utorrent_downloading_location():
#
#     if os.path.isfile(UTORRENT_SETTINGS_FILE_PATH):
#     if os.path.isfile(UTORRENT_SETTINGS_FILE_PATH):
#         Utorrent_file_ob = open(UTORRENT_SETTINGS_FILE_PATH, 'rb')
#         data = Utorrent_file_ob.read().lower()
#         download_folder_index = data.find('active_download23:')
#         download_folder_l_index = data.find('24:dir_active_download:', download_folder_index)
#         download_loc = data[download_folder_index + 12:download_folder_l_index + 1]
#         # move_to_folder_index = data.find('download24:')
#         # move_to_folder_l_index = data.find('27',move_to_folder_index)
#         # move_loc = data[move_to_folder_index+11:move_to_folder_l_index]
#         return (download_loc)
#     else:
#         return ('')

def check_if_has_valid_torrent_file(searchName,seriesName):

    try:
        url = 'https://thepiratebay.org/search/' + searchName + '/0/99/0'
        req = read_webSite(url)
        if req is None:
            return
        html = req.text.lower()
        parse_str = '<div class="detname">'  # parsing file to find 720P quality
        torrents_list = html.split(parse_str)
        good_torrents = 0

        for torrent_data in torrents_list[1:11]:
            end_of_name_data = torrent_data.find('</div>')
            name_data = torrent_data[:end_of_name_data - 5]
            torrent_name = name_data[name_data.rfind('>') + 1:].lower()
            num_of_seeders = torrent_data[torrent_data.find('<td align="right">') + 18 : torrent_data.find('</td>')]
            release = get_release(torrent_name)

            if num_of_seeders < MIN_SEEDERS:
                break
            if not check_if_item_is_valid(seriesName[:-7], torrent_name,'torrent'):
                continue

            magnet_index = torrent_data.find('magnet:')
            magnet_link = torrent_data[magnet_index: torrent_data.find('"', magnet_index + 7)]

            good_torrents += 1
            new_torrent_name = change_to_proper_name(seriesName[:-7], torrent_name, release,'.')
            TORRENTS_FILE_NAMES[seriesName] = new_torrent_name
            TORRENTS_TO_DOWNLOAD_LST.append(new_torrent_name)
            MAGNETS_LIST.append(magnet_link)
            return True

        return False

    except Exception as ex:
        errTitle = ""
        errMsg = "There was an error getting exact subtitle for " + searchName
        errSolution = "Try unchecking the HD-Only checkbox"
        errAction = "continue"
        exception_routine(errMsg, errTitle, errSolution, errAction)

def download_series_season(seriesName):
    global RUNTIME_ERRORS
    global REQUESTED_SUBS_TO_DOWNLOAD
    global TORRENTS_FILE_NAMES

    seriesName = seriesName
    initial_num = len(TORRENTS_TO_DOWNLOAD_LST)
    download_my_shows(seriesName)
    #check maybe better torrent with another name

    try:
        # if len(TORRENTS_TO_DOWNLOAD_LST) == initial_num:#didnt find with first name
        #trying to download another torrent either way, maybe better - user will choose!
        if seriesName[-9] == '0':
            otherName = seriesName[:-10] + 'season ' + seriesName[-8:-7]
        else:
            otherName = seriesName[:-10] + 'season ' + seriesName[-9:-7]
        download_my_shows(otherName)

        if len(TORRENTS_TO_DOWNLOAD_LST) == initial_num:#season probably still running
            initial_num = len(TORRENTS_TO_DOWNLOAD_LST)
            get_whole_season(seriesName)
            if len(TORRENTS_TO_DOWNLOAD_LST) == initial_num:
                SEASONS_NOT_FOUND.append(seriesName)

        if len(SUB_LINKS) == 0:
            episodes_lst = generate_lst_of_eps_in_season(seriesName,frame.panel.num_of_eps)
            torrentName = TORRENTS_TO_DOWNLOAD_LST[0]
            torrent_release = get_release(torrentName)

            for episode in episodes_lst:
                TORRENTS_FILE_NAMES[episode] = change_to_proper_name(episode,torrentName,torrent_release,'.')
                # if torrent_release != '':
                #     TORRENTS_FILE_NAMES["%s %s" %(episode, torrent_release)] = c
                # else:
                #     REQUESTED_SUBS_TO_DOWNLOAD.append("%s" %(episode))

            # torrents_names = [item + " %s" % torrent_release for item in episodes_lst ]
            # multiThreading_routine(download_exact_subtitles,episodes_lst)

        #except Exception as ex:
            #RUNTIME_ERRORS.append("Could not download season torrent, try again later.")
    except Exception as ex:
        errTitle = ""
        errMsg = "There was an error downloading the season"
        errSolution = "try to check/un-check the HD-Only checkbox and try again"
        errAction = "continue"
        exception_routine(errMsg, errTitle, errSolution, errAction)

def get_subtitle_file(sub_link):
    global RUNTIME_ERRORS
    global DOWNLOADED_SUBS
    global SUBS_LOCATION
    global SUB_DOWNLOAD_SHOWS_NOT_FOUND
    global ALREADY_HAVE_THESE_SUBS

    if SHUTDOWN_OUTPUT_SCREEN:
        return


    sub_url = sub_link[0]
    sub_name = sub_link[1]
    showName = sub_link[2]
    req = read_webSite(sub_url)
    if req is None:
        return
    html = req.text
    parse_str = '<a href=\"/subtitle/download'
    index = html.find(parse_str)
    end_index = html.find('\" rel=\"nofollow\" onclick')

    link = html[index + 9:end_index]
    domain = 'https://subscene.com'
    download_link = domain + link
    req2 = urllib2.Request(download_link, headers=HDR)
    try:
        webFile = urllib2.urlopen(req2)
    except Exception as ex:
        exception_routine("Could not download subs for : '" + showName + ".",
                          errSolution='Try again later')
        return
        #to prevent multiple file access
    with lock:
        try:
            show = showName[:showName.rfind(" ")]
            # if "season" in showName:
            #     show = show[:show.rfind(" ")]
            # if os.path.exists(ORGANIZED_FOLDER_PATH + '%s\\' % show):
            #     SUBS_LOCATION = ORGANIZED_FOLDER_PATH + '%s\\' % show.title()
            # else:
            #     SUBS_LOCATION = ORGANIZED_FOLDER_PATH + '%s\\' % SUBS_FOLDER_NAME
            tempzip = open(SUBS_LOCATION + str(get_subtitle_file.counter) + SUB_TMP_FILENAME, "wb+")
            tempzip.write(webFile.read())
            tempzip.close()
            zf = zipfile.ZipFile(SUBS_LOCATION + str(get_subtitle_file.counter) + SUB_TMP_FILENAME)
            subFileName = zf.NameToInfo.keys()[0]
            subRelease = get_release(subFileName)

            if sub_name not in DOWNLOADED_SUBS:  # no duplicates
                #extract whole season
                if 'season' in showName:
                    if not os.path.exists(SUBS_LOCATION + '//' + sub_name):
                        os.makedirs(SUBS_LOCATION + '//' + sub_name)
                        zf.extractall(SUBS_LOCATION + '//' + sub_name)
                        DOWNLOADED_SUBS.append(sub_name)
                    else:
                        ALREADY_HAVE_THESE_SUBS.append(sub_name)

                else:
                    # extract only the one correct sub
                    for member in zf.infolist():
                        if subRelease in member.filename.lower():
                            if not os.path.exists(SUBS_LOCATION + sub_name + '.srt'):
                                member.filename = str(sub_name + '.srt').title()
                                # time.sleep(0.1)
                                zf.extract(member,SUBS_LOCATION)
                                DOWNLOADED_SUBS.append(sub_name)
                                break
                            else:
                                ALREADY_HAVE_THESE_SUBS.append(sub_name)
                                break

            zf.close()
            if os.path.isfile(SUBS_LOCATION + str(get_subtitle_file.counter) + SUB_TMP_FILENAME):
                delete_file(SUBS_LOCATION + str(get_subtitle_file.counter) + SUB_TMP_FILENAME)
            get_subtitle_file.counter += 1

        except Exception as ex:
            with lock:
                if not get_subtitle_file.first_thread_flag:
                    get_subtitle_file.first_thread_flag = True

                    RUNTIME_ERRORS.append("Could not download subtitles for '" + showName + ".")
                    errTitle = "Error Downloading subtitle file"
                    errMsg = "There was an Error while Downloading subs for :\n {}\n".format(showName)
                    errSolution = "Try again later. \n" \
                                  "If error persists, please contact support."
                    errAction = "continue"
                    exception_routine(errMsg, errTitle, errSolution, errAction)

def get_subscene_alternative_name(show):

    SEASON_NUM = ['', 'first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth',
                  'eleventh', 'twelfth', 'thirteenth', 'fourteenth', 'fifteenth', 'sixteenth', 'seventeenth','eighteenth',
                  'nineteenth', 'twentieth']

    if show in REQUESTED_MOVIES_TO_DOWNLOAD:
        return "the " + show

    show_details = show.split(' ')

    if show_details[-1] == 'season': # series s0X season
        showName = " ".join(show_details[:-2])
        seasonNum = show_details[-2]
        otherName = ''
        if show[-9] == '0':
            otherName = show[:-10] + 'season ' + show[-8:-7]
        else:
            otherName = show[:-10] + 'season ' + show[-9:-7]
        return otherName

    elif show_details[-2] == 'season': # series season X
        seasonNum = show_details[-1]
        otherName = ''
        if len(seasonNum) == 1:
            otherName = show[:-8] + 's0' + show[-1] + ' season'
        else:
            otherName = show[:-9] + 's' + show[-2:] + ' season'
        return otherName

    else:
        showName = show_details[:-1]
        episode = show_details[-1]

    if episode.isdigit():
        season = SEASON_NUM[int(episode)]
    else:
        season = SEASON_NUM[int(episode[1:3])]

    subscene_name = ''
    for word in showName:
        subscene_name = subscene_name + word + '-'
    subscene_name = subscene_name + season + '-' + 'season'

    if 'shameless' in subscene_name: #annoying patch
        subscene_name = 'shameless-us-' + season +'-season'

    return subscene_name


def download_exact_subtitles(showName):
    global SUB_LINKS
    global SUBS_NOT_FOUND
    global lock

    if SHUTDOWN_OUTPUT_SCREEN:
        return

    try:

        if showName in [item[2] for item in SUB_LINKS]:
            return

        with lock:
            searchName = showName
            if 'season' in showName:
                # if showName[-8:-2] == 'season':
                #     searchName = showName[:-8] + 's0' + showName[-1] + ' season'
                return# patch to not download whole seasons subs


            for lang in SUB_LANGUAGES:
                torrentName = showName
                if showName not in REQUESTED_SUBS_TO_DOWNLOAD:
                    if showName not in TORRENTS_FILE_NAMES.keys():
                        # if 'season' in frame.panel.searchRelease:
                        torrentName = TORRENTS_FILE_NAMES[frame.panel.searchString]
                    else:
                        torrentName = TORRENTS_FILE_NAMES[showName]
                torrentRelease = showName.split()[-1]
                if showName not in REQUESTED_SUBS_TO_DOWNLOAD:
                    torrentRelease = get_release(torrentName)

                if showName in REQUESTED_SUBS_TO_DOWNLOAD:
                    searchName = frame.panel.searchString # to remove subs
                    showName = searchName

                # if torrentRelease in RELEASE_NAMES:
                #     if showName not in REQUESTED_SUBS_TO_DOWNLOAD:
                #         searchName += " " #     + torrentRelease (kills searches)
                url = 'https://subscene.com/subtitles/release?q=' + searchName + '/' + lang

                req = read_webSite(url)
                if req is None:
                    return
                html = req.text.lower()
                parse_str = 'class=\"a1\"'
                subs = html.split(parse_str)
                domain = 'https://subscene.com'

                if len(subs) <= 2:
                    if showName in REQUESTED_MOVIES_TO_DOWNLOAD:
                        if len(subs) < 5:
                            subs = get_subs_url_for_movie(subs[0], showName, lang)
                            if not subs:
                                return
                    else:
                        return

                added_to_download_lst = 0
                counter = 0
                tmp_release_names = []
                tempSubLinks = []


                search_for_specific_release = 0
                if torrentRelease in RELEASE_NAMES:
                    search_for_specific_release = 1

                elif torrentRelease != '':
                    search_for_specific_release = 1

                for sub_link in subs[1:]:
                    idxStart = sub_link.find('<span>')
                    idxEnd = sub_link.find('</span>', idxStart)
                    subName = sub_link[idxStart + 14: idxEnd - 7]

                    # check if torrent its 720p and fits the show. if not, skip
                    if not check_if_item_is_valid(showName,subName,'sub'):
                       continue


                    #create the sub url
                    initial_index = sub_link.find("href=\"") + 6
                    final_index = sub_link.find("\">")
                    url_addition = sub_link[initial_index:final_index]
                    sub_url = domain + url_addition
                    if lang not in sub_url:
                        continue

                    release = get_release(subName)

                    # found perfect match
                    if release != '' and release in torrentRelease:
                        newSubName = change_to_proper_name(showName,subName,release,'.')
                        SUB_LINKS.append([sub_url, newSubName,showName])
                        return

                    # skip same releases
                    if release in tmp_release_names:
                        continue

                    if release != '':
                        tmp_release_names.append(release)

                    #add to temporary possible links list
                    counter += 1
                    number_str = ' ( ' + str(len(tempSubLinks)+ 1) + ' ) '
                    newSubName = change_to_proper_name(showName,subName,release, number_str)
                    tempSubLinks.append([sub_url, newSubName,showName])
                    added_to_download_lst = 1
                    if search_for_specific_release == 0 and counter == NUM_OF_SUB_FILES:
                        break

                if added_to_download_lst == 1:
                    for item in tempSubLinks[:NUM_OF_SUB_FILES]:
                        SUB_LINKS.append(item)
                else:
                    if "season" not in showName:
                        SUBS_NOT_FOUND[showName] = torrentName

    except Exception as ex:
        errTitle = "Error searching for subtitles"
        errMsg = "There was an Error while searching for new subs.\n"
        errSolution = "Maybe the site is down,\n" \
                      "Try again later. \n" \
                      "If error persists, please contact support."
        errAction = "continue"
        exception_routine(errMsg, errTitle, errSolution, errAction)

def open_magnet(magnet_link):
    global RUNTIME_ERRORS
    try:

        if SHUTDOWN_OUTPUT_SCREEN:
            return

        if os.name == 'nt':  # Windows
            os.startfile(magnet_link)
        elif os.uname()[0] == 'Linux':  # Linux
            subprocess.call(["xdg-open", magnet_link])
        else:  # Don't know what you are, hope the OS can open a magnet URL!
            os.startfile(magnet_link)

    except:
        RUNTIME_ERRORS.append("Can't open the torrents. Make sure you have uTorrent installed and try again")

#update myShowFile with added shows, ID, and date
def write_new_data_to_file(date =''):
    global ORGANIZED_FOLDER_PATH

    file_ob = open(SHOW_FILE_LOCATION, 'w')
    new_date = datetime.datetime.today()
    date_str = str(new_date.day) + '-' + str(new_date.month) + '-' + str(new_date.year) + '\n'
    if date == 'last_update':
        date_str = LAST_VISIT + '\n'
    file_ob.write("-------------- Last Update -------------\n")
    file_ob.write(date_str)
    file_ob.write("----------------------------------------\n")
    #file_ob.write("*I will download every episode released \
    #              \nsince that date, and update it \
    #              \nautomatically every time you run me\n")
    file_ob.write("\n\n")
    file_ob.write("-------------- My Shows List -----------\n")
    for show, id in MY_SHOWS.items():
        if id == -1:
            continue
        file_ob.write(show.title() + '::' + str(id) + '\n')
    for bad_show in SHOWS_NOT_FOUND:
        file_ob.write(bad_show.title() + '::' + str(-1) + '\n')
    file_ob.write("----------------------------------------\n\n")

    file_ob.write("\nVersion: \"%s\"" % APP_VERSION)
    file_ob.write("\nEnable shows organizer: \"%s\"" % ENABLE_SERIES_ORGANIZER)
    if ORGANIZED_FOLDER_PATH == "":
        ORGANIZED_FOLDER_PATH = DEFAULT_MY_SHOWS_FOLDER
    file_ob.write("\nDownload Folder: \"%s\"" % ORGANIZED_FOLDER_PATH)
    file_ob.write("\nPassword: \"%s\"" % CURRENT_APP_PASSWORD)
    file_ob.write("\nScheduler: \"%s\"" % HAS_SCHEDULER)
    file_ob.write("\nTask Run Time: \"%s\"" % SCHEDULER_RUN_TIME)

def create_my_show_list(line):
    global RUNTIME_ERRORS
    global MY_SHOWS

    try:
        newline = line.replace('\n', '')  # delete the '/n' character
        details = newline.split('::')
        name = details[0].lower()
        if len(details) > 1:
            if details[1] == None:
                MY_SHOWS[name] = get_show_id(name)
            MY_SHOWS[name] = details[1]
        elif name != '' and '----' not in name:
            MY_SHOWS[name] = get_show_id(name)


    except Exception as ex:
        RUNTIME_ERRORS.append("Error while reading myShowList file.Make sure file is written properly")
        return False


#get myepisodes ID for quicker access after first time
def get_show_id(showName):
    global SHOWS_NOT_FOUND

    firstLetter = showName[0]
    firstWord = showName.split()[0]
    if firstWord == 'the':
        firstLetter = showName[4]
    url = 'https://myepisodes.com/shows/' + firstLetter.capitalize()
    data = ''
    try:
        data = urllib2.urlopen(url).read().lower()
    except Exception as ex:
        errTitle = ""
        errMsg = "I had an error while getting the show's ID.\n"
        errSolution = "Please try again later.\nIf error persists, contact support."
        errAction = "continue"
        exception_routine(errMsg, errTitle, errSolution, errAction)

    index = data.find('/' + showName)
    last_index = data.find('\"', index)
    show = data[index + 1:last_index]
    counter = 5
    while show != showName:
        index = data.find('/' + showName, last_index)
        last_index = data.find('\"', index)
        show = data[index + 1:last_index]
        if counter == 0:
            SHOWS_NOT_FOUND.append(showName)
            return -1
        counter -= 1
    show_details = data[index - 20:index]
    show_id = show_details[show_details.find('epsbyshow/') + 10:]
    return show_id


def get_list_of_dates(since):

    try:
        MONTHS = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        today = datetime.datetime.today() - datetime.timedelta(hours=7)
        start = datetime.datetime.strptime(since, "%d-%m-%Y")

        if (today - start).days < -1 :
            raise Exception("I cant predict the future!\nChoose a proper date and run again")
        if (today-start).days > MAX_DAYS:
            raise Exception("You went too far back....\nI cant go back 3 years!"
                            "\nChoose a proper date and try again.")

        date_generated = [start + datetime.timedelta(days=x) for x in range(0, (today - start).days)]
        date_lst = []
        for day in date_generated:
            date_lst.append(str(day.day) + '-' + str(MONTHS[day.month]) + '-' + str(day.year))
        if len(date_lst) == 0:
            yesterday = today - datetime.timedelta(1)
            yest = str(yesterday.day) + '-' + str(MONTHS[yesterday.month]) + '-' + str(yesterday.year)
            date_lst.append(yest)
        return date_lst

    except Exception as ex:
        if "I cant" in ex.message:
            prompt_user_with_error(ex.message, "Bad Date")

        else:
            errTitle = "Bad Date"
            errMsg = "There was an error generating the list of dates"
            errSolution = "Please contact support"
            errAction = "stop"
            exception_routine(errMsg, errTitle, errSolution, errAction)

        return []

def update_all_shows_dic_and_file():

    try:
        #delete all content
        today = datetime.datetime.today() - datetime.timedelta(hours=10)
        file_ob = open(ALL_SHOWS_FILE_PATH, 'w')
        file_ob.write("Last Update: " + str(today)[:-6] + "\n\n")
        file_ob.close()

        string = "#abcdefghijklmnopqrstuvwxyz"
        # for ch in string:
        #     get_all_shows_by_letter_and_write_to_file_and_dic(ch)
        for letter in string:
            get_all_shows_by_letter_and_write_to_file_and_dic(letter)

        time.sleep(1)
        print "\nNow i know my ABC's, next time won't you sing with me :D"
        time.sleep(1)
        print "\nUpdate finished. Enjoy"

    except Exception as ex:
        errTitle = ""
        errMsg = "There was an error updating all-shows data base "
        errSolution = "Please try again later"
        errAction = "continue"
        exception_routine(errMsg, errTitle, errSolution, errAction)


def get_all_shows_by_letter_and_write_to_file_and_dic(letter):
    global ALL_SHOWS

    try:
        if letter != '#':
            print letter
        url = 'https://myepisodes.com/shows/' + letter.capitalize()

        data = urllib2.urlopen(url).read().lower()
        parse_str = "</a></td>"
        shows_lst_data = data.split(parse_str)

        file_ob = open(ALL_SHOWS_FILE_PATH, 'a')

        for item in shows_lst_data[:-1]:
            show = item[item.rfind("\">") + 2:]
            file_ob.write(show.lower() + '\n')

        file_ob.close()

    except Exception as ex:
        errTitle = ""
        errMsg = "Could not update show list"
        errSolution = "Make sure you are properly connceted to the internet.\n" \
                      "If you are, then please try again later"
        errAction = "continue"
        exception_routine(errMsg, errTitle, errSolution, errAction)

# def get_all_shows_id():
#     pass


def get_my_shows_since_update(date):
    global EPS_TO_DOWNLOAD_SINCE_UPDATE

    try:

        str = 'longnumber\">'
        #data = urllib2.urlopen("https://www.myepisodes.com/epsbydate/" + date).read().lower()
        url = "https://www.myepisodes.com/epsbydate/" + date
        req = read_webSite(url)
        if req is None:
            return False
        data = req.text.lower()
        for show, id in MY_SHOWS.items():
            if id == -1:  # if show was not found
                continue
            show_index = data.find(show)
            while show_index != -1:
                id_index_start = data.find("/",show_index-10) + 1
                id_index_end = data.find("/", id_index_start+1)
                show_id_on_site = data[id_index_start:id_index_end]
                episode_number = data.find(str, id_index_start)
                showName = show + ' ' + data[episode_number + 12:episode_number + 18]
                if showName[-6] != 's':
                    break
                if show_id_on_site == id:
                    EPS_TO_DOWNLOAD_SINCE_UPDATE[showName.lower()] = date
                show_index = data.find(show, show_index + len(show) + 10)

    except Exception as ex:
        errTitle = ""
        errMsg = "Error getting list of new shows"
        errSolution = "Make sure you are connected to the internet"
        errAction = "continue"
        exception_routine(errMsg, errTitle, errSolution, errAction)


def get_latest_episode_number(seriesName):
    global RUNTIME_ERRORS
    try:
        series_name = seriesName.split(" season")[0]
        series_name = series_name.replace(' ', '-')
        series_name = series_name.replace("'",'')
        url = 'http://next-episode.net/' + series_name
        req = read_webSite(url,2)
        if req is None:
            return 0
        html = req.text.lower()
        parse_str = "episode:</div><div class=\"sub_main\">"
        # myFile = open("file.txt","w+")
        # myFile.write(html)
        idx = html.find(parse_str)
        new_idx = html.find(parse_str,idx + 1)
        end_idx = html.find('</div></div>', new_idx)
        latest_episode_number = html[new_idx  + len(parse_str): end_idx ]
        season_number_parser = '<div class="subheadline"><h3>season:</h3></div>'
        season_number_idx = html.find(season_number_parser)
        season_end_idx = html.find('\t\t\t<div></div>', season_number_idx)
        season_number = html[season_number_idx + 47: season_end_idx]
        if season_number in seriesName[-3:]:
            return  int(latest_episode_number)
        else:
            return 0

    except Exception as ex:
        return 0

def get_latest_season_number(seriesName):
    global RUNTIME_ERRORS
    try:
        seriesName = seriesName.replace(" ", "-")
        url = 'http://next-episode.net/' + seriesName
        req = read_webSite(url)
        html = req.text.lower()
        parse_str = 'episode:</div><div style="display:inline-block;width:260px;margin-left:90px;">'
        idx = html.find(parse_str)
        end_idx = html.find('</div></div>', idx)
        latest_episode_number = html[idx + 78: end_idx]
        season_number_parser = '<div class="subheadline"><h3>season:</h3></div>'
        season_number_idx = html.find(season_number_parser)
        season_end_idx = html.find('\t\t\t<div></div>', season_number_idx)
        season_number = html[season_number_idx + 47: season_end_idx]
        if season_number.isdigit():
            return int(season_number)
        else:
            return 0

    except Exception as ex:
        return 0

def generate_lst_of_eps_in_season(series_to_download,max_episode_number):
    global REQUESTED_EPS_TO_DOWNLOAD

    episodes_lst = []
    NUM_ARR = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14',
               '15', '16', '17', '18','19', '20', '21', '22', '23', '24','25']


    if series_to_download[-1].isdigit():
        seasonNum = int(series_to_download[-2:].strip(" ")) - 1
        seriesName = series_to_download.split(" season")[0]
    else:
        seasonNum = int(series_to_download[-8:-7]) - 1
        seriesName = series_to_download[:-11]
    for episode_number in range(max_episode_number):
        episode_name =seriesName + " s" + NUM_ARR[seasonNum]+ 'e' + NUM_ARR[episode_number]
        episodes_lst.append(episode_name.lower())
        REQUESTED_EPS_TO_DOWNLOAD.append(episode_name)

    return episodes_lst


def get_whole_season(series_to_download):
    global TORRENTS_FILE_NAMES
    global MAGNETS_LIST
    global TORRENTS_TO_DOWNLOAD_LST
    global SEASONS_NOT_FOUND

    try:
        max_episode_number = get_latest_episode_number(series_to_download)
        if max_episode_number < frame.panel.num_of_eps:
            max_episode_number = frame.panel.num_of_eps
        episodes_lst = generate_lst_of_eps_in_season(frame.panel.searchString,max_episode_number)

        multiThreading_routine(download_my_shows, episodes_lst)

    except Exception as ex:
        errTitle = ""
        errMsg = "Could not download the season : {}".format(series_to_download)
        errSolution = "Please try again later"
        errAction = "continue"
        exception_routine(errMsg, errTitle, errSolution, errAction)


def change_to_proper_name(show,itemName,release,number):

    itemName  = itemName.replace(' ', '.')
    wordsInShow = show.split()
    newName = '.'.join(wordsInShow)

    if ".." in newName: #fix for mr. robot like shows
        newName = newName.replace("..",".")

    if release == "":
        release = 'zibi'

    if number != '.':
        newName += ".720p" + number + ' - ' + release

    else:
        if '720p' in itemName:
            newName += number + '720p' + ' - ' + release
        elif 'hdtv' in itemName:
            newName += number + 'hdtv' + ' - ' + release
        elif 'webrip' in itemName:
            newName += number + 'webrip' + ' - ' + release

        elif '1080p' in itemName:
            newName += number + '1080p' + ' - ' + release

        else:
            newName += number + '720p' + ' - ' + release #patch to make it look good :(


    if "." == newName[-1]:
        newName = newName[:-1]
    if '.' == newName[0]:
        newName = newName[1:]
    if len(newName) > 70:
        newName = newName[:70]

    return newName



def check_if_item_is_valid(name,itemName,item):
    ok = 1
    words = name.split(' ')
    words = [word.strip(".") for word in words]# shows like mr. robot
    itemWords  = itemName.split('.')

    if len(itemWords) < 4:
        itemWords = itemName.split(' ')

    if words[0] != itemWords[0]:
        if "hbo" not in itemWords[0]:
                return False

    # if words[1] != itemWords[1]:   # too strict for now
    #     if not itemWords[-2:].isalnum():
    #         return False

    for word in words:
        if '(' in word:
            continue
        if '.' in word:
            word = word.strip('.')
        if word == 'season':
            seasonNum = ''
            if "season" == words[-1]:
                seasonNum = words[-2]
                if seasonNum + " " in itemName:
                    continue
                elif seasonNum + "." in itemName:
                    continue
            else:
                seasonNum = name[name.find("season")+7:]
                if "season" in itemName:
                    if seasonNum in itemName[itemName.find("season")+7:itemName.find("season")+ 9]:
                        break
                if len(seasonNum) == 1:
                    seasonNum = "0" + seasonNum
                if "s" + seasonNum in itemName:
                    if seasonNum in itemName[itemName.find("s" + seasonNum): itemName.find("s" + seasonNum) + 6]:
                        break
                else:
                    return False

        if word not in itemName:
            ok = 0
            break

    if ok == 0:
        return False
    elif '720p' not in itemName and ONLY_HD_QUALITY_FLAG: #and item != 'sub':
        if '1080p' not in itemName and ONLY_HD_QUALITY_FLAG:
            return False
        else:
            return True
    else:
        return True


def get_subs_url_for_movie(subs,movieName,lang):

    spliter = '<h2 class="popular">popular</h2>'
    subs_options = subs.split(spliter)
    popular_subs = subs_options[1]
    spliter_2 = '<a href='
    idxStart = popular_subs.find(spliter_2)
    idxEnd = popular_subs.find('>', idxStart)
    url_addition = popular_subs[idxStart + 10: idxEnd - 1]

    url =  'https://subscene.com/' + url_addition + "/" + lang
    req = read_webSite(url)

    if req is None:
        return False

    html = req.text.lower()
    parse_str = 'class=\"a1\"'
    subs = html.split(parse_str)

    if len(subs) <= 2:
        return False
    else:
        return subs

def check_if_torrent_has_exact_subtitles(showName,torrentRelease,searchName=""):
    global SUB_LINKS

    if SHUTDOWN_OUTPUT_SCREEN:
        return

    try:

        releaseQhdr =""
        if searchName == "" or showName[-7:] == 'season':
            releaseQhdr = 'release?q='
            searchName = showName
        lang = 'english'
        url = 'https://subscene.com/subtitles/' + releaseQhdr + searchName + '/' + lang
        # if showName in REQUESTED_MOVIES_TO_DOWNLOAD:
        #     movieName = searchName.replace(' ', '-')
        #     url = 'https://subscene.com/subtitles/' + movieName + '/' + lang
        # if showName[-8:-2] == 'season':
        #     showName = showName[:-8] + ' s0' + showName[-1] + ' season'

        req = read_webSite(url)

        if req is None:
            return



        html = req.text.lower()
        parse_str = 'class=\"a1\"'
        subs = html.split(parse_str)

        if len(subs) <= 2:
            if showName in REQUESTED_MOVIES_TO_DOWNLOAD:
                if len(subs) < 5:
                    subs = get_subs_url_for_movie(subs[0],showName,lang)
                    if not subs:
                        return False
            else:
                return False

        for sub_link in subs[1:]:
            idxStart = sub_link.find('<span>')
            idxEnd = sub_link.find('</span>', idxStart)
            subName = sub_link[idxStart + 14: idxEnd - 7]

            release = get_release(subName)
            # check if torrent its 720p and fits the show. if not, skip
            if release != '':
                if release in torrentRelease:
                    if lang in sub_link:
                        if check_if_item_is_valid(showName, subName, 'sub'):
                            domain = 'https://subscene.com'
                            initial_index = sub_link.find("href=\"") + 6
                            final_index = sub_link.find("\">")
                            url_addition = sub_link[initial_index:final_index]
                            sub_url = domain + url_addition
                            newSubName = change_to_proper_name(showName, subName, release, '.')
                            with lock:
                                SUB_LINKS.append([sub_url, newSubName, showName])
                            return True

        return False

    except Exception as ex:
        errTitle = ""
        errMsg = "There was an error searching exact subtitle for " + showName
        errSolution = "Try again later"
        errAction = "continue"
        exception_routine(errMsg, errTitle, errSolution, errAction)


def download_my_shows(show):
    global TORRENTS_FILE_NAMES
    global MAGNETS_LIST
    global EPS_NOT_FOUND
    global SEASONS_NOT_FOUND
    global TORRENTS_TO_DOWNLOAD_LST

    try:

        show = show.replace('\'', '')
        if ' (us)' in show:
            show = show.replace(' (us)','')
        url = 'https://thepiratebay.org/search/' + show + '/0/99/0'
        req = read_webSite(url)
        if req is None:
            return
        html = req.text.lower()
        str = '<div class="detname">'  # parsing file to find 720P quality
        torrents_list = html.split(str)
        default_magnet = ''
        default_name = ''
        default_release = ''
        counter = 0

        for torrent_data in torrents_list[1:11]:
            counter += 1
            end_of_name_data = torrent_data.find('</div>')
            name_data = torrent_data[:end_of_name_data - 5]
            torrent_name = name_data[name_data.rfind('>') + 1:].lower()
            seeders_idx = torrent_data.find('<td align="right">')
            num_of_seeders = torrent_data[seeders_idx + 18 : torrent_data.find('</td>',seeders_idx)]
            release = get_release(torrent_name)

            if not check_if_item_is_valid(show, torrent_name,'torrent'):
                continue

            magnet_index = torrent_data.find('magnet:')
            magnet_link = torrent_data[magnet_index: torrent_data.find('"', magnet_index + 7)]
            if release != '':  # keep looking for a better torrent
                if int(num_of_seeders) < MIN_SEEDERS and default_magnet != '':
                    break # you didnt find nothing better, break and use default

                if not ( check_if_torrent_has_exact_subtitles(show,release) or check_if_torrent_has_exact_subtitles(show,release,get_subscene_alternative_name(show))):
                    if default_release == "":
                        default_release = release
                        default_magnet = magnet_link
                        default_name = torrent_name
                        continue
                else: #has matching subtitles
                    new_torrent_name = change_to_proper_name(show, torrent_name, release,'.')
                    TORRENTS_FILE_NAMES[show] = new_torrent_name
                    TORRENTS_TO_DOWNLOAD_LST.append(new_torrent_name)
                    MAGNETS_LIST.append(magnet_link)
                    return # found the torrent you were looking for

            #if default is yet set, set one
            elif default_magnet == '':
                default_magnet = magnet_link
                default_name = torrent_name
                default_release = release


        if counter == 0 or default_magnet == '':
            if 'season' in show:
                return
            EPS_NOT_FOUND.append(show)
        elif default_magnet[:6] == 'magnet':
            new_defult_torrent_name = change_to_proper_name(show,default_name,default_release,'.')
            TORRENTS_FILE_NAMES[show] = new_defult_torrent_name
            TORRENTS_TO_DOWNLOAD_LST.append(new_defult_torrent_name)
            MAGNETS_LIST.append(default_magnet)

    except Exception as ex:
        errTitle = ""
        errMsg = "There was an error while searching for :\n  - %s\n " % show
        errSolution = "Please try again later"
        errAction = "continue"
        exception_routine(errMsg, errTitle, errSolution, errAction)

def parse_file_to_dic(filePath,dic,splitter):

    f = open(filePath,'r')
    data = f.readlines()
    for line in data:
        line = line.strip("\n").lower()
        if line != "":
            items = line.split(splitter)
            key = items[0]
            val = items[1]
            dic[key] = val


def handle_input_from_text_editor(txt):
    global RUNTIME_ERRORS
    global REQUESTED_EPS_TO_DOWNLOAD
    global REQUESTED_SERIES_TO_DOWNLOAD
    global REQUESTED_MOVIES_TO_DOWNLOAD
    global REQUESTED_SUBS_TO_DOWNLOAD

    try:

        if txt == "":
            prompt_user_with_message("Please enter the desired show name first")
            return

        while txt[-1] == " ":  # erase any spaces at the end
            txt = txt[:-1]

        # if 'install utorrent' in txt:
        #     frame.panel.outPutTxtCtrl.Show()
        #     print "Follow The Installation instructions.\nDont worry its very simple:)"
        #     time.sleep(1)
        #     subprocess.Popen(['uTorrent.exe', USER_PATH])
        #     return False

        # if "password" in txt:
        #     new_pass = prompt_user_with_text_question(message="Enter New Password:")
        #     if new_pass != "":
        #         CURRENT_APP_PASSWORD = new_pass
        #         prompt_user_with_message("Password Updated Successfuly",title= "!")
        #     else:
        #         pass
                # prompt_user_with_message("Password Update Failed. Try Again","Tsk Tsk Tsk....")
            # return False

        # if "update" in txt:
        #     frame.panel.dropBoxItem.download_new_watchme_version()
        #     return False


        type = str(frame.panel.typeChoice.GetStringSelection())
        frame.panel.searchType = type

        if type == TYPE_OPTIONS[0]: #unchosen
            prompt_user_with_message("Choose item TYPE from the list!")
            return False

        elif type == TYPE_OPTIONS[1]: #Series
            season_num = frame.panel.seasonChoice.GetStringSelection()
            if season_num == SEASON_OPTIONS[0]:
                prompt_user_with_message("Choose season number from the list!")
                return False
            episode_num = frame.panel.episodeChoice.GetStringSelection()
            if episode_num == EPISODE_OPTIONS[0]:
                prompt_user_with_message("Choose episode number from the list!")
                return False
            elif episode_num == "All Season":
                itemName = "%s %s season" % (txt, season_num)
                frame.panel.searchString = itemName.lower()
                REQUESTED_SERIES_TO_DOWNLOAD.append(itemName.lower())
                return True

            else:
                itemName = "%s %s%s" %(txt,season_num, episode_num)
                frame.panel.searchString = itemName.lower()
                REQUESTED_EPS_TO_DOWNLOAD.append(itemName.lower())
                return True

        elif type == TYPE_OPTIONS[2]: #Movie
            REQUESTED_MOVIES_TO_DOWNLOAD.append(txt)
            frame.panel.searchString = txt.lower()
            return True

        elif type == TYPE_OPTIONS[3]: #Subs
            season_num = frame.panel.seasonChoice.GetStringSelection()
            if season_num == SEASON_OPTIONS[0]:
                season_num = ''
            episode_num = frame.panel.episodeChoice.GetStringSelection()
            if episode_num == EPISODE_OPTIONS[0]:
                episode_num = ''

            if episode_num == '' or season_num == '':
                REQUESTED_SUBS_TO_DOWNLOAD.append(txt)
                return True
            else:
                if episode_num == "All Season":
                    itemName = "%s %s subs" % (txt, season_num)
                    frame.panel.searchString = itemName.lower()
                    REQUESTED_SUBS_TO_DOWNLOAD.append(itemName.lower())
                    return True

                itemName = "%s %s%s%s" %(txt,season_num, episode_num," " + frame.panel.searchRelease)
                frame.panel.searchString = itemName.lower()
                REQUESTED_SUBS_TO_DOWNLOAD.append(itemName.lower())
                return True

        return False

    except Exception as ex:
        errTitle = ""
        errMsg = "I had an error while reading you'r input.\n"
        errSolution = "Make sure you wrote the item properly.\nIf error persists, please contact support."
        errAction = "continue"
        exception_routine(errMsg, errTitle, errSolution, errAction)


def Main_special_requests():
    global SPECIAL_REQUESTS_RUN

    SPECIAL_REQUESTS_RUN = True
    # for eps in sorted(REQUESTED_SERIES_TO_DOWNLOAD):
    #     print "  -  " + eps[:-7].title()
    #
    # for eps in sorted(REQUESTED_EPS_TO_DOWNLOAD):
    #     print "  -  " + eps.title()
    #
    # for sub in sorted(REQUESTED_SUBS_TO_DOWNLOAD):
    #     print "  -  " + sub.title() + ' SUBS'


    if len(RUNTIME_ERRORS) > 0:
        return
    #download series
    if len(REQUESTED_EPS_TO_DOWNLOAD) == 1:
        download_my_shows(REQUESTED_EPS_TO_DOWNLOAD[0])
    elif len(REQUESTED_SERIES_TO_DOWNLOAD) == 1:
        download_series_season(REQUESTED_SERIES_TO_DOWNLOAD[0])
    elif len(REQUESTED_MOVIES_TO_DOWNLOAD) == 1:
        download_my_shows(REQUESTED_MOVIES_TO_DOWNLOAD[0])


def Main_my_episodes():
    global MY_SHOWS, DATES
    global EPS_TO_DOWNLOAD_SINCE_UPDATE
    global RUNTIME_ERRORS

    try:
        print "Searching for new episodes since that day ...\n".format(LAST_VISIT)

        # create the shows list from the myShowList file
        multiThreading_routine(create_my_show_list, SHOWS_LIST_INPUT)

        # get all the dates since last update
        DATES = get_list_of_dates(LAST_VISIT)  # send the first line of the file without the \n char and ()
        # get a list of shows that came out since last update
        multiThreading_routine(get_my_shows_since_update, DATES)

        if len(RUNTIME_ERRORS) > 0:
            return

        if len(EPS_TO_DOWNLOAD_SINCE_UPDATE) == 0:
            print '    >> There are no new episodes yet'

            print "\n\nSee you next time :) \n"

            return

        else:
            print "   >> Found " + str(len(EPS_TO_DOWNLOAD_SINCE_UPDATE)) + " New Episodes \n"
            for eps in sorted(EPS_TO_DOWNLOAD_SINCE_UPDATE.keys()):
                print "    -  " + eps.title()

            if len(EPS_TO_DOWNLOAD_SINCE_UPDATE) > 0:
                print "\n\nSearching For Torrents...\n"

            # get all the necessary torrents

            multiThreading_routine(download_my_shows, EPS_TO_DOWNLOAD_SINCE_UPDATE.keys())

    except Exception as ex:
        errTitle = ""
        errMsg = "There was an error while downloading new shows"
        errSolution = "Please try again later"
        errAction = "continue"
        exception_routine(errMsg, errTitle, errSolution, errAction)


def Main_subs_routine():
    global ONLY_HD_QUALITY_FLAG
    global SUBS_NOT_FOUND

    if len(TORRENTS_TO_DOWNLOAD_LST) > 0:
        print "   >> Found " + str(len(TORRENTS_TO_DOWNLOAD_LST)) + " Torrents ... Downloading ...\n"
    for item in sorted(TORRENTS_TO_DOWNLOAD_LST):
        print "    -  " + item.title()


    if len(TORRENTS_TO_DOWNLOAD_LST) > 0 or len(REQUESTED_SUBS_TO_DOWNLOAD) > 0:
        print "\n\nSearching for subtitles...\n"

        # multiThreading_routine(download_exact_subtitles, TORRENTS_FILE_NAMES.keys() + REQUESTED_SUBS_TO_DOWNLOAD)
        MultiThreadingWithQueue(MAX_QUEUE_THREADS,activateThreads,TORRENTS_FILE_NAMES.keys() + REQUESTED_SUBS_TO_DOWNLOAD)

        # if len (SUBS_NOT_FOUND) == 0:
        #
        #     newName = get_subscene_alternative_name()

        if len(SUB_LINKS) > 0:
            print "   >> Found " + str(len(SUB_LINKS)) + " SUBS ... Downloading ...\n"

            multiThreading_routine(get_subtitle_file, SUB_LINKS)

        else:
            print "   >> No subtitles found, sorry."


def Main_errors_summary_and_goodbye():
    global LST_OF_FILES_TO_MOVE_LATER

    END_TIME = time.time()
    runTime = round(END_TIME - START_TIME,3)

    for item in sorted(DOWNLOADED_SUBS):
        print "    -  " + str(item.title())

    if len(ALREADY_HAVE_THESE_SUBS) is not 0:
        print "\n  (!) You already have these files:\n"
        for item in sorted(ALREADY_HAVE_THESE_SUBS):
            print "     -  " + str(item.title())

    #print unfound episodes
    if len(EPS_NOT_FOUND) > 0:
        print "\n  (!) Did not find the proper torrents for:\n"
        for torrent in sorted(EPS_NOT_FOUND):
            print "     -  " + torrent.title()
        if len(REQUESTED_MOVIES_TO_DOWNLOAD) > 0:
            print "\n   >>  Make sure you entered the right name"
        if ONLY_HD_QUALITY_FLAG:
            print "\n   >>  You can uncheck the 'HD ONLY' checkbox and try again"

    if len(SEASONS_NOT_FOUND) > 0:
        print "\n  (!) Did not find the proper torrent for:\n"
        for torrent in sorted(SEASONS_NOT_FOUND):
            print "     -  " + torrent.title()
        print "\n   >>  Make sure the name and season number is correct and try again:)"
        if ONLY_HD_QUALITY_FLAG:
            print "\n   >>  You can uncheck the 'HD ONLY' checkbox and try again"
    #print unfound subtitles
    if (len(SUBS_NOT_FOUND.keys()) > 0):
        print "\n  (!) Did not find any matching subs for:\n"
        for sub in sorted(SUBS_NOT_FOUND.keys()):
            print "     -  " + sub.title()


    # print bad show names
    if len(SHOWS_NOT_FOUND) > 0:
        print "\nSHOWS_NOT_FOUND:\n"
        for bad_show_name in SHOWS_NOT_FOUND:
            bad_show_name = bad_show_name.capitalize()
            print '  (!!) Can\'t find \"' + bad_show_name + '\" '
        print "   >>  Please write the exact show name and try again."



    if len(TORRENTS_TO_DOWNLOAD_LST + DOWNLOADED_SUBS) > 0 :
        print "\n\n\n" + "-" * 22 + " Session Summary " + "-" * 23 + "\n"
        print "    Downloaded ", str(len(TORRENTS_TO_DOWNLOAD_LST)), " Torrents"
        print "    Downloaded ", str(len(DOWNLOADED_SUBS)), " New Subtitles\n"
        print "    Runtime:  " + str(runTime) + "  seconds \n"
        print "-"*66


    # if len(LST_OF_FILES_TO_MOVE_LATER) > 0:
    #     if ORGANIZED_FOLDER_PATH:
    #         print "\n  (!) Could not move these files to shows folder:\n"
    #         for file in sorted([item[3] for item in LST_OF_FILES_TO_MOVE_LATER]):
    #             print "       -  " + file.title()
    #         print "\n      Because they are seeding in Utorrent.\n"
    #         print "   >>  Delete finished torrents in Utorrents and retry again\n" \
    #
    LST_OF_FILES_TO_MOVE_LATER = []

    if len(RUNTIME_ERRORS) > 0:
        print "\n  (!!)  Runtime Errors:\n"
        for error in set(RUNTIME_ERRORS):
            print '     -  ' + error

    if len(DATES) > 3 or len(EPS_TO_DOWNLOAD_SINCE_UPDATE) == 0:
        if not SPECIAL_REQUESTS_RUN:
            get_upcoming_shows()
            print_upcoming_shows()

    # print '\n\n\n'

    # download the shows
    if MODE is not 'DEBUG':
        multiThreading_routine(open_magnet,MAGNETS_LIST)

    frame.panel.outPutTxtCtrl.SetFocus()
    frame.panel.specialReqBtn.Enable()
    frame.panel.myEpisodesBtn.Enable()


def final_actions_routine():
    global SPECIAL_REQUESTS_RUN

    try:
        write_session_to_lastSession_file()
        #add_session_to_logFile()
        # move_seeding_files_shutdown_utorrent()

        t = threading.Thread(target = frame.panel.dropBoxItem.upload_log_to_dropbox, args = (LAST_SESSION_LOG_PATH,))
        t.setDaemon(True)
        t.start()
        # frame.panel.dropBoxItem.upload_log_to_dropbox(LAST_SESSION_LOG_PATH)            ###############ADD THIS#####
        manage_subs_folder()
        # manage_shows_folder()
        remove_leftover_folders(ORGANIZED_FOLDER_PATH + NEW_DOWNLOADS_FOLDER_NAME)
        remove_leftover_folders(ORGANIZED_FOLDER_PATH + SUBS_FOLDER_NAME)

        SPECIAL_REQUESTS_RUN = False

    except Exception as ex:
        errTitle = ""
        errMsg = "There was an error during the final actions."
        errSolution = "Try again later"
        errAction = "continue"
        exception_routine(errMsg, errTitle, errSolution, errAction)

def exec_my_episodes():
    global LAST_VISIT
    # global SHUTDOWN_OUTPUT_SCREEN
    try:

        # SHUTDOWN_OUTPUT_SCREEN = False
        Main_my_episodes()
        create_new_directories()
        Main_subs_routine()
        Main_errors_summary_and_goodbye()
        add_session_to_history_file()
        final_actions_routine()


        # update the config file with new date and shows id's
        if MODE is not 'DEBUG' and len(RUNTIME_ERRORS) == 0:
            today = datetime.datetime.today()
            month = today.month
            day = today.day
            year = today.year
            date_str = "%02d-%02d-%4d" % (day, month, year)
            LAST_VISIT = date_str
            today_date = wx.DateTimeFromDMY(int(day), int(month) - 1, int(year))
            frame.panel.datepick.SetValue(today_date)
            write_new_data_to_file()  # updates myShows file

    except Exception as ex:
        errTitle = ""
        errMsg = "There was an error downloading your new episodes"
        errSolution = "Try again later"
        errAction = "continue"
        exception_routine(errMsg, errTitle, errSolution, errAction)

def exec_special_requests():
    global RUNTIME_ERRORS
    global SHUTDOWN_OUTPUT_SCREEN
    try:

        print "\nSearching for item:   %s   (%s) \n" % (frame.panel.searchString.title(),frame.panel.searchType)
        Main_special_requests()
        create_new_directories()
        Main_subs_routine()
        Main_errors_summary_and_goodbye()
        final_actions_routine()


    except Exception as ex:
        errTitle = ""
        errMsg = "There was an error downloading your requested item"
        errSolution = "Try again later"
        errAction = "continue"
        exception_routine(errMsg, errTitle, errSolution, errAction)

# global helper parameters go get_sub_file
get_subtitle_file.counter = 0
get_subtitle_file.first_thread_flag = False
read_webSite.first_thread_flag = False
lock = threading.Lock()
print_lock = threading.Lock()
def check_if_now_is_scheduler_time():

    if not HAS_SCHEDULER:
        return False

    nowTime = datetime.datetime.now()

    now_hour = nowTime.hour
    now_minutes = nowTime.minute

    task_hour =  int(SCHEDULER_RUN_TIME.split(":")[0])
    task_minutes = int(SCHEDULER_RUN_TIME.split(":")[1])

    if task_hour == now_hour and task_minutes == now_minutes:
        return True
    else:
        return False


def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.AppendItem(item)
    menu.AppendSeparator()

    return item






















#-----------------------------------------------------------------------------------------------------------
#GUI CLASS
#-----------------------------------------------------------------------------------------------------------

class MyPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # self.SetBackgroundStyle(wx.BG_STYLE_ERASE)
        # self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        if FIRST_TIME:
            self.Greeting = wx.StaticText(self, label="\nHello " + USERNAME + " :)   This is your first time")
        else:
            self.Greeting = wx.StaticText(self, label="\nHello " + USERNAME + " :)   Your last visit was on")

        self.datepick = wx.DatePickerCtrl(self, size=(110,25), pos=(100, 15),
                                          style=wx.DP_DROPDOWN | wx.DP_SHOWCENTURY)
        self.datepick.Bind(wx.EVT_DATE_CHANGED, self.onAction)
        self.myEpisodesBtn = wx.Button(self, label="Download Special Requests", size = (170,30))
        self.myEpisodesBtn.Bind(wx.EVT_BUTTON, self.onSpecialRequests)
        self.editShowsBtn = wx.Button(self, label="Edit My Shows", size = (110,30))
        self.editShowsBtn.Bind(wx.EVT_BUTTON, self.onEditShows)
        self.list_box = None
        self.quote2 = wx.StaticText(self, label="You can also download a spicific episode,movie,or subtitle:\n")
        self.txt = wx.TextCtrl(self,-1,style=wx.TE_PROCESS_ENTER, size = (170,25))
        self.txt.Bind(wx.EVT_TEXT_ENTER, self.onTextEnter)
        self.specialReqBtn = wx.Button(self, label="Download My Episodes", size = (170,30))
        self.specialReqBtn.Bind(wx.EVT_BUTTON, self.onDownloadEpisodes)
        # self.specialReqBtn.SetBackgroundColour("Green")
        # self.Bind(wx.EVT_KEY_UP, self.onKeyUp)
        self.datepick.SetValue(self.string_to_dateTime())
        self.typeChoice = wx.Choice(self, choices=TYPE_OPTIONS, size=(90, 30))
        self.seasonChoice = wx.Choice(self, choices=SEASON_OPTIONS, size=(90, 30))
        self.episodeChoice = wx.Choice(self, choices=EPISODE_OPTIONS, size=(90, 30))
        self.typeChoice.Bind(wx.EVT_CHOICE, self.onTypeChoice)
        self.seasonChoice.Bind(wx.EVT_CHOICE, self.onSeasonChoice)
        self.episodeChoice.Bind(wx.EVT_CHOICE, self.onEpisodeChoice)
        self.checkBox = wx.CheckBox(self, label='HD Only')
        self.Bind(wx.EVT_CHECKBOX, self.onChecked)
        exit_button = wx.Button(self, label="Close", size = (100,30))
        exit_button.Bind(wx.EVT_BUTTON,self.onExit)
        self.Bind(wx.EVT_CLOSE, self.onExit)
        #------
        # show_folder_btn = wx.Button(self,label="",size = (40,40))
        # show_folder_btn.Bind(wx.EVT_BUTTON,self.onShowFolder)
        # hboxClose = wx.BoxSizer(wx.HORIZONTAL)
        # hboxClose.AddSpacer(20)
        # hboxClose.Add(show_folder_btn)
        # hboxClose.AddSpacer(70)
        # hboxClose.Add(exit_button)
        #
        # my_sizer.Add(hboxClose,wx.LEFT,wx.ALIGN_LEFT)
        #----

        # self.Bind(wx.EVT_END_SESSION,self.onExit)
        # self.Bind(wx.EVT_WINDOW_DESTROY,self.onExit)
        # self.Bind(wx.EVT_WINDOW_MODAL_DIALOG_CLOSED,self.onExit)
        # self.Bind(EVT_ERROR_EVENT, self.onError)
        self.typeChoice.SetSelection(0)
        self.seasonChoice.SetSelection(0)
        self.episodeChoice.SetSelection(0)
        self.seasonChoice.Disable()
        self.episodeChoice.Disable()

        my_sizer = wx.BoxSizer(wx.VERTICAL)

        #------ show folder button -----
        bmp = wx.Bitmap(USER_PATH + FOLDER_IMAGE_NAME, wx.BITMAP_TYPE_ANY)
        self.bmpbtn = wx.BitmapButton(self, id=wx.ID_ANY, bitmap=bmp, style=wx.BU_BOTTOM,
                                      size=(40, 30))
        # show_folder_btn = wx.Button(self,label="",size = (30,30))
        self.bmpbtn.Bind(wx.EVT_BUTTON,self.onShowFolder)
        # self.bmpbtn.SetBackgroundColour("GRAY")
        # self.bmpbtn.SetBitmapLabel("Open Shows Folder")

        my_sizer.AddSpacer(10)


        #----------------------------
        hboxClose = wx.BoxSizer(wx.HORIZONTAL)

        hboxClose.AddSpacer(15)
        hboxClose.Add(self.bmpbtn)
        # if not ENABLE_SERIES_ORGANIZER:
        #     self.bmpbtn.Hide()
        hboxClose.AddSpacer(42)
        hboxClose.Add(self.Greeting)
        #----------------------------

        my_sizer.Add(hboxClose,10,wx.LEFT,wx.ALIGN_LEFT)

        my_sizer.Add(self.datepick,0,wx.CENTER,)
        my_sizer.AddSpacer(20)
        my_sizer.Add(self.editShowsBtn, 0, wx.CENTER | wx.ALL)
        my_sizer.AddSpacer(20)
        my_sizer.Add(self.specialReqBtn, 0, wx.CENTER)
        my_sizer.AddSpacer(20)
        my_sizer.Add(self.quote2, 0, wx.CENTER)
        my_sizer.Add(self.txt,0,wx.CENTER)

        hboxSpecial = wx.BoxSizer(wx.HORIZONTAL)
        my_sizer.AddSpacer(20)
        hboxSpecial.Add(self.typeChoice)
        hboxSpecial.AddSpacer(20)
        hboxSpecial.Add(self.seasonChoice)
        hboxSpecial.AddSpacer(20)
        hboxSpecial.Add(self.episodeChoice)

        my_sizer.Add(hboxSpecial,wx.CENTER,wx.ALIGN_CENTER)
        my_sizer.AddSpacer(20)
        my_sizer.Add(self.checkBox, 0, wx.CENTER,20)
        my_sizer.AddSpacer(20)

        # hbox = wx.BoxSizer(wx.HORIZONTAL)
        my_sizer.Add(self.myEpisodesBtn,0,wx.CENTER,20)
        my_sizer.AddSpacer(20)
        # my_sizer.Add(show_folder_btn,0,wx.LEFT,0)
        my_sizer.Add(exit_button,0,wx.CENTER,20)
        my_sizer.AddSpacer(20)


        self.searchString = ''
        self.searchResult = None
        self.searchType = ''
        self.seriesName = ''
        self.searchRelease = ''
        # my_sizer.Add(hbox,wx.TEXT_ALIGNMENT_CENTER)

        #self.SetSizer(my_sizer)
        self.SetSizerAndFit(my_sizer)
        self.txt.SetFocus()

        self.outPutTxtCtrl = outputClass()
        self.taksBarItem = TaskBarIcon()
        self.dropBoxItem = DropBoxClass()

    def start_panel_init_threads(self):


        dbThread = threading.Timer(1, self.dropBoxItem.get_admin_data_from_dropBox)
        dbThread.setDaemon(True)
        dbThread.start()

        pid_thread = threading.Thread(target=write_pid_to_file)
        pid_thread.setDaemon(True)
        pid_thread.start()

        if FIRST_TIME:
            wx.FutureCall(3000, self.FirstRun)

        if ENABLE_SERIES_ORGANIZER:
            folder_thread = threading.Thread(
                target=remove_leftover_folders(ORGANIZED_FOLDER_PATH + NEW_DOWNLOADS_FOLDER_NAME))
            folder_thread.setDaemon(True)
            folder_thread.start()
            shows_thread = threading.Timer(3, manage_shows_folder)
            shows_thread.setDaemon(True)
            shows_thread.start()


    def onShowFolder(self,event):

        if ENABLE_SERIES_ORGANIZER:
            os.startfile(ORGANIZED_FOLDER_PATH)
        else:
            prompt_user_with_message("This button opens 'My Shows' folder."
                                     "First enable 'Organize Shows In Folder' ('Edit My Shows' button)",
                                     "'My Shows' Folder Link",)
    def onTextEnter(self,event):
        self.clearAllChoices()
        self.onTypeChoice("")


    def clearAllChoices(self):

        # self.seasonChoice.Clear()
        # self.episodeChoice.Clear()
        # self.seasonChoice.SetItems(SEASON_OPTIONS)
        # self.episodeChoice.SetItems(EPISODE_OPTIONS)
        # self.seasonChoice.SetSelection(self.num_of_seasons-1)
        # self.episodeChoice.SetSelection(self.num_of_eps+1)
        self.seasonChoice.Clear()
        self.episodeChoice.Clear()
        self.seasonChoice.Append("-- Season --")
        self.episodeChoice.Append("-- Episode --")
        self.seasonChoice.SetSelection(0)
        self.episodeChoice.SetSelection(0)

    def onTypeChoice(self,event):
        global SEASON_OPTIONS
        global TVDB_RESULT

        self.seasonChoice.Enable()
        self.episodeChoice.Enable()

        choice = str(self.typeChoice.GetStringSelection())

        if choice == TYPE_OPTIONS[0]: # default
            self.clearAllChoices()
            self.typeChoice.SetSelection(1)  # series is default

        elif choice == TYPE_OPTIONS[1]: # Series
            self.clearAllChoices()
            self.typeChoice.SetSelection(1)

        elif choice == TYPE_OPTIONS[2]: #Movie
            self.clearAllChoices()
            self.typeChoice.SetSelection(2)
            self.seasonChoice.Disable()
            self.episodeChoice.Disable()
            return

        elif choice == TYPE_OPTIONS[3]: #Subtitles
            self.typeChoice.SetSelection(3)
            if self.searchString != "":
                if self.searchRelease == "":
                    self.onEpisodeChoice("")
                return

        self.searchString = self.txt.GetValue().lower() # read text in editor

        # if self.searchString in ALTERNATIVE_COMMANDS:
        #     handle_input_from_text_editor(self.searchString)
        #     return

        try:

            ret_val = read_tvdb_details(self.searchString)
            if ret_val is False: # error connecting to website
                return
            if not TVDB_RESULT:
                err_msg = "The Show you entered does not exist!\n" \
                          "Make sure the item name and the item type is correct :)"
                if self.searchString == "":
                    err_msg = "First Write down the name of the item you wish to download and press enter"
                prompt_user_with_message(err_msg, "Bad Show Name")
                frame.panel.typeChoice.SetSelection(0)
                return
            if len(TVDB_RESULT) > 1:
                ret_ans = self.choose_show_from_list()
                if not ret_ans:
                    return
            else:
                self.searchResult = TVDB_RESULT[0]
            self.seriesName = self.searchResult.SeriesName
            self.txt.SetValue(str(self.seriesName))

            self.num_of_seasons = len(self.searchResult)

            if self.num_of_seasons == 1:
                self.num_of_seasons = 2
            self.seasonChoice.Clear()
            self.seasonChoice.Append("-- Season --")

            if self.num_of_seasons == 0:
                self.seasonChoice.Append("< Manual >")
                self.seasonChoice.SetSelection(0)
                return

            SEASON_OPTIONS = ["S" + str(num).zfill(2) for num in range(1,self.num_of_seasons)]
            self.seasonChoice.Enable()
            self.episodeChoice.Enable()

            # another_num_of_seasons = get_latest_season_number(self.searchString)
            # if another_num_of_seasons > self.num_of_eps and another_num_of_seasons != 0:
            #     num_of_seasons = another_num_of_seasons
            #     SEASON_OPTIONS = ["S" + str(num).zfill(2) for num in range(1, num_of_seasons)]

            for season in SEASON_OPTIONS:
                self.seasonChoice.Append(season)
            self.seasonChoice.Append("< Manual >")
            self.seasonChoice.SetSelection(self.num_of_seasons-1)
            self.onSeasonChoice("")
            self.anotherShowThread = threading.Thread(target=self.check_for_another_show_num)
            self.anotherShowThread.setDaemon(True)
            self.anotherShowThread.start()
        except Exception as ex:
            errTitle = ""
            errMsg = "I had an error while getting the show's details.\n"
            errSolution = "Please try again later.\nIf error persists, contact support."
            errAction = "continue"
            exception_routine(errMsg, errTitle, errSolution, errAction)

    def choose_show_from_list(self):
        self.episodeChoice.Enable()
        self.seasonChoice.Enable()

        self.chooseShow = ChooseShowDialog(self,-1,"Choose Show From List")
        self.chooseShow.onSearch(None)
        self.chooseShow.ShowModal()
        self.chooseShow.Destroy()
        if not frame.panel.searchResult :
            return False
        else:
            return True

    def onSeasonChoice(self,event):
        global EPISODE_OPTIONS
        try:
            choice = str(self.seasonChoice.GetStringSelection())[1:]
            if "--" in choice:
                return
            if " >" in choice:
                ans = prompt_user_with_text_question(message="For Example: 'S04'", title="Enter Season Number")
                if ans[0].lower() != 's':
                    prompt_user_with_error("Please follow the required format","Bad Input")
                    self.seasonChoice.SetSelection(self.num_of_seasons - 1)
                    choice = str(self.seasonChoice.GetStringSelection())[1:]
                else:
                    choice = ans[1:]
                    self.num_of_seasons = int(choice)
                    self.seasonChoice.Clear()
                    self.seasonChoice.Append("-- Season --")
                    SEASON_OPTIONS = ["S" + str(num).zfill(2) for num in range(1, int(choice)+1)]
                    for season in SEASON_OPTIONS:
                        self.seasonChoice.Append(season)
                    self.seasonChoice.Append("< Manual >")
                    self.seasonChoice.SetSelection(self.num_of_seasons)
            frame.panel.seasonChoice.Update()
            season_num = int(choice)
            try:
                self.num_of_eps = len(self.searchResult[season_num])
            except Exception as ex:
                season_num = self.num_of_seasons
                self.num_of_eps = 25

            self.updateNumOfEps()
            frame.panel.episodeChoice.Update()



        except Exception as ex:
            errTitle = ""
            errMsg = "I had an error while getting the season's details.\n"
            errSolution = "Please try again later.\nIf error persists, contact support."
            errAction = "continue"
            exception_routine(errMsg, errTitle, errSolution, errAction)

    def check_for_another_show_num(self):
        choice = str(self.seasonChoice.GetStringSelection())[1:]
        season_num = int(choice)
        choice = str(self.seasonChoice.GetStringSelection())[1:]
        another_num_of_eps = get_latest_episode_number("%s season %s" % (self.searchString, choice))
        if another_num_of_eps != self.num_of_eps and another_num_of_eps != 0:
            curr_choice = str(self.seasonChoice.GetStringSelection())[1:]
            curr_season_num = int(curr_choice)
            if season_num != curr_season_num:# make sure user didnt change season meanwhile
                return
            self.num_of_eps = another_num_of_eps
            self.updateNumOfEps()

    def updateNumOfEps(self):
        try:
            EPISODE_OPTIONS = ["E" + str(num).zfill(2) for num in range(1,self.num_of_eps  + 1)]
            self.episodeChoice.Clear()
            self.episodeChoice.Append("-- Episode --")
            for episode in EPISODE_OPTIONS:
                self.episodeChoice.Append(episode)
            self.episodeChoice.Append("All Season")
            self.episodeChoice.SetSelection(self.num_of_eps)
            self.episodeChoice.Enable()

        except Exception as ex:
            prompt_user_with_error("Error updating episodes list.\nTry again later.")


    def onEpisodeChoice(self,event):
        # self.myEpisodesBtn.SetFocus()
        if str(self.typeChoice.GetStringSelection()) == "Subtitles":
            ans = prompt_user_with_question("Do you want to search for a specific release?","Killers? Dimension? LOL ?..")
            if ans:
                release = prompt_user_with_text_question(message="which release?")
                self.searchRelease = release.lower()
                self.myEpisodesBtn.SetFocus()
            else:
                self.searchRelease = ''

    def string_to_dateTime(self):
        date_str = LAST_VISIT.split('-')
        day = date_str[0]
        month = date_str[1]
        year = date_str[2]
        date = wx.DateTimeFromDMY(int(day), int(month) - 1, int(year))
        return date

    def onAction(self,event):
        global LAST_VISIT

        selected = self.datepick.GetValue()
        month = selected.Month + 1
        day = selected.Day
        year = selected.Year
        date_str = "%02d-%02d-%4d" % (day, month, year)
        LAST_VISIT = date_str
        write_new_data_to_file('last_update')

    # def onKeyUp(self,event):
    #     keyCode = event.GetKeyCode()
    #     if keyCode == wx.WXK_ESCAPE:
    #         sys.exit(0)

    def onDownloadEpisodes(self, event):
        global START_TIME
        global SHUTDOWN_OUTPUT_SCREEN



        wake_app()
        clear_parameters()
        START_TIME = time.time()
        read_show_file()

        if event == "Scheduler":
            print "\n"
            print "-"*24 + " Scheduler Run " + "-"*25
            print ""

        print "\nHello " + USERNAME + " :)"
        print "Your last visit was on " + LAST_VISIT + "\n\n"

        try:
            self.th = threading.Thread(target=exec_my_episodes)
            self.th.setDaemon(True)
            self.th.start()
            frame.panel.specialReqBtn.Disable()
            frame.panel.myEpisodesBtn.Disable()

        except Exception as ex:
            wx.CallAfter(self.onError("Critical Error!\nPlease try again later."))

    def onSpecialRequests(self, event):
        global START_TIME
        global SHUTDOWN_OUTPUT_SCREEN

        self.searchString = ''
        self.searchType = ''
        self.seriesName = ''

        txt = self.txt.GetValue()
        clear_parameters()
        START_TIME = time.time()
        ok = handle_input_from_text_editor(txt)
        if not ok:
            return

        self.outPutTxtCtrl.log.Clear()
        self.outPutTxtCtrl.Show()
        self.outPutTxtCtrl.Raise()
        SHUTDOWN_OUTPUT_SCREEN = False

        try:
            th = threading.Thread(target=exec_special_requests)
            th.setDaemon(True)
            th.start()
            frame.panel.specialReqBtn.Disable()
            frame.panel.myEpisodesBtn.Disable()
        except Exception as ex:
            self.onError("Error downloading special request.\n"
                         "Please try again later.")

    def onEditShows(self, event):

        #read_show_file()
        #multiThreading_routine(create_my_show_list, SHOWS_LIST_INPUT)
        if self.list_box == None:
            self.list_box = ListBoxClass(frame.panel)
            icon = wx.IconFromBitmap(wx.Bitmap(EDIT_SHOWS_ICON_PATH))
            self.list_box.SetIcon(icon)
        else:
            self.list_box.Center()
            self.list_box.update_listbox_items()
            self.list_box.Show()
            self.list_box.SetFocus()


    def FirstRun(self):
        # self.Greeting.SetLabel("\nHello " + USERNAME + " :)")
        self.dropBoxItem.download_user_agreement()
        msg = first_time_screen()
        dlg=wx.MessageDialog(self, msg, "Welcome to WatchMe:)", wx.OK|wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Center()
        dlg.Destroy()

    def onChecked(self,e):
        global ONLY_HD_QUALITY_FLAG

        cb = e.GetEventObject()
        ONLY_HD_QUALITY_FLAG = cb.GetValue()

    def onError(self, msg,title="Error!"):
        # with lock:
        prompt_user_with_error(msg,title)
        # self.outPutTxtCtrl.Close()
        # self.Close()
        # self.Destroy()
        # frame.Destroy()
        # sys.exit(1)
        finals_actions_before_quit()
        frame.Hide()
        time.sleep(2)
        close_app_for_good()

    def onSleep(self,event):
        print event

    def onExit(self, event):

        finals_actions_before_quit()

        if HAS_SCHEDULER:
            put_app_to_sleep()

        else:
            close_app_for_good()
            # try:
            #     self.outPutTxtCtrl.Close()
            #     self.taksBarItem.RemoveIcon()
            #     self.taksBarItem.Destroy()
            #     frame.Close()
            #     frame.Destroy()
            #

    def OnEraseBackground(self, evt):
        """
        Add a picture to the background
        """
        # yanked from ColourDB.py
        dc = evt.GetDC()

        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()

        bmp = wx.Bitmap("pic.jpg")
        img = wx.ImageFromBitmap(bmp)
        w,h = img.GetSize()
        cliWidth, cliHeight = self.GetClientSize()

        img = img.Scale(cliWidth, cliHeight, wx.IMAGE_QUALITY_HIGH)
        scaledBmp = wx.BitmapFromImage(img)
        # xPos = (cliWidth - w)/2
        # yPos = (cliHeight - h)/2

        dc.DrawBitmap(scaledBmp, 0, 0)
        dc.SetBackgroundMode(wx.TRANSPARENT)


#---------------------------------------------------------------------------------------------

class ListBoxClass(wx.Frame):

    def __init__(self,parent):
        wx.Frame.__init__(self,parent,title='My Shows Settings',size = (340,450), pos=(500,180),
                          style = wx.CLOSE_BOX  | wx.CAPTION )

        ID_NEW = 1
        ID_CLOSE = 2
        ID_CLEAR = 3
        ID_DELETE = 4
        ID_DETAILS = 5
        ID_UPDATE = 6

        panel = wx.Panel(self, -1)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        mainBox = wx.BoxSizer(wx.VERTICAL)
        schedBox = wx.BoxSizer(wx.HORIZONTAL)

        self.choiceLabel = '   -- Select Show To Add --'
        read_best_shows_file()
        read_show_file()
        best_shows_title = [show.title() for show in BEST_SHOWS.keys()]
        self.choice = wx.Choice(panel, choices=[self.choiceLabel] + sorted(best_shows_title),size =(180,30), style = wx.CB_SORT)
        self.choice.Bind(wx.EVT_CHOICE, self.onChoice)
        self.choice.SetSelection(0)

        self.listbox = wx.ListBox(panel, -1,size = (250,200),style = wx.LB_NEEDED_SB |wx.LB_EXTENDED )

        for item in sorted(MY_SHOWS.keys()):
            self.listbox.Append(item.title())

        # self.Bind(wx.EVT_LIST_DELETE_ITEM,self.onDel)
        btnPanel = wx.Panel(panel, -1)
        new = wx.Button(btnPanel, ID_NEW, 'New Show', size=(95, 30))
        dlt = wx.Button(btnPanel, ID_DELETE, 'Delete', size=(95, 30))
        clr = wx.Button(btnPanel, ID_CLEAR, 'Clear ALL', size=(95, 30))
        detailsBtn = wx.Button(btnPanel, ID_DETAILS,'IMDB Details', size=(95,30))
        updateShowsBtn = wx.Button(btnPanel,ID_UPDATE,'Update ShowList', size=(95,30))

        self.manage_shows_checkBox = wx.CheckBox(panel, label='Organize Shows In Folder', pos=(0, 10))
        self.manage_shows_checkBox.Bind(wx.EVT_CHECKBOX, self.onShowsCheckBox)

        # self.schedulerCheckbox = wx.CheckBox(panel, label='Download Episodes Automatically', pos=(0, 10))
        # self.minuteChoice = wx.Choice(self, choices=[str(x+1) for x in range(60)], size=(20, 30))
        # self.minuteChoice.Bind(wx.EVT_CHOICE, self.onMinuteChoice)
        # self.hourChoice = wx.Choice(self, choices=[str(x+1) for x in range(24)], size=(20, 30))
        # self.hourChoice.Bind(wx.EVT_CHOICE, self.onHourChoice)
        # schedBox.Add(self.schedulerCheckbox,0,wx.LEFT,10)
        # schedBox.Add(self.hourChoice,0)
        # schedBox.Add(self.minuteChoice,0)

        self.Bind(wx.EVT_BUTTON, self.NewItem, id=ID_NEW)
        self.Bind(wx.EVT_BUTTON, self.OnDelete, id=ID_DELETE)
        self.Bind(wx.EVT_BUTTON, self.OnClear, id=ID_CLEAR)
        self.Bind(wx.EVT_BUTTON, self.onIMDB, id=ID_DETAILS)
        self.Bind(wx.EVT_BUTTON, self.onUpdate, id=ID_UPDATE)
        #self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnRename)

        vbox.Add((-1, 20))
        vbox.Add(new)
        vbox.Add(dlt, 0, wx.TOP, 5)
        vbox.Add(clr, 0, wx.TOP, 5)
        vbox.Add(detailsBtn,0,wx.TOP,5)
        vbox.AddSpacer(30)
        vbox.Add(updateShowsBtn,0,wx.TOP,5)

        btnPanel.SetSizer(vbox)
        hbox.Add(self.listbox, 1, wx.ALL, 20)
        hbox.Add(btnPanel, 0.6, wx.EXPAND | wx.RIGHT, 20)

        mainBox.Add((-1, 20))
        mainBox.Add(self.choice, 0, wx.LEFT , 20)
        mainBox.Add(hbox,wx.EXPAND | wx.ALL | wx.CENTRE,5)

        cls = wx.Button(panel, ID_CLOSE, 'Close', size=(90, 30))
        self.Bind(wx.EVT_BUTTON, self.onClose, id=ID_CLOSE)
        self.Bind(wx.EVT_CLOSE, self.onClose)


        self.path_box = wx.BoxSizer(wx.HORIZONTAL)
        self.dirPick = wx.DirPickerCtrl(panel, path=ORGANIZED_FOLDER_PATH, message="Select Shows Directory",size = (300,25),style=wx.DIRP_USE_TEXTCTRL | wx.DIRP_SMALL)
        self.path_box.Add(self.dirPick , 0, wx.EXPAND | wx.ALL , 20)
        self.dirPick.Bind(wx.EVT_DIRPICKER_CHANGED,self.onSetDirectory)
        self.dirPick.Disable()

        mainBox.Add(self.manage_shows_checkBox,0, wx.LEFT,20)
        #self.downloadText = wx.StaticText(panel, label="Choose Download Directory")
        #mainBox.Add(self.downloadText,0,wx.LEFT,20)
        mainBox.Add(self.path_box, wx.CENTRE,5)

        mainBox.Add(cls, 4, wx.CENTRE, 0)
        mainBox.Add((-1, 20))

        if ENABLE_SERIES_ORGANIZER:
            self.manage_shows_checkBox.SetValue(True)
            self.dirPick.Enable()
        else:
            self.manage_shows_checkBox.SetValue(False)
            self.dirPick.Disable()

        panel.SetSizer(mainBox)
        self.Centre()
        self.Show(True)


    def update_listbox_items(self):

        self.listbox.Clear()
        for item in sorted(MY_SHOWS.keys()):
            self.listbox.Append(item.title())

    def onDel(self,event):

        pass

    def onUpdate(self,event):

        frame.panel.outPutTxtCtrl.Show()
        print "Updating shows data base...This can take a minute..."
        print "Sing along with me meanwhile...\n"

        # update_all_shows_dic_and_file()

        try:

            update_thread = threading.Thread(target=update_all_shows_dic_and_file)
            update_thread.setDaemon(True)
            update_thread.start()

        except Exception as ex:
            prompt_user_with_message(ex.message)
    # def onDownload(self,event):
    #     global REQUESTED_SERIES_TO_DOWNLOAD
    #     global START_TIME
    #
    #     clear_parameters()
    #     START_TIME = time.time()
    #
    #     selNum = self.listbox.GetSelection()
    #     if selNum == -1:
    #         prompt_user_with_message("You must choose a series from the list first....")
    #         return
    #     selstring = str(self.listbox.GetString(selNum)).lower()
    #
    #     print "\nSearching for all '%s' seasons...\n" % selstring.title()
    #
    #     season_number = get_latest_season_number(selstring)
    #     if season_number == 0:
    #         season_number = 1
    #
    #     print "\nFound %d seasons:\n" % season_number
    #     for i in range(season_number):
    #         REQUESTED_SERIES_TO_DOWNLOAD.append(selstring + " s0%d season" % (i+1))
    #
    #
    #
    #     try:
    #         th = threading.Thread(target=exec_special_requests)
    #         th.start()
    #
    #     except Exception as ex:
    #         frame.panel.onError(ex.message)
    #

    def onIMDB(self,event):

        db = api.TVDB("B43FF87DE395DF56")

        selNum = self.listbox.GetSelections()
        if len(selNum) > 1:
            prompt_user_with_message("Please choose only one item at a time for this feature")
        else:
            selNum = selNum[0]

        if selNum == -1:
            prompt_user_with_message("You must choose a series from the list first....")
            return
        selstring = str(self.listbox.GetString(selNum)).lower()

        result = db.search(selstring, 'en')
        id = str(result[0].IMDB_ID)
        imbd_link = "http://www.imdb.com/title/%s" % id
        webbrowser.open_new_tab(imbd_link)


    def onSetDirectory(self,event):
        global ORGANIZED_FOLDER_PATH

        ORGANIZED_FOLDER_PATH = self.dirPick.GetPath() + "\\"

    def onShowsCheckBox(self,event):
        global ENABLE_SERIES_ORGANIZER

        read_show_file()

        if ENABLE_SERIES_ORGANIZER == False:

            msg = "This is a new feature:)\nIn order for this to work properly,\n" + \
                                       "you need to change one setting in your Utorrent client.\n" + \
                                        "You want to try?  (Totaly worth it)"

            ans = prompt_user_with_question(msg, "New Feature!")

            if ans:
                successful = show_utorrent_settings_instructions()
                if successful:
                    ENABLE_SERIES_ORGANIZER = True
                    self.manage_shows_checkBox.SetValue(True)
                    self.dirPick.Enable()
                    self.dirPick.SetPath(DEFAULT_MY_SHOWS_FOLDER)
                    last_msg = "Now all of your new downloads will automatically move into\n" \
                               "that folder once they finish downloading,\n" \
                               "and I will organize it for you ;)"
                    prompt_user_with_message(last_msg,"Well Done :)")
                    write_new_data_to_file('last_update')
                    frame.panel.bmpbtn.Show()
                else:
                    self.manage_shows_checkBox.SetValue(False)
                    self.dirPick.Disable()

        else:
            ENABLE_SERIES_ORGANIZER = False
            self.manage_shows_checkBox.SetValue(False)
            self.dirPick.Disable()
            frame.panel.bmpbtn.Hide()

        write_new_data_to_file('last_update')


    def onChoice(self, event):
        global BEST_SHOWS
        global MY_SHOWS

        choice = str(self.choice.GetStringSelection().lower())
        if choice not in MY_SHOWS.keys() and choice != self.choiceLabel.lower() and choice != "":
            frame.panel.list_box.listbox.Append(choice.title())
            MY_SHOWS[choice] = BEST_SHOWS[choice]
            del BEST_SHOWS[choice]
            write_new_data_to_file('last_update')
            read_best_shows_file()
            self.choice.Clear()
            self.choice.AppendItems([self.choiceLabel] + sorted([show.title() for show in BEST_SHOWS.keys()]))
            self.choice.SetSelection(0)
        else:
            if choice == self.choiceLabel.lower():
                return
            prompt_user_with_message("You are already following %s" % choice)


    def NewItem(self, event):
        global MY_SHOWS

        new_item = NewShowDialog(self, -1, 'Enter New Show')
        new_item.ShowModal()
        new_item.Destroy()


    def OnDelete(self, event):
        global MY_SHOWS
        global BEST_SHOWS

        user_selections = self.listbox.GetSelections()

        if not user_selections:
            return

        for sel in reversed(user_selections):
            if sel != -1:
                selstring = str(self.listbox.GetString(sel)).lower()
                BEST_SHOWS[selstring] = MY_SHOWS[selstring]
                del MY_SHOWS[selstring]
                self.listbox.Delete(sel)

        # for sel in user_selections:
        #     self.listbox.Delete(sel)

        write_new_data_to_file('last_update')
        self.choice.Clear()
        self.choice.AppendItems([self.choiceLabel] + sorted([show.title() for show in BEST_SHOWS.keys()]))
        self.choice.SetSelection(0)

    def OnClear(self, event):
        global MY_SHOWS

        if self.listbox.GetCount() == 0:
            return

        dlg = wx.MessageDialog(None, 'Are you sure??', 'Delete all shows?', wx.YES_NO | wx.ICON_QUESTION |wx.CENTRE)
        result = dlg.ShowModal() == wx.ID_YES
        dlg.Destroy()

        if result is True:
            self.listbox.Clear()
            MY_SHOWS.clear()
            write_new_data_to_file('last_update')
        read_best_shows_file()
        self.choice.Clear()
        self.choice.AppendItems([self.choiceLabel] +  sorted([show.title() for show in BEST_SHOWS.keys()]))
        self.choice.SetSelection(0)

    def onClose(self,event):
        #self.Close()

        self.Hide()
        frame.Raise()
        # self.Destroy()
        #write_new_data_to_file('la)

#---------------------------------------------------------------------------------------------


# class ListBoxFrame(wx.Frame,):
#     def __init__(self):
#         wx.Frame.__init__(self, None, -1, 'Choose Youur Show',size=(250, 200))
#         self.panel = wx.Panel(self, -1)
#         self.quote2 = wx.StaticText(self,label="\nIf you wish to \n"
#         self.new_show = wx.GetTextFromUser("Type Show's Name", 'Add Custom Show To Show List',"Eze Picho Shahaf")
#         self.choices = get_list_of_relevant_shows(str(self.new_show))
#         sizer = wx.BoxSizer(wx.VERTICAL)
#         self.listBox = wx.ListBox(self.panel, -1, (20, 20), (80, 120))
#         #self.listBox.SetSelection(0)
#         sizer.Add(self.listBox)
#         self.panel.SetSizer(sizer)
#         self.Show(True)
#         self.Center()

class NewShowDialog(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(200,270))

        self.parent = self.GetParent()

        self.txt = wx.TextCtrl(self, -1, style=wx.SUNKEN_BORDER | wx.TE_PROCESS_ENTER, size = (150,25))
        self.txt.Bind(wx.EVT_TEXT_ENTER, self.onSearch)

        self.listbox = wx.ListBox(self, -1, size = (150,110),style=wx.LB_SINGLE)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.onAdd)
        self.searchBtn = wx.Button(self,2,"Search", size = (100,25))
        self.closeBtn = wx.Button(self, 1, 'Close', size = (70,25))
        self.addBtn = wx.Button(self,3,"Add",size = (70,25))

        self.Bind(wx.EVT_BUTTON,self.onSearch,id =2)
        self.Bind(wx.EVT_BUTTON, self.onClose, id=1)
        self.Bind(wx.EVT_BUTTON, self.onAdd, id=3)
        #self.Bind(wx.EVT_CHAR_HOOK,self.onKeyPush)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.addBtn,1,wx.LEFT | wx.ALL,3)
        hbox.Add(self.closeBtn, 1, wx.RIGHT | wx.ALL,3)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddSpacer(10)
        sizer.Add(self.txt,0,wx.CENTRE | wx.ALL,5)
        sizer.Add(self.searchBtn,0,wx.CENTER | wx.ALL,5)
        sizer.Add(self.listbox,0,wx.CENTRE | wx.EXPAND ,5)
        sizer.Add(hbox, 0,wx.CENTRE | wx.ALL,5)
        self.SetSizer(sizer)
        self.Centre()

        self.txt.SetFocus()

    # def onKeyPush(self,event):
    #     keyCode = event.GetKeyCode()
    #
    #     if keyCode == wx.WXK_RETURN:
    #         if self.listbox.GetSelection() != -1:
    #             self.onAdd(event)
    #         else:
    #             self.onSearch(event)
    #
    #     elif keyCode == wx.WXK_ESCAPE:
    #         self.onClose(event)
    #



    def onSearch(self,event):

        self.listbox.Clear()
        new_show = str(self.txt.GetValue())
        if new_show == "":
            return

        relevant_shows_lst = get_list_of_relevant_shows(new_show)
        for item in sorted(relevant_shows_lst):
            self.listbox.Append(item.title())

        self.addBtn.SetFocus()

    def onAdd(self,event):

        num = self.listbox.GetSelection()
        new_show = str(self.listbox.GetString(num))
        new_show = new_show.strip('\n').lower()
        if new_show == "":
            return
        elif new_show in MY_SHOWS.keys():
            prompt_user_with_message("You are already following this show! You Fool.")
            return

        self.Close()
        frame.panel.list_box.listbox.Append(new_show.title())
        id = get_show_id(new_show)
        if id == -1:
            prompt_user_with_message("Sorry,There was an error adding the show. Try again later.")
            return
        else:
            MY_SHOWS[new_show] = id
            write_new_data_to_file('last_update')


    def onClose(self, event):
        self.Close()

    def OnSelect(self, event):
        item = event.GetSelection()
#--------------------------------------------
class ChooseShowDialog(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(200,270))

        self.parent = self.GetParent()

        self.txt = wx.TextCtrl(self, -1, value = frame.panel.searchString,
                                style=wx.SUNKEN_BORDER | wx.TE_PROCESS_ENTER, size = (150,25))
        self.txt.Bind(wx.EVT_TEXT_ENTER, self.onSearch)

        self.listbox = wx.ListBox(self, -1, size = (150,110))
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.onChoose)
        # self.listbox.Bind(wx.EVT_COMMAND_ENTER,self.onChoose)
        self.chooseBtn = wx.Button(self,1,"Choose",size = (70,25))
        self.searchBtn = wx.Button(self,2,"Search", size = (100,25))
        self.closeBtn = wx.Button(self, 10, 'Close', size = (70,25))

        self.Bind(wx.EVT_BUTTON, self.onChoose, id=1)
        self.Bind(wx.EVT_BUTTON,self.onSearch,id =2)
        self.Bind(wx.EVT_BUTTON, self.onClose, id=10)
        # self.Bind(wx.EVT_CHAR_HOOK,self.onKeyPush)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.chooseBtn,1,wx.LEFT | wx.ALL,3)
        hbox.Add(self.closeBtn, 1, wx.RIGHT | wx.ALL,3)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddSpacer(10)
        sizer.Add(self.txt,0,wx.CENTRE | wx.ALL,5)
        sizer.Add(self.searchBtn,0,wx.CENTER | wx.ALL,5)
        sizer.Add(self.listbox,0,wx.CENTRE | wx.EXPAND ,5)
        sizer.Add(hbox, 0,wx.CENTRE | wx.ALL,5)
        self.SetSizer(sizer)
        self.Centre()

        self.listbox.SetFocus()

    # def onKeyPush(self,event):
    #     return
    #
    #     keyCode = event.GetKeyCode()
    #
    #
    #     if keyCode == wx.WXK_ESCAPE:
    #         self.onClose(event)
    #     elif keyCode == wx.WXK_DOWN:
    #         self.listbox.SetFocus()
    #         self.listbox.SetFirstItem()




    def onSearch(self,event):
        global TVDB_RESULT

        new_show = str(self.txt.GetValue())

        if event is not None:
            TVDB_RESULT = None
            read_tvdb_details(new_show)

        self.listbox.Clear()
        if new_show == "":
            return

        relevant_shows_lst = [str(item.SeriesName) for item in TVDB_RESULT._result]
        for item in relevant_shows_lst:
            self.listbox.Append(item.title())

        self.listbox.SetSelection(0)
        self.listbox.SetFocus()

    def onChoose(self,event):
        num = self.listbox.GetSelection()
        new_show = str(self.listbox.GetString(num))
        new_show = new_show.strip('\n')
        if new_show == "":
            return

        self.Close()
        frame.panel.txt.SetValue(new_show)
        frame.panel.searchString = new_show
        frame.panel.searchResult = TVDB_RESULT._result[num]


    def onClose(self, event):
        self.Close()

    def OnSelect(self, event):
        item = event.GetSelection()


class RetryFrame(wx.Dialog):

    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(200,270))
        self.parent = self.GetParent()

        self.msg = ''
        self.msgText = wx.StaticText(self, label=msg)

        self.retryBtn = wx.Button(self, 2, "Retry", size=(100, 25))
        self.closeBtn = wx.Button(self, 1, 'Close', size=(100, 25))

        self.Bind(wx.EVT_BUTTON, self.onRetry, id=2)
        self.Bind(wx.EVT_BUTTON, self.onClose, id=1)

        # self.Bind(wx.EVT_CHAR_HOOK,self.onKeyPush)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.retryBtn, 1, wx.RIGHT | wx.ALL, 3)
        hbox.Add(self.closeBtn, 1, wx.LEFT | wx.ALL, 3)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddSpacer(10)
        sizer.Add(self.msgText, 10, wx.LEFT | wx.ALL, 10)

        sizer.Add(hbox, 0, wx.CENTRE | wx.ALL, 5)
        self.SetSizer(sizer)
        self.Centre()

        self.retryBtn.SetFocus()

    def onRetry(self,event):
        pass
    def onClose(self,event):
        pass

# ---------------------------------------------------
class MainWindow(wx.Frame):
    def __init__(self):

        global USER_DISPLAY_SIZE

        USER_DISPLAY_SIZE = wx.GetDisplaySize()

        x_pos = USER_DISPLAY_SIZE[0]/2 - APP_SIZE[0] + 5
        y_pos = USER_DISPLAY_SIZE[1]/2 - APP_SIZE[1]/2

        wx.Frame.__init__(self, None, title=" "*2 + "WatchMe - %s" % APP_VERSION, size=APP_SIZE,pos=(x_pos,y_pos),
                          style = wx.CLOSE_BOX  | wx.CAPTION  | wx.MINIMIZE_BOX | wx.SYSTEM_MENU)

        # self.SetBackgroundColour(wx.WHITE)



    def create_panel(self):

        self.panel = MyPanel(self)
        self.Bind(wx.EVT_CLOSE,self.onClose)
        self.panel.checkBox.SetValue(True)

    def add_menu_bar(self):

        # --------MENU BAR---------
        menuBar = wx.MenuBar()
        fileMenu = wx.Menu()
        # fileMenu.SetBackgroundColour(wx.GREEN_PEN)

        utorrentMenu = fileMenu.Append(wx.NewId(),"Install Utorrent", "Download Utorrent Application")
        self.Bind(wx.EVT_MENU, self.onDownloadUtorrent, utorrentMenu)
        # fileMenu.AppendSeparator()
        # passWordMenu = fileMenu.Append(wx.NewId(), "Change Password", "Change User Password")
        # self.Bind(wx.EVT_MENU, self.onPassWordMenu, passWordMenu)
        fileMenu.AppendSeparator()
        createScheduler = fileMenu.Append(wx.NewId(), "Create Scheduler",  "Run App in Background")
        self.Bind(wx.EVT_MENU, self.onCreateScheduler, createScheduler)
        fileMenu.AppendSeparator()
        deleteScheduler = fileMenu.Append(wx.NewId(), "Delete Scheduler",  "Delete Task")
        self.Bind(wx.EVT_MENU, self.onDelSchedule, deleteScheduler)
        fileMenu.AppendSeparator()
        organizeShows = fileMenu.Append(wx.NewId(), "Organize Shows Folder","Organize")
        self.Bind(wx.EVT_MENU, self.onOrganizeShows, organizeShows)
        fileMenu.AppendSeparator()
        upcomingEpisodes = fileMenu.Append(wx.NewId(),"Upcoming Episodes", "See The Future")
        self.Bind(wx.EVT_MENU, self.onUpcomingEpisodes, upcomingEpisodes)
        fileMenu.AppendSeparator()
        updateMenu = fileMenu.Append(wx.NewId(), "Update WatchMe","Get Lastest Version")
        self.Bind(wx.EVT_MENU, self.onUpdateMenu, updateMenu)
        fileMenu.AppendSeparator()
        contactMenu = fileMenu.Append(wx.NewId(), "Contact Support","Get Help!")
        self.Bind(wx.EVT_MENU, self.onContactSupport, contactMenu)
        fileMenu.AppendSeparator()
        aboutMenu = fileMenu.Append(wx.NewId(), "About WatchMe", "About")
        self.Bind(wx.EVT_MENU, self.onAbout,aboutMenu)

        menuBar.Append(fileMenu, "& More Options  ")
        self.SetMenuBar(menuBar)

        # -------------------------
        # randomId = wx.NewId()
        # accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CTRL,  ord('O'), randomId )])
        # self.Bind(wx.EVT_MENU, self.onKeyCombo, id=randomId)
        # self.SetAcceleratorTable(accel_tbl)


    def onClose(self,event):
        frame.panel.onExit("")



    def onCreateScheduler(self,event):
        global HAS_SCHEDULER
        global SCHEDULER_RUN_TIME

        ans = True

        if HAS_SCHEDULER:
            ans = prompt_user_with_question("You already have a scheduler set for {}\n"
                                            "Do you want to create a new one instead?\n".format(SCHEDULER_RUN_TIME),
                                            "Edit Scheduler Run-Time")
            if not ans:
                return
        else:
            ans = prompt_user_with_question("The scheduler is a new feature:)\n\n"
                                                 "If you approve,the app will run once a day,\n"
                                                 "and automaticaly download your favorite shows.\n"
                                                 "Do you want to try it out?\n",
                                                 "WatchMe Scheduler")
        if ans:
            runTime = prompt_user_with_text_question(message="Enter the time you want the app to run at every day\n"
                                           "\nFor Example: \'23:30\'\n",title="Choose Scheduler Time")
            if not runTime:
                prompt_user_with_message("No pressure. Try it when you're ready.", "Too bad")
                return
            if ":" not in runTime:
                prompt_user_with_message("Please insert a valid time as requested")
                return
            try:
                hour = runTime.split(":")[0]
                minute = runTime.split(":")[1]
                if int(hour) < 0 or int(hour) > 23:
                    prompt_user_with_error("Please insert a valid hour ( 0 - 23 ")
                    return
                if int(minute) < 0 or int(minute) > 59:
                    prompt_user_with_error("Please insert a valid minute ( 0 - 59 )")
                    return
                SCHEDULER_RUN_TIME = runTime
                HAS_SCHEDULER = True
                self.panel.scheduler = EventScheduler(hour, minute,"create")

            except Exception as ex:
                prompt_user_with_message("Please insert a valid time as requested")



    def onDelSchedule(self,event):
        global HAS_SCHEDULER
        global SCHEDULER_RUN_TIME

        if not HAS_SCHEDULER:
            prompt_user_with_message("Scheduler was yet activated.\n"
                                     "Click on 'Create Scheduler' and I will guide you from there:)\n","First Create, Then Delete....")
        else:
            self.panel.scheduler = EventScheduler('0', '0',"delete")
            HAS_SCHEDULER = False
            SCHEDULER_RUN_TIME = ""

    # def onPassWordMenu(self,event):
    #     global CURRENT_APP_PASSWORD
    #     new_pass = prompt_user_with_text_question(message="Enter New Password:")
    #     if new_pass != "":
    #         sure = prompt_user_with_question("If you enter the wrong password, \n "
    #                                          "you will not be able to use this app...",
    #                                          "Are you sure??\n ")
    #         if sure:
    #             CURRENT_APP_PASSWORD = new_pass
    #             prompt_user_with_message("Password Updated Successfuly",title= "Success!")
    #     else:
    #         prompt_user_with_message("Password Update Failed. Try Again Later","Tsk Tsk Tsk....")
    #     return False

    def onUpdateMenu(self,event):
        time.sleep(1)
        self.panel.dropBoxItem.download_new_watchme_version()              ##### ADD THISS!!!!@$#!@

    def onDownloadUtorrent(self,event):
        self.panel.outPutTxtCtrl.Show()
        self.panel.outPutTxtCtrl.log.Clear()
        self.panel.outPutTxtCtrl.Raise()

        print "Follow The Installation instructions.\nDont worry its very simple:)"
        time.sleep(1)
        try:
            subprocess.Popen(['uTorrent.exe', USER_PATH])
        except Exception as ex:
            errTitle = "Error"
            errMsg = "I had a problem trying to open Utorrent."
            errSolution = "Make sure it is properly installed.\n" \
                          "If error persists, please contact support."
            errAction = "continue"
            exception_routine(errMsg, errTitle, errSolution, errAction)

        return

    def onOrganizeShows(self,event):
        if not ENABLE_SERIES_ORGANIZER:
            msg = "If you want me to organize your shows for you, \n" \
                  "click on 'Edit My Shows', check the 'Organize Shows In Folder'\n" \
                  "checkbox and follow the instructions."
            prompt_user_with_message(msg,title="Trust Me...Do it.")
            return

        manage_shows_folder()
        manage_subs_folder()
        remove_leftover_folders(ORGANIZED_FOLDER_PATH + NEW_DOWNLOADS_FOLDER_NAME)
        remove_leftover_folders(ORGANIZED_FOLDER_PATH + SUBS_FOLDER_NAME)
        if not LST_OF_FILES_TO_MOVE_LATER:
            prompt_user_with_message("Organized Shows and Subs Folder Succesfuly:)","Order Is Everything!")
        else:
            msg = " Could not move these files to shows folder:\n\n"
            for file in sorted([item[3] for item in LST_OF_FILES_TO_MOVE_LATER]):
                msg += "  -  " + file.title() + "\n"
            msg += "\n Because they are seeding in Utorrent.\n" \
                       " Delete finished torrents in Utorrents and retry again."
            # msg += "\n\n ( You can also click on 'Organize Shows Folder'\n" \
            #        "At the 'More Options' menu at the top left corner )\n"
            prompt_user_with_message(msg,"Can't move seeding files")

    def onUpcomingEpisodes(self,event):
        global SHUTDOWN_OUTPUT_SCREEN

        try:
            msg = "How far away do you want to know the future?\n\n" \
                  "(Enter the number of days)"

            ans = prompt_user_with_text_question(message = msg,title = "Let's see what's coming up... :)")

            if not ans:
                return
            days = int(ans)
            while days > 59:
                jedi_msg = "\nEven HollyWood dont know that far....\n\n" \
                           "Try again: (maximum 59 days)"
                ans = prompt_user_with_text_question(message = jedi_msg,title = "What am I a fucking JEDI??")
                if not ans:
                    return
                days = int(ans)
            while days < 1 or days > 59:
                valid_days_msg = "Please enter a valid number of days ( 0 - 59 )"
                ans = prompt_user_with_text_question(message=valid_days_msg,title="Wrong Input")
                if not ans:
                    return
                days = int(ans)

            get_upcoming_shows(days)

            frame.panel.outPutTxtCtrl.log.Clear()
            frame.panel.outPutTxtCtrl.Show()
            frame.panel.outPutTxtCtrl.log.Raise()
            SHUTDOWN_OUTPUT_SCREEN = False

            print_upcoming_shows()

        except Exception as ex:
            errTitle = "Eror"
            errMsg = "There was an Error while getting upcoming shows.\n"
            errSolution = "Try again later. \n" \
                          "If error persists, please contact support."
            errAction = "continue"
            exception_routine(errMsg, errTitle, errSolution, errAction)

    def onContactSupport(self,event):
        try:
            contact = ContactSupport()

        except Exception as ex:
            print ex


    def onAbout(self,event):

        info = wx.AboutDialogInfo()

        description = "\nWatchMe was developed to help you manage and organize\n" \
                      "all of your favourite shows and movies.\n" \
                      "You can check out all of the current features at the\n" \
                      "'More Options' menu at the top left corner of the app.\n" \
                      "WatchMe is still in development and hopefuly more features will               \n" \
                      "be added soon. Hope you enjoy it meanwhile :)\n"

        licence = """WatchMe is free software; you can redistribute
        it and/or modify it under the terms of the GNU General Public License as
        published by the Free Software Foundation.
        However,WatchMe is not responsible for any illegal actions and the usage
        Of this application is at your own risk.

        WatchMe is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
        See the GNU General Public License for more details. You should have
        received a copy of the GNU General Public License along with WatchMe;
        if not, write to the Free Software Foundation, Inc., 59 Temple Place,
        Suite 330, Boston, MA  02111-1307  USA"""

        info.SetIcon(wx.Icon('magnet.ico', wx.BITMAP_TYPE_ANY))
        info.SetName('WatchMe')
        info.SetVersion(APP_VERSION)
        info.SetDescription(description)
        info.SetCopyright('(C) 2016 - 2017 WatchMe')
        info.SetWebSite('http://www.WatchMe.com')
        info.SetLicence(licence)
        info.AddDeveloper('Wat Chme')


        about = wx.AboutBox(info)
#---------------------------------------------------------------------------------------------
# DropBox Class
#---------------------------------------------------------------------------------------------
class DropBoxClass():

    def __init__(self):
        self.access_token = DROPBOX_ACCESS_TOKEN
        self.logs_folder_name = DROPBOX_LOG_FILES_FOLDER
        self.admin_file = DROPBOX_ADMIN_FILE
        self.watchme_installation_file_path = DROPBOX_WATCHME_INSTALL_FILE
        self.dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
        self.user_agreement_file_path = DROPBOX_TERMS_AND_CONDITIONS_PATH

    def get_admin_data_from_dropBox(self):

        try:
            # self.dbx.files_download_to_file(ADMIN_FILE_PATH,self.admin_file)
            file_from_dropBox = self.dbx.files_download(self.admin_file)
            fileData = file_from_dropBox[1].content.split("\r")

            for line in fileData:
                line = line.strip("\n").lower()
                if line != "":
                    items = line.split(' : ')
                    key = items[0]
                    val = items[1]
                    ADMIN_DIC[key] = val

            check_user_permissions()

        except Exception as ex:
            pass #if cant reach dropbox,give him free pass

            # errTitle = "Error!"
            # errMsg = "There was an Error Connecting to the internet!\n" \
            #          "Cannot proceed until you fix it\n"
            # errSolution = "Try again later"
            # errAction = "exit"
            # exception_routine(errMsg, errTitle, errSolution, errAction)

    def upload_log_to_dropbox(self,file_to_upload):
        try:
            nowTime = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            fileName = "%s/%s [%s] .txt" % (USERNAME,USERNAME, nowTime)
            with open(file_to_upload, 'rb') as f:
                self.dbx.files_upload(f.read(), DROPBOX_LOG_FILES_FOLDER + fileName)

        except Exception as ex:
            pass

    def upload_support_message(self,file_to_upload):

        try:

            nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            fileName = "{} [ {} ] .txt".format(USERNAME,nowTime)
            with open(file_to_upload,'rb') as f:
                self.dbx.files_upload(f.read(),DROPBOX_USER_MSGS_FOLDER + fileName)

        except Exception as ex:
            errTitle = "Connection Error"
            errMsg = "There was an error sending your message."
            errSolution = "Try again later"
            errAction = "continue"
            exception_routine(errMsg, errTitle, errSolution, errAction)

    def download_new_watchme_version(self):
        try:
            curr_version = APP_VERSION
            admin_version = ADMIN_DIC['version']
            if curr_version != admin_version:
                msg = "Hi %s! \n\n" \
                      "Your current version: %s\n" \
                      "Available Version: %s\n\n" \
                      "Do you want to update to the most recent version?\n" \
                        % (USERNAME,curr_version,admin_version)

                ans = prompt_user_with_question(msg,"Update WatchMe")
                if ans:

                    prompt_user_with_message( "This might take a few minutes.\n"
                                               "Click OK,  I'll tell you when I'm done :)",
                                              "Patience My Young Padawan...")

                    dbFilePath = "%s/WatchMe %s.msi" % (self.watchme_installation_file_path,admin_version)
                    newFilePath = "%s\WatchMe %s.msi" % (USER_PATH,admin_version)
                    self.dbx.files_download_to_file(newFilePath,dbFilePath)


                    prompt_user_with_message("WatchMe installation file was downloaded at:\n%s"
                                             "\n\nUninstall this version and install again from new file." % newFilePath,
                                             "I Hope you'll like the new version:) ")


            else:
                prompt_user_with_message("Your WatchMe version is up to date :) ", "All Good")

        except Exception as ex:
            errTitle = "Update Error!"
            errMsg = "There was an Error while updating WatchMe.\n"
            errSolution = "Please try again later. \n" \
                          "If error persists, please contact support."
            errAction = "stop"
            exception_routine(errMsg, errTitle, errSolution, errAction)


    def download_user_agreement(self):

        try:
            self.dbx.files_download_to_file(USER_TERMS_AND_CONDITIONS_PATH,
                                            DROPBOX_TERMS_AND_CONDITIONS_PATH)
        except Exception as ex:
            errTitle = "Download Error!"
            errMsg = "There was an Error Downloading Terms&Conditions.\n"
            errSolution = "Please try again later. \n" \
                          "If error persists, please contact support."
            errAction = "continue"
            exception_routine(errMsg, errTitle, errSolution, errAction)


#---------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------
class outputClass(wx.Frame):

    def __init__(self):

        x_pos = USER_DISPLAY_SIZE[0]/2 - 4
        y_pos = USER_DISPLAY_SIZE[1]/2 - APP_SIZE[1]/2

        wx.Frame.__init__(self, None, wx.ID_ANY, OUTPUT_SCREEN_TITLE,size=(380,505), pos=(x_pos,y_pos),
                          style = wx.CAPTION | wx.RESIZE_BORDER | wx.CLOSE_BOX)

        # Add a panel so it looks the correct on all platforms
        self.panel = wx.Panel(self, wx.ID_ANY)
        self.log = wx.TextCtrl(self.panel, wx.ID_ANY, style=wx. wx.TE_READONLY | wx.TE_MULTILINE )
        self.btn = wx.Button(self.panel, wx.ID_ANY, 'Shut Down!', size = (100,30) )
        self.Bind(wx.EVT_BUTTON, self.onButton, self.btn)
        self.Bind(wx.EVT_CLOSE,self.onCloseWindow)

        # Add widgets to a sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        # sizer.AddSpacer(10)
        sizer.Add(self.log, 1, wx.ALL | wx.EXPAND)
        sizer.Add(self.btn, 0, wx.ALL | wx.CENTER, 20)

        self.panel.SetSizer(sizer)

        # redirect text here
        redir = RedirectText(self.log)
        sys.stdout = redir
        sys.stderr = redir

        self.icon = wx.IconFromBitmap(wx.Bitmap(ICON_PATH))
        self.SetIcon(self.icon)

        # menuBar = wx.MenuBar()
        # fileMenu = wx.Menu()
        # menuBar.Append(fileMenu, "&")
        # self.SetMenuBar(menuBar)

    def onButton(self, event):
        global SHUTDOWN_OUTPUT_SCREEN

        SHUTDOWN_OUTPUT_SCREEN = True
        self.Hide()
        self.log.Clear()
        frame.panel.specialReqBtn.Enable()
        frame.panel.myEpisodesBtn.Enable()
                # raise Exception("User Terminated this thread")

    def onCloseWindow(self,event):

        frame.panel.outPutTxtCtrl.onButton("")



#------------------------------------------------------------------------------------------
# Redirect Text
#------------------------------------------------------------------------------------------
class RedirectText(object):

    def __init__(self, aWxTextCtrl):
        self.out = aWxTextCtrl

    def write(self, string):
        global SESSION_LOG_STR

        try:

            with print_lock:
                self.out.AppendText(str(string))
                SESSION_LOG_STR += string

        except Exception as ex:
            errTitle = ""
            errMsg = "I had a little printing error."
            errSolution = "Sorry, please try again later"
            errAction = "continue"
            exception_routine(errMsg, errTitle, errSolution, errAction)
#--------------------------------------------------------------------------





#---------------------------------------------------------------------------
#Scheduler
#---------------------------------------------------------------------------

class EventScheduler():

    def __init__(self,hour,minute,mode):

        self.SC = 'Daily'   #task type
        self.TN = 'WatchMe' #task name
        self.TR = USER_PATH + "\\" + APP_NAME # scheduler file path
        self.ST = "%s:%s" % (hour,minute) #start time
        self.ED = "31/12/2017" # end time

        self.mode = mode
        self.create_command = "schtasks /create /sc %s /tn %s /tr %s /st %s /ed %s /F" % \
                  (self.SC,self.TN,self.TR,self.ST,self.ED)
        self.del_command = "schtasks /delete /tn %s /F" % self.TN
        self.edit_command = "schtasks /change /TN %s /RL HIGHEST" % self.TN

        if self.mode == "create":
            self.create_task()
        elif self.mode == 'delete':
            self.delete_task()

    def create_task(self):

        try:
            # ans = os.system(command)
            # print ans
            # p = Popen(command, shell=True, stdin=PIPE)
            # time.sleep(.5)
            # ans2 = p.communicate("Y\n")
            # ans = p.stdin.write("Y\n")
            # print ans

            # p = Popen(self.create_command, shell=True, stdin=PIPE)
            # time.sleep(0.5)

            create_scheduler_task()

            prompt_user_with_message("Scheduler Activated Successfully at:  {}".format(SCHEDULER_RUN_TIME),
                                     "All Good")
            write_new_data_to_file('last_update')

        except Exception as ex:
            errTitle = "Scheduler Error!"
            errMsg = "There was an Error creating a new task.\n"
            errSolution = "Try again later. \n" \
                          "If error persists, please contact support."
            errAction = "stop"
            exception_routine(errMsg, errTitle, errSolution, errAction)

    def delete_task(self):
        global HAS_SCHEDULER

        try:
            # p = Popen(self.del_command, shell=True, stdin=PIPE)

            prompt_user_with_message("Scheduled Task Deleted Successfuly","In Case You Were Worried..")
            HAS_SCHEDULER = False
            write_new_data_to_file('last_update')

        except Exception as ex:
            prompt_user_with_message("error deleting task")

#------------------------------------------------------------------------------------
#TaskBar Icon
#------------------------------------------------------------------------------------
class TaskBarIcon(wx.TaskBarIcon):
    def __init__(self):
        super(TaskBarIcon, self).__init__()
        self.set_icon(ICON_PATH)
        self.Bind(wx.EVT_TASKBAR_RIGHT_DOWN, self.on_right_down)
        self.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.on_doubleClick)
        # self.Bind(wx.EVT_TASKBAR_LEFT_UP,self.on_right_down)


    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'Show WatchMe', self.on_doubleClick)
        create_menu_item(menu, 'Put To Sleep', self.on_sleep)
        create_menu_item(menu, 'Exit', self.on_exit)
        return menu


    def set_icon(self, path):
        icon = wx.IconFromBitmap(wx.Bitmap(path))
        self.SetIcon(icon, 'WatchMe')

    def on_right_down(self, event):
        try:
            self.menu = self.CreatePopupMenu()
            self.PopupMenu(self.menu)
            self.menu.Destroy()
        except Exception as ex:
            errTitle = ""
            errMsg = "There was an error with the task bar icon."
            errSolution = "Sorry, please try again later"
            errAction = "continue"
            exception_routine(errMsg, errTitle, errSolution, errAction)

    def on_doubleClick(self,event):
        frame.Show()
        frame.Raise()
        frame.Iconize(False)

    def on_sleep(self,event):
        put_app_to_sleep()

    def on_exit(self, event):
        if HAS_SCHEDULER:
            msg = "Are you sure you want to Exit?\n" \
                  "If you will exit, the scheduler will not be able\n" \
                  "to download your shows automatically.\n"
            ans = prompt_user_with_question(msg,"Please Dont Leave Me !")
            if ans:
                close_app_for_good()
                # frame.panel.Hide()
                # exit_thread = threading.Timer(1,("force"))
                # exit_thread.setDaemon(True)
                # exit_thread.start()
            else:
                put_app_to_sleep()

        else:
            close_app_for_good()
#------------------------------------------------------------------------------------
#ContactSupport Window
#------------------------------------------------------------------------------------

class ContactSupport(wx.Frame):

    def __init__(self):

        wx.Frame.__init__(self, frame, wx.ID_ANY, "What's On Your Mind?",
                          style=wx.CAPTION | wx.RESIZE_BORDER | wx.CLOSE_BOX ,size = (300,370), pos=(400,290))

        icon = wx.IconFromBitmap(wx.Bitmap(ICON_PATH))
        self.SetIcon(icon)

        self.panel = wx.Panel(self, wx.ID_ANY)
        self.msgToUsr = "Write down what you need and I wil do my best to help.\n"\
                        "\nFeel free to write some feedback as well :)"
        self.mailMsg = "Enter your E-Mail here so I could answer you"
        # self.Greeting = wx.StaticText(self, label=self.msgToUsr)
        self.mailBox = wx.TextCtrl(self.panel, wx.ID_ANY,  size = (300,30))
        self.messageBox = wx.TextCtrl(self.panel, wx.ID_ANY, style= wx.TE_PROCESS_ENTER | wx.TE_MULTILINE,  size = (300,170) )
        # self.messageBox.Bind(wx.EVT_TEXT_ENTER, self.onMsgEnterTxt)
        self.mailBox.Bind(wx.EVT_TEXT_ENTER, self.onMailEnterTxt)
        self.finished_constructor = False

        self.sndBtn = wx.Button(self.panel, wx.ID_ANY, 'Send Message')
        self.sndBtn.Bind(wx.EVT_BUTTON, self.onSend)
        self.Bind(wx.EVT_CLOSE,self.onClose)
        self.messageBox.Bind(wx.EVT_SET_FOCUS, self.onMsgFocus)
        self.mailBox.Bind(wx.EVT_SET_FOCUS, self.onMailFocus)

        self.mailBox.SetValue(self.mailMsg)
        self.messageBox.SetValue(self.msgToUsr)

        # Add widgets to a sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddSpacer(20)
        # sizer.Add(self.Greeting,0,wx.ALL | wx.CENTER,10)
        sizer.Add(self.messageBox, 0, wx.ALL | wx.CENTER, 10)
        sizer.AddSpacer(20)
        sizer.Add(self.mailBox, 0, wx.ALL | wx.CENTER, 10)
        sizer.Add(self.sndBtn,0,wx.ALL | wx.CENTER,10)

        # self.panel.SetSizer(sizer)
        self.panel.SetSizerAndFit(sizer)

        self.Show()
        self.Center()

        self.finished_constructor = True

    def onSend(self,event):

        txtMsg = self.messageBox.GetValue()
        if txtMsg == "" or txtMsg == self.msgToUsr:
            prompt_user_with_message("Can't send empty message.\n"
                                     "Write down what's on your mind.")
            return

        email = self.mailBox.GetValue()
        if email == "" or email == self.mailMsg:
            prompt_user_with_message("Please write down your E-Mail,\n"
                                     "So i could answer reply your message.")
            return

        msgFile = open(CLIENT_MSG_FILE_PATH,"w+")
        msgFile.write("\nUser Name : {} \n"
                      "User Email : {}".format(USERNAME,email))
        msgFile.write("\n\n{}".format(txtMsg))
        msgFile.close()

        frame.panel.dropBoxItem.upload_support_message(CLIENT_MSG_FILE_PATH)
        prompt_user_with_message("Thank you For your thoughts and comments,\n"
                                 "I will reply soon.","Message Sent Successfuly")
        self.Destroy()

    def onMsgEnterTxt(self,event):

        self.mailBox.SetFocus()

    def onMailEnterTxt(self,event):

        self.sndBtn.SetFocus()

    def onMsgFocus(self,event):
        if not self.finished_constructor:
            return

        if self.messageBox.GetValue() == self.msgToUsr:
            self.messageBox.SetValue("")
        event.Skip()


    def onMailFocus(self,event):

        if not self.finished_constructor:
            return

        if self.mailBox.GetValue() == self.mailMsg:
            self.mailBox.SetValue("")

        event.Skip()
    def onClose(self,event):
        prompt_user_with_message("Message was not sent!\n\n"
                                 "Dont be shy, try again later:)","Cold Feet?")
        self.Destroy()

#------------------------------------------------------------------------------------
#Main
#------------------------------------------------------------------------------------

def main():
    global frame
    global app
    try:

        app = wx.App(False) # start application
        read_show_file()
        t1 = threading.Thread(target = multiThreading_routine,args = (create_my_show_list,SHOWS_LIST_INPUT))
        t1.setDaemon(True)
        t1.start()



        #app.SetOutputWindowAttributes(title='Eze Picho Shahaf!', size=(380,485), pos=(675,100))
        frame = MainWindow()
        frame.create_panel()
        frame.add_menu_bar()

        if not ENABLE_SERIES_ORGANIZER:
            frame.panel.bmpbtn.Hide()

        frame.Show()

        frame.panel.start_panel_init_threads()


        icon = wx.IconFromBitmap(wx.Bitmap(ICON_PATH))
        frame.SetIcon(icon)

        # outPutTxtCtrl = outputClass()
        # if check_if_now_is_scheduler_time():
        #     frame.panel.onDownloadEpisodes("Scheduler")
        # else:

        app.MainLoop()


    except Exception as ex:
        errTitle = ""
        errMsg = "I had a big main error now =\\ I'm shutting down."
        errSolution = "If error persists, please contact support"
        errAction = "exit"
        exception_routine(errMsg, errTitle, errSolution, errAction)



main()
