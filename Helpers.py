import os
import sys
import threading
from time import sleep
import Errors
import time
import pickle

def strip_filename_from_path(path):
    return os.path.basename(path)

def get_folder_of_path(full_filename):
    return os.path.dirname(full_filename)

def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print '%r (%r, %r) %2.2f sec' % \
              (method.__name__, args, kw, te-ts)
        return result

    return timed

def multiThreading_routine(func_name, relevant_list):

    try:
        threads = [threading.Thread(target=func_name, args=(item,)) for item in relevant_list]
        for t in threads:
            t.setDaemon(True)
            t.start()
            sleep(0.3)
            # if func_name is download_my_shows:
            #     time.sleep(0.3)
            # elif func_name is get_subtitle_file:
            #     time.sleep(0.3)
            # elif func_name is download_exact_subtitles:
            #     time.sleep(0.3)
        for t in threads:
            t.join()
    except Exception as ex:
        raise Errors.MultiThreadingError(ex,item)

def load_pickle_object(pickle_file_path):

    if not os.path.exists(pickle_file_path):
        raise Errors.DataBaseNotFound()

    file_ob = open(pickle_file_path, 'r')
    pickle_obj = pickle.load(file_ob)
    file_ob.close()
    return pickle_obj

def dump_to_pickle_object(pickle_file_path,object_to_dump):
    file_ob = open(pickle_file_path, "w+")
    pickle.dump(object_to_dump, file_ob)
    file_ob.close()


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
