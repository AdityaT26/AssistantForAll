import os
import dropbox
from tkinter import messagebox, PhotoImage
import dataPath as dp
from webbrowser import open_new_tab

DTP = dp.dataPath.dataPath

Quit = False

TOKEN="-XQIBbW2PR8AAAAAAAAAASqPiQbZb9cYyp2Klbzi8439QFhgEMfToAVU0SzFI60R"

DBX = dropbox.Dropbox(TOKEN)

try:

    class Dataset_Text():
        begin = False
        HTML_Debug = False
        request  = { "request" : ""}
        response = { "processing" : False, "response" : "", "response-html" : ""}

    class Dataset_Voice():
        begin = False
        request = { "request" : False, "query" : ""}
        response = {"response-html" : ""}
        speak = 0

    class Settings():
        enterSend = False
        html = False
        Voice = True
        Text = False
        integratedHTML = False
        browserPath = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
        #theme = "#212121"
        #theme = '#ffffff'
        theme = 'light'

    class Command():
        On = False
        send = False
        CredentialsReq = False
    
    class Etc():
        icon = None

    def loadSettings():

        if os.path.exists(DTP+"\\Assets\\")==False:
            os.mkdir(DTP+"\\Assets\\")

        '''if os.path.exists(DTP+"\\Assets\\Icons\\")==False:
            os.mkdir(DTP+"\\Assets\\Icons\\")'''
        
        '''
        if os.path.exists(DTP+"\\Assets\\Icons\\mic.png")==False:
            with open(DTP+"\\Assets\\Icons\\mic.png", "wb") as f:
                metadata, res = DBX.files_download(path='/AonW/mic.png')
                content=res.content
                f.write(content)'''

        '''if os.path.exists(DTP+"\\Assets\\Icons\\icon.dat")==False:
            with open(DTP+"\\Assets\\Icons\\icon.dat", "wb") as f:
                metadata, res = DBX.files_download(path='/AonW/icon.png')
                content=res.content
                f.write(content)'''

        '''if os.path.exists(DTP+"\\Assets\\Icons\\chromedriver.exe")==False:
            with open(DTP+"\\Assets\\Icons\\chromedriver.exe", "wb") as f:
                metadata, res = DBX.files_download(path='/AonW/chromedriver.exe')
                content=res.content
                f.write(content)'''

        '''if os.path.exists(DTP+"\\Assets\\Icons\\G.png")==False:
            with open(DTP+"\\Assets\\Icons\\G.png", "wb") as f:
                metadata, res = DBX.files_download(path='/AonW/G.png')
                content=res.content
                f.write(content)'''

        if os.path.exists(DTP+"\\Assets\\settings.cfg"):
            try:
                f = ''
                with open(DTP+"\\Assets\\settings.cfg", 'r') as h:
                    f=h.read()
                f=f.split('\n')
                if f[0]=='text':
                    Settings.Text=True
                    Settings.Voice=False
                else:
                    Settings.Text=False
                    Settings.Voice=True
                if f[1].endswith('ON'):
                    Settings.html=True
                else:
                    Settings.html=False
                if f[2].endswith('ON'):
                    Settings.integratedHTML=True
                    Dataset_Text.HTML_Debug=True
                else:
                    Settings.integratedHTML=False
                    Dataset_Text.HTML_Debug=False
                if f[3].endswith('ON'):
                    Settings.enterSend=True
                else:
                    Settings.enterSend=False
                Settings.browserPath = f[4]

                with open(DTP+"\\Assets\\theme", 'r') as h:
                    f=h.read()
                if f.lower() == 'light':
                    Settings.theme = 'light'
                else:
                    Settings.theme = 'dark'
                '''with open('ran.txt', 'a') as h:
                    pass'''
            except Exception as e:
                print("PATH EXISTS - READ ERROR: ", e)
                with open(DTP+"\\Assets\\settings.cfg", 'w+') as h:
                    h.write('voice\nhtmlON\nintegratedHTMLOFF\nEnterSendON\nC:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s\n')
                with open(DTP+"\\Assets\\theme", 'w+') as h:
                    h.write('light')
        else:
            print("PATH DOESN'T EXIST")
            with open(DTP+"\\Assets\\settings.cfg", 'w+') as h:
                h.write('voice\nhtmlON\nintegratedHTMLOFF\nEnterSendON\nC:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s\n')
            with open(DTP+"\\Assets\\theme", 'w+') as h:
                h.write('light')
except:
    messagebox.showerror('Google Assistant On Windows - ERROR', 'The Application couldn\'t be run properly!\nData Handling Exception')

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
