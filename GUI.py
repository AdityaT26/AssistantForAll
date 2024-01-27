import os
import time
import threading
from tkinter import *
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from PIL import ImageTk, Image
import webbrowser
import DataSets
import settings
import about
import update
import loadCreds
from tkinter import messagebox
import intro
import create_path
import sys
import DEBUG as dbg

import dataPath as dp

DTP = dp.dataPath.dataPath

HTP = dp.dataPath.htmlPath
#HTP = dp.dataPath.dataPath

DEBUG = dbg.DEBUG

class ResizingCanvas(Canvas):
    def __init__(self,parent,**kwargs):
        Canvas.__init__(self,parent,**kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height

        # resize the canvas 
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all",0,0,wscale,hscale)

class Vars():
    # Vars.
    root = None
    canvas = None
    micLogo = None
    micBt = None
    bg = '#ffffff'
    fg = 'black'
    abg = '#686870'
    afg = '#f7922d'
    inactive = None
    active = None
    browserFrame = None
    driver = None
    username = os.getlogin().replace(' ','%20')
    GLogoR = None
    GLogoInactive = None
    GLogoActive = None
    GLabel = None
    txtAr = None
    txtInpAr = None
    menubar = None
    Notif = None
    send_bt = None
    donate_bt = None
    #paypal = "https://paypal.me/NalinThakur58?country.x=IN&locale.x=en_GB"  #DAD's
    paypal = "https://paypal.me/AdityaThakur26?locale.x=en_GB"              #MINE        

def dummy():
    pass

def clearFile(file):
    if len(file)>18:
        h = open(file, 'w+')
        h.write('')
        h.close()

def postLoginAttempt(link, goToLabel, SignIn_Bt):
    Vars.root.title('Google Assistant on Windows - Signing In')
    Vars.root.lift()
    Vars.root.attributes("-topmost", True)
    Vars.root.attributes("-topmost", False)
    while loadCreds.Token.success == False:
        if loadCreds.Token.error:
            break
        time.sleep(0.2)

    if loadCreds.Token.success:
        Vars.root.title('Google Assistant on Windows - Success')

        link.destroy()
        SignIn_Bt.destroy()

        goToLabel = Label(Vars.canvas, text="Success!!\n\nRestart The App to \nTalk\nwith your assistant!!", fg="#4287f5",bg = Vars.bg, font=(dp.font, 35))
        goToLabel.place(relx=0.1, rely=0.1, height = 500, relwidth=0.8)
    
    else:

        link.destroy()
        SignIn_Bt.destroy()
    
        goToLabel = Label(Vars.canvas, text="An Error Occurred\nAn error occurred\nwhile signing in\ntry again later", fg="#f7922d",bg = Vars.bg, font=(dp.font, 38))
        goToLabel.place(relx=0.1, rely=0.1, height = 600, relwidth=0.8)

def loadCredsBt(SignIn_Bt):
    SignIn_Bt.config(state='disabled', font=(dp.font, 17))
    SignIn_Bt.place(rely = 0.14, relx=0.28, height=55, width=220)
    ttoken = threading.Thread(target = lambda : loadCreds.createCreds())
    ttoken.daemon = True
    ttoken.start()

    while loadCreds.Token.askToken == False:
        time.sleep(0.2)

    goToLabel = Label(Vars.canvas, text="Trying to open link\n if it doesn't open go to:", font=(dp.font, 18), bg='white')
    goToLabel.place(relx=0.1, rely=0.23, height = 100, relwidth=0.8) 
    link=ScrolledText(Vars.canvas, fg="#4287f5", width=70, height=90, font=(dp.font, 18))
    link.place(relx=0.1, rely=0.36, height = 90, relwidth=0.8) 
    link.insert(END, loadCreds.Token.authUrl)
    #link.insert(END, 'https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=1039137964337ri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fassistant-sdk-protot_type=offline')
    link.config(state = 'disabled')

    #Vars.driver.open_new_tab('https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=1039137964337ri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fassistant-sdk-protot_type=offline')
    turl = threading.Thread(target = lambda:web_out(loadCreds.Token.authUrl))
    turl.daemon = True
    turl.start()

    while loadCreds.Token.token=="":
        pass
        time.sleep(0.5)
    postLoginAttempt(link, goToLabel, SignIn_Bt)


def on_enter(e):
    Vars.micBt['image'] = Vars.active

def on_leave(e):
    Vars.micBt['image'] = Vars.inactive

def web_out(html):
    webbrowser.open_new_tab(html)

def RespondAnim():
    cd = 50
    while True:
        while DataSets.Dataset_Voice.speak==1:
            for i in range(50, 61, 2):
                bloat = ImageTk.PhotoImage(Vars.GLogoR.resize((i, i), Image.ANTIALIAS))
                Vars.GLabel["image"] = bloat
                cd = i
            for i in range(60, 49, -2):
                bloat = ImageTk.PhotoImage(Vars.GLogoR.resize((i, i), Image.ANTIALIAS))
                cd = i
                Vars.GLabel["image"] = bloat
            time.sleep(0.8)
        if cd>50:
            cd = 50  
            Vars.GLabel["image"] = Vars.GLogoInactive

def switchSpeak(*args):
    if DataSets.Dataset_Voice.speak==0:
        DataSets.Dataset_Voice.speak=1
        Vars.txtAr.config(state='normal')
        Vars.txtAr.insert(END, "Listening\n")
        Vars.txtAr.config(state='disabled')
        Vars.txtAr.see("end")

def close():
    if os.path.exists(HTP+"\\htmlRs.html"):
        clearFile(HTP+"\\htmlRs.html")
        #os.remove(HTP+"\\htmlRs.html")
    if os.path.exists(HTP+"\\htmlRsTemp.html"):
        clearFile(HTP+"\\htmlRsTemp.html")
        #os.remove(HTP+"\\htmlRsTemp.html")
    Vars.root.destroy()
    DataSets.Quit = True
    os._exit(0)

def queryVoice():
    while True:
        #time.sleep(1.5)
        time.sleep(0.5)
        if DataSets.Dataset_Voice.request["query"]!="":
            Vars.txtAr.config(state='normal')
            Vars.txtAr.insert(END, "<You>: "+DataSets.Dataset_Voice.request["query"]+"\n")
            DataSets.Dataset_Voice.request["query"]=""
            Vars.txtAr.config(state='disabled')
            Vars.txtAr.see("end")

def queryText():
    while True:
        time.sleep(0.5)
        if DataSets.Dataset_Text.response["processing"]:
            Vars.send_bt.config(state='disabled')
            DataSets.Dataset_Voice.speak=1
        elif DataSets.Dataset_Text.response["response"]!="" and DataSets.Dataset_Text.response["processing"]==False:
            DataSets.Dataset_Voice.speak=0
            Vars.txtAr.config(state='normal')
            Vars.txtAr.insert(END, "<Assistant>: "+DataSets.Dataset_Text.response["response"]+"\n")
            Vars.txtAr.config(state='disabled')
            Vars.txtInpAr.delete("1.0", END)
            DataSets.Dataset_Text.response["response"]=""
            Vars.send_bt.config(state='normal')
            Vars.txtAr.see("end")

def setQueryText(*args, **kwargs):
    DataSets.Dataset_Text.request["request"]=Vars.txtInpAr.get("1.0", END)
    Vars.txtAr.config(state='normal')
    Vars.txtAr.insert(END, "\n<You>: "+Vars.txtInpAr.get("1.0", END)+"\n")
    Vars.txtAr.config(state='disabled')
    Vars.txtInpAr.delete("1.0", END)
    Vars.txtAr.see("end")

def setRawMsg(msg):
    Vars.txtAr.config(state='normal')
    Vars.txtAr.insert(END, "\n"+msg+"\n")
    Vars.txtAr.config(state='disabled')
    Vars.txtAr.see("end")

def getMessage(fname):
    print(fname)
    title = fname[fname.index('(')+1:fname.index(')')]
    fetchAndDisplay = True
    update.start('read', fname, title, fetchAndDisplay, Vars.bg, Vars.fg, Vars.abg, Vars.afg)

def addNotif(i):
    titleold = i[i.index('(')+1:i.index(')')]
    Vars.Notif.add_command(label=titleold, command = lambda:getMessage(i))

def checkUpdate():
    
    u, v, abt, title, fname= update.chkUpdates()

    print(u, v, title)

    #if u:
    #    print('Update available ~ ',v)
    #    update.start(vers = v, abt = abt)
    print(DTP+"\\Assets\\notifs")
    with open(DTP+"\\Assets\\notifs", 'a') as h:
        pass
    print(DTP)
    with open(DTP+"\\Assets\\notifs", 'r') as h:
        notifs = h.readlines()
   
    for i in range(len(notifs)):
        j = notifs[i]
        notifs[i] = j[0:len(j)-1]
    
    print(notifs)

    while Vars.Notif==None:
        time.sleep(0.3)

    for i in notifs:
        #titleold = i[i.index('(')+1:i.index(')')]
        #Vars.Notif.add_command(label=titleold, command = lambda:getMessage(i))
        addNotif(i)
    

    if v == 'read' and fname not in notifs:
        update.start(v, abt, title, False, Vars.bg, Vars.fg, Vars.abg, Vars.afg)
        with open(DTP+"\\Assets\\notifs", 'a') as h:
            h.write(fname+'\n')
        Vars.Notif.add_command(label=title, command = lambda:getMessage(fname))

def logout():
    if os.path.exists(loadCreds.Token.credSavePath):
        os.remove(loadCreds.Token.credSavePath)
    Vars.root.title('Google Assistant on Windows - Restart App to Logout')

def setTheme():
    
    with open(DTP+"\\Assets\\theme", 'w+') as h:
        if DataSets.Settings.theme == 'light':
            h.write('dark')
        else:
            h.write('light')
    Vars.root.title('Google Assistant on Windows - Restart App to Change Theme')

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def start(*args):

    try:
        print('GUI START')

        Vars.root = Tk()
        #Vars.root = Toplevel()
        Vars.root.minsize(500, 500)
        Vars.root.lift()
        Vars.root.attributes("-topmost", True)

        DataSets.loadSettings()

        credSavePath_sub_list = [os.getenv('APPDATA'), '\\AonW', '\\data']

        create_path.CREATE_PATH_LIST(path_list=credSavePath_sub_list, log=False)

        if DataSets.Settings.theme == 'light':
            Vars.bg = '#ffffff'
            Vars.fg = 'black'
            Vars.abg = 'White'
        else:
            Vars.bg = '#212121'
            Vars.fg = '#aed9e6'
            Vars.abg = '#686870'
        
        Vars.root.title('Google Assistant on Windows')
        Vars.root.minsize(500, 500)
        Vars.root.attributes("-topmost", False)

        tu = threading.Thread(target = lambda: checkUpdate())
        tu.daemon=True
        tu.start()

        icon = None
        if DEBUG:
            try:
                icon = PhotoImage(file = "icon.png")
                Vars.root.iconphoto(False, icon)
            except:
                print('Iconset - False')
        else:
            try:
                icon = PhotoImage(file = os.path.join(resource_path('.'),"icon.png"))
                Vars.root.iconphoto(False, icon)
            except:
                print('Iconset - False')


        tint = threading.Thread(target = lambda: intro.start())
        tint.daemon=True
        tint.start()

        #Vars.canvas = ResizingCanvas(Vars.root, width=520, height=750, bg=Vars.bg, highlightthickness=0)
        Vars.canvas = ResizingCanvas(Vars.root, width=520, height=650, bg=Vars.bg, highlightthickness=0)
        Vars.canvas.pack(fill=BOTH, expand=YES)

        if DEBUG:
            Vars.micLogo = Image.open("mic.png")
            Vars.GLogoR = Image.open("G.png")
        else:
            Vars.micLogo = Image.open(os.path.join(resource_path('.'),"mic.png"))
            Vars.GLogoR = Image.open(os.path.join(resource_path('.'),"G.png"))

        Vars.inactive = ImageTk.PhotoImage(Vars.micLogo.resize((55, 80), Image.ANTIALIAS))
        Vars.active = ImageTk.PhotoImage(Vars.micLogo.resize((65, 90), Image.ANTIALIAS))
        Vars.GLogoInactive = ImageTk.PhotoImage(Vars.GLogoR.resize((50, 50), Image.ANTIALIAS))
        Vars.GLogoActive = ImageTk.PhotoImage(Vars.GLogoR.resize((60, 60), Image.ANTIALIAS))

        Vars.donate_bt=tk.Button(Vars.canvas, text="Donate :)", padx=5, bg=Vars.bg, fg="#4287f5", activeforeground=Vars.afg, \
                    activebackground=Vars.abg ,font=(dp.font, 20), \
                    command= lambda : web_out(Vars.paypal))
        Vars.donate_bt.place(height=40, relx=0.69, rely=0.02)

        if args[0]==False:

            print('Credentials Found!')

            print('HTP = "'+HTP+'"')

            clearFile(HTP+"\\htmlRs.html")
            clearFile(HTP+"\\htmlRsTemp.html")

            if os.path.exists(HTP+"\\htmlRs.html"):
                clearFile(HTP+"\\htmlRs.html")
                #os.remove(HTP+"\\htmlRs.html")
            if os.path.exists(HTP+"\\htmlRsTemp.html"):
                clearFile(HTP+"\\htmlRsTemp.html")
                #os.remove(HTP+"\\htmlRsTemp.html")
            if os.path.exists(HTP+"\\DeleteThistemp2"):
                clearFile(HTP+"\\DeleteThistemp2")
                #os.remove(HTP+"\\DeleteThistemp2")

            Vars.txtAr=ScrolledText(Vars.canvas, state='normal', bg=Vars.bg, fg=Vars.fg, font=(dp.font, 17))
            scrollbar = Scrollbar(Vars.canvas, orient='horizontal') 
            scrollbar.place(rely=0.8, relwidth=1)
            Vars.txtAr.config(xscrollcommand=scrollbar.set)
            scrollbar.config(command = Vars.txtAr.xview, bg = Vars.bg)
            Vars.txtAr.place(relx=0, rely=0.12, relheight=0.7, relwidth=1)

            if DataSets.Settings.Voice:
                print('Voice GUI starting')
                tv = threading.Thread(target = lambda: queryVoice())
                tv.daemon=True
                tv.start()

                Vars.micBt = tk.Button(Vars.canvas, text="Speak", padx=10, bg=Vars.bg, image=Vars.inactive, activebackground=Vars.bg, command= lambda:switchSpeak())
                Vars.micBt["border"] = "0"
                Vars.micBt.place(height=90, width=65, relx=0.44, rely=0.85)

                Vars.micBt.bind("<Enter>", on_enter)
                Vars.micBt.bind("<Leave>", on_leave) 
                print('Voice GUI started')
            else:
                tv = threading.Thread(target = lambda: queryText())
                tv.daemon=True
                tv.start() 

                Vars.txtInpAr=ScrolledText(Vars.canvas, fg="#4287f5", bg=Vars.bg, width=70, height=100, font=(dp.font, 18))
                Vars.txtInpAr.place(relx=0.01, rely=0.85, height = 90, relwidth=0.8) 

                Vars.send_bt=tk.Button(Vars.canvas, text="Ask", padx=10, bg=Vars.bg, fg="#4287f5", activeforeground=Vars.afg, \
                    activebackground="White" ,font=(dp.font, 20), \
                    command= lambda : setQueryText())
                Vars.send_bt.place(height=35, width=60, relx=0.85, rely=0.87)

            print('Configuring GLogo')
            Vars.GLabel = Label(Vars.root, image=Vars.GLogoInactive, bg=Vars.bg)
            Vars.GLabel.place(width=60, height=60, relx=0.01, rely=0.01 )
            print('Configured GLogo')

            print('Configuring Menu Bar')
            Vars.menubar = Menu(Vars.root)
            Settings = Menu(Vars.menubar, tearoff=0)
            Settings.add_command(label="Preferences", command=lambda:settings.start(icon))
            Vars.menubar.add_cascade(label="Settings", menu=Settings)

            About = Menu(Vars.menubar, tearoff=0)
            About.add_command(label="About This App", command=lambda:about.start(icon, Vars.fg, Vars.bg))
            Vars.menubar.add_cascade(label="About", menu=About)

            Logout = Menu(Vars.menubar, tearoff=0)
            Logout.add_command(label="Logout (Takes Effect On App Restart)", command = lambda:logout())
            Vars.menubar.add_cascade(label="Logout", menu=Logout)

            Theme = Menu(Vars.menubar, tearoff=0)
            if DataSets.Settings.theme == 'dark':
                Theme.add_command(label="Light ☀ (Takes Effect On App Restart)", command=lambda:setTheme())
            else:
                Theme.add_command(label="Dark ☾ (Takes Effect On App Restart)", command=lambda:setTheme())
            Vars.menubar.add_cascade(label="Theme", menu=Theme)

            Vars.Notif = Menu(Vars.menubar, tearoff=0)
            Vars.menubar.add_cascade(label="Notifications", menu=Vars.Notif)

            Vars.root.config(menu=Vars.menubar)
            print('Configured Menu Bar')

            print('Configuring Animations')
            tl = threading.Thread(target = lambda: RespondAnim())
            tl.daemon=True
            tl.start()
            print('Configured Animations')

            print('Configuring Chat Area')
            if DataSets.Settings.Voice:
                Vars.txtAr.insert(END, "Google Assistant(only querries are shown in Voice mode)\n")
            else:
                Vars.txtAr.insert(END, "Google Assistant\n")
            Vars.txtAr.config(state='disabled')
            print('Configured Chat Area')

            if DataSets.Settings.enterSend:
                if DataSets.Settings.Voice:
                    #Vars.micBt.bind("<Return>", on_enter)
                    Vars.root.bind('<Return>', switchSpeak)
                else:
                    Vars.root.bind('<Return>', setQueryText)

            h = open(DTP+'\\start.start', 'w+')
            h.close()

        else:

            Vars.GLabel = Label(Vars.root, image=Vars.GLogoInactive, bg=Vars.bg)
            Vars.GLabel.place(width=60, height=60, relx=0.01, rely=0.01 )

            chrome = DataSets.Settings.browserPath
            webbrowser.register("wb", None, webbrowser.BackgroundBrowser(chrome))
            webbrowser.get("wb")

            Vars.menubar = Menu(Vars.root)
            Settings = Menu(Vars.menubar, tearoff=0)
            Settings.add_command(label="Preferences", command=lambda:settings.start())
            Vars.menubar.add_cascade(label="Settings", menu=Settings)

            About = Menu(Vars.menubar, tearoff=0)
            About.add_command(label="About This App", command=lambda:about.start(icon, Vars.fg, Vars.bg))
            Vars.menubar.add_cascade(label="About", menu=About)

            Vars.root.config(menu=Vars.menubar)

            SignIn_Bt =  Button(Vars.canvas, text="Sign-In With Google", padx=10, bg=Vars.bg, fg="#4287f5", activeforeground=Vars.afg, \
                    activebackground=Vars.abg ,font=(dp.font, 30), \
                    command= lambda : loadCredsBt(SignIn_Bt))
            SignIn_Bt.place(rely = 0.2, relx=0.12, height=100, width=400)

            SignInLabel = Label(Vars.canvas, text="Clicking the Sign-In\nbutton will take you\nto your browser.", fg="#f7922d",bg = Vars.bg, font=(dp.font, 28))
            SignInLabel.place(relx=0.1, rely=0.45, height = 150, relwidth=0.8) 

            h = open(DTP+'\\start.start', 'w+')
            h.close()

        Vars.root.protocol("WM_DELETE_WINDOW", lambda:close())

        Vars.root.mainloop()
    
    except:

        print('An ERROR Occurred -GUI')
        

        try:

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

            rootE = Tk()

            rootE.minsize(400, 200)
            rootE.resizable(0, 0)
            rootE.title('Google Assistant On Windows - ERROR')

            canvas = Canvas(rootE, bg = Vars.bg)
            canvas.place(relx=0, rely=0, relheight=1, relwidth=1)

            Lab1 = Label(canvas, borderwidth=10, text="Google Assistant on Windows", font=(dp.font, 24), bg = 'white')
            Lab1.pack(pady=10)


            Lab2 = Label(canvas, borderwidth=10, text="An ERROR Occurred", font=(dp.font, 24), bg = 'white')
            Lab2.pack(pady=10)

            rootE.mainloop()

        except:
            messagebox.showerror('Google Assistant On Windows - GUI_ERROR', 'The Application couldn\'t be run properly!')

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
