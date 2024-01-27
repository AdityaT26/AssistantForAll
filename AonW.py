import Text
import Voice
import time
import DataSets
import threading
import GUI
from os import getenv, _exit
import create_path

from tkinter import messagebox

import dataPath as dp

DTP = dp.dataPath.dataPath

credSavePath_sub_list = [getenv('APPDATA'), '\\AonW', '\\data']

create_path.CREATE_PATH_LIST(path_list=credSavePath_sub_list, log=False)

DataSets.loadSettings()

TEXTPUT  = DataSets.Settings.Text
VOICEPUT = DataSets.Settings.Voice

if TEXTPUT and not VOICEPUT:
    try:
        t = threading.Thread(target = lambda: Text.main())
        t.daemon=True
        t.start()
        while DataSets.Dataset_Text.begin==False and DataSets.Command.CredentialsReq == False:
            pass
    except:
        print('Invalid, credentials, re sign-in required')
elif TEXTPUT and VOICEPUT:
    try:
        t = threading.Thread(target = lambda: Text.main())
        t.daemon=True
        t.start()
        tv = threading.Thread(target = lambda: Voice.main())
        tv.daemon=True
        tv.start()
        while (DataSets.Dataset_Text.begin==False or DataSets.Dataset_Voice.begin==False) and DataSets.Command.CredentialsReq == False:
            pass
    except:
        print('Invalid, credentials, re sign-in required')
elif not TEXTPUT and VOICEPUT:
    try:
        tv = threading.Thread(target = lambda: Voice.main())
        tv.daemon=True
        tv.start()
        while DataSets.Dataset_Voice.begin==False and DataSets.Command.CredentialsReq == False:
            pass
    except:
        print('Invalid, credentials, re sign-in required')

def start():

    tg = threading.Thread(target = lambda: GUI.start(DataSets.Command.CredentialsReq))
    tg.daemon=True
    tg.start()

    while True:
        time.sleep(2)
        if DataSets.Quit:
            break
    _exit(0)

if __name__== "__main__":
    try:
        start()
    except:
        messagebox.showerror('Google Assistant On Windows - ERROR', 'The main Application couldn\'t be run properly!')
        try:
            h = open(DTP+'\\start.start', 'w+')
            h.close()
        except:
            pass
        import traceback, sys

        # Get current system exception
        ex_type, ex_value, ex_traceback = sys.exc_info()

        # Extract unformatter stack traces as tuples
        trace_back = traceback.extract_tb(ex_traceback)

        # Format stacktrace
        stack_trace = list()

        for trace in trace_back:
            stack_trace.append("File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))

        print("Exception type : %s " % ex_type.__name__)
        print("Exception message : %s" %ex_value)
        print("Stack trace : %s" %stack_trace)