from tkinter import *
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import os
import dropbox 
import sys
from threading import Thread
import DEBUG as dbg
import dataPath as dp

DTP = dp.dataPath.dataPath

HTP = dp.dataPath.htmlPath

DEBUG = dbg.DEBUG

ver = '1.1.2.0'

class Vars():
    token = "-XQIBbW2PR8AAAAAAAAAASqPiQbZb9cYyp2Klbzi8439QFhgEMfToAVU0SzFI60R"
    dbx   = None
    exe   = False
    doneUpdt = None

def close(root):
    if Vars.doneUpdt:
        root.destroy()
    else:
        pass

def fileFormatter(response):
    vers=''
    title = ''
    versLS={}
    for file in response.entries:
        s=file.name
        try:
            vers = s[0:s.index('(')]
        except:
            vers[0:(len(s)-4)]
        versLS[vers]=s

    vers = sorted(versLS.keys(), reverse = True)[0]
    fname = sorted(versLS.values(), reverse = True)[0]
    versLS = sorted(versLS.keys(), reverse = True)
    try:
        title = fname[fname.index('(')+1:fname.index(')')]
    except:
        pass

    return vers, fname, title, versLS

def chkUpdates():
    try:

        updt = False

        abt = None
        
        temp =  os.path.basename(sys.argv[0])
        if(temp.endswith('exe')):
            Vars.exe=True

        if(Vars.exe):
            response = Vars.dbx.files_list_folder("/updates_aonw_exe/")
            vers, fname, title, versLS = fileFormatter(response)
            metadata, res = Vars.dbx.files_download(path='/updates_aonw_exe/'+fname)
            abt=res.content

        else:
            response = Vars.dbx.files_list_folder("/updates_aonw/")
            vers, fname, title, versLS = fileFormatter(response)
            metadata, res = Vars.dbx.files_download(path='/updates_aonw/'+fname)
            abt=res.content

        print(versLS)
        print(versLS.count(vers))

        if abt == None:
            abt = 'Update Available ~ '+vers

        if(vers>ver):
            updt = True
        else:
            print("APPLICATION UP-TO-DATE")

        if versLS.count(vers) >=2 :
            return updt, vers, abt, title, fname
        else:
            return updt, 'read', abt, title, fname
    except:
        print("except")
        if(True):

            import traceback

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
        return False, '', '', '', ''
            
def updateApp(vers, laterBt, updtBt, root):

    print('Updating to ', vers)

    root.title("Assistant on Windows - Updating to version "+vers+" .....")

    try:

        if(Vars.exe):

            temp =  os.path.basename(sys.argv[0])

            filename=''

            for i in range(0,len(temp)-3):
                filename+=temp[i]
            
            h=open(filename+"temp", "w+")
            h.close()

            with open(filename+"temp", "wb") as f:
                metadata, res = Vars.dbx.files_download(path="/updates_aonw_exe/"+vers+".exe")
                f.write(res.content)
            f.close()
            os.rename(filename+"exe", "DeleteThis"+"temp2")
            os.rename(filename+"temp", filename+"exe")
            #return True, filename
        else:
            temp =  os.path.basename(sys.argv[0])

            filename=''

            for i in range(0,len(temp)-3):
                filename+=temp[i]
            
            with open(filename+".py", "wb") as f:
                metadata, res = Vars.dbx.files_download(path="/updates_aonw/"+vers+"f.py")
                f.write(res.content)
            f.close()
            #return True, filename+".py"
            pass

        updtSuccess = Label(root, text="Update Successful!! Restart App to Apply", padx=10, bg="White", fg="#4287f5" \
                         ,font=(dp.font, 20))
        updtSuccess.place( relx=0.15, rely=0.83 )

        root.title("Assistant on Windows - Update Successful")

        Vars.doneUpdt = True
            
    except:

        root.title("Assistant on Windows - Update Failed")

        updtFailed = Label(root, text="Update Failed, Nothing has been changed.", padx=10, bg="White", fg="#f7922d" \
                         ,font=(dp.font, 20))
        updtFailed.place( relx=0.1, rely=0.83 )
            
        print(" ERROR UPDATING, NOT AFFECTED")
        if(DEBUG):

            import traceback

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

        Vars.doneUpdt = True

        return False, ''


def updtThd(vers, laterBt, updtBt, root):

    updtBt.destroy()
    laterBt.destroy()

    t = Thread(target = lambda: updateApp(vers, laterBt, updtBt, root))
    t.daemon = True
    t.start()


def start(vers, abt, title, fetchAndDisplay, *args):

    try:

        if fetchAndDisplay:
            metadata, res = Vars.dbx.files_download(path='/updates_aonw/'+abt)
            abt=res.content

        root = Tk()

        bg = args[0]
        fg = args[1]
        abg = args[2]
        afg = args[3]

        try:
            root.iconphoto(False, args[0])
        except:
            pass

        root.minsize(600, 400)

        root.resizable(0, 0)

        root.title("Assistant on Windows - Update")

        root.lift()
        root.attributes("-topmost", True)
        root.attributes("-topmost", False)


        canvas = Canvas(root, bg="#212121")
        canvas.place(relx = 0, y = 0, height = 300, width = 600)

        about = abt

        About = ScrolledText(canvas, font=(dp.font, 14), bg=bg, fg=fg)
        About.tag_configure("left", justify="left")
        About.pack(padx=5, pady=5)
        About.insert(END, about)
        About.config(state='disabled')

        if vers != 'read':

            laterBt = Button(root, text="Remind me Later", padx=10, bg=bg, fg=fg, activeforeground=afg, \
                        activebackground=abg ,font=(dp.font, 20), \
                        command= lambda : root.destroy())
            laterBt.place( relx=0.1, rely=0.8 )

            updtBt = Button(root, text="Update Now", padx=10, bg=bg, fg=fg, activeforeground=afg, \
                        activebackground=abg ,font=(dp.font, 20), \
                        command= lambda : updtThd(vers, laterBt, updtBt, root))
            
            updtBt.place( relx=0.6, rely=0.8 )
        
        else:
            root.title("Google Assistant on Windows - Message: "+title)
            Vars.doneUpdt = True
            canvas = Canvas(root, bg="#212121")
            canvas.place(relx=0, y=300, height=100, relwidth=1)

            laterBt = Button(canvas, text="Sure!", padx=10, bg=bg, fg=fg, activeforeground=afg, \
                        activebackground=abg ,font=(dp.font, 20), \
                        command= lambda : root.destroy())
            laterBt.place( relx=0.43, rely=0.19 )

        root.protocol("WM_DELETE_WINDOW", lambda:close(root))

        root.mainloop()

    except:
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

        messagebox.showerror('Google Assistant On Windows - ERROR', 'The Application couldn\'t be run properly!')

        try:
            h = open(HTP+'\\start.start', 'w+')
            h.close()
        except:
            pass

Vars.dbx = dropbox.Dropbox(Vars.token)