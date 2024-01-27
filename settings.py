from tkinter import *
from DataSets import Settings
from DataSets import loadSettings
from tkinter import messagebox

import os

import dataPath as dp

DTP = dp.dataPath.dataPath

def ToggleHTML():
    if Settings.html:
        Settings.html = False
    else:
        Settings.html = True

def ToggleIntegratedHTML():
    if Settings.integratedHTML:
        Settings.integratedHTML = False
    else:
        Settings.integratedHTML = True

def ToggleEnterSend():
    if Settings.enterSend:
        Settings.enterSend = False
    else:
        Settings.enterSend = True


def VoiceOp():
    Settings.Voice=True
    Settings.Text=False
def TextOp():
    Settings.Voice=False
    Settings.Text=True

class BP_Var():
    BrwPth = None

def close(root):
    if os.path.exists(DTP+"\\Assets\\settings.cfg"):
        os.remove(DTP+"\\Assets\\settings.cfg")
    with open(DTP+"\\Assets\\settings.cfg", 'w+') as h:
        set=""
        if Settings.Voice:
            set+="voice\n"
        else:
            set+="text\n"
        if Settings.html:
            set+="htmlON\n"
        else:
            set+="htmlOFF\n"
        if Settings.integratedHTML:
            set+="integratedHTMLON\n"
        else:
            set+="integratedHTMLOFF\n"
        if Settings.enterSend:
            set+="EnterSendON\n"
        else:
            set+="EnterSendOFF\n"
        set+=BP_Var.BrwPth.get()+'\n'
        Settings.browserPath = BP_Var.BrwPth.get()
        h.write(set)
    root.destroy()

class Theme():
    fg = None
    bg = None

def start(*args):

    try:

        loadSettings()

        root = Tk()

        try:
            root.iconphoto(False, args[0])
        except:
            pass
        
        Theme.fg = 'black'
        Theme.bg = 'white'

        if Settings.theme == 'dark':
            Theme.fg = '#aed9e6'
            Theme.bg = '#212121'

        root.minsize(300, 400)

        root.resizable(0, 0)

        root.title("Assistant on Windows - Settings")

        canvas = Canvas(root, bg = Theme.bg)
        canvas.pack()

        C1 = Checkbutton(canvas, text = "Web Response", command = lambda: ToggleHTML(), \
                    onvalue = 1, offvalue = 0, height=2, \
                    width = 20, font=(dp.font, 18), cursor = 'dot', bg =Theme.bg, fg = Theme.fg, activebackground = Theme.bg, activeforeground = Theme.fg, selectcolor=Theme.bg)

        C2 = Checkbutton(canvas, text = "Integrated Web Response\n(Experimental-TextOnly)", command = lambda: ToggleIntegratedHTML(), \
                    onvalue = 1, offvalue = 0, height=2, \
                    width = 20, font=(dp.font, 18), cursor = 'dot', bg =Theme.bg, fg = Theme.fg, activebackground = Theme.bg, activeforeground = Theme.fg, selectcolor=Theme.bg)

        C3 = Checkbutton(canvas, text = "Enter To ASK", command = lambda: ToggleEnterSend(), \
                    onvalue = 1, offvalue = 0, height=2, \
                    width = 20, font=(dp.font, 18), cursor = 'dot', bg =Theme.bg, fg = Theme.fg, activebackground = Theme.bg, activeforeground = Theme.fg, selectcolor=Theme.bg)

        if Settings.html:
            C1.select()
        if Settings.integratedHTML:
            C2.select()
        if Settings.enterSend:
            C3.select()

        C1.pack(padx=5, pady=5)
        C2.pack(padx=5, pady=5)
        C3.pack(padx=5, pady=5)

        BP_Var.BrwPth = Entry(canvas, font=(dp.font, 15), width = 60, bg = Theme.bg, fg=Theme.fg)
        LP = Label(canvas, text="Browser Path: (should end with \' %s\')",  font=(dp.font, 15), bg = Theme.bg, fg =Theme.fg)
        LP.pack()
        BP_Var.BrwPth.insert(0, Settings.browserPath)
        BP_Var.BrwPth.pack(pady=5)

        V = Radiobutton(canvas, borderwidth=10, text="Voice Input", value=1,\
            font=(dp.font, 24), cursor = 'dot', command=lambda:VoiceOp(), bg =Theme.bg, fg = Theme.fg, activebackground = Theme.bg, activeforeground = Theme.fg, selectcolor=Theme.bg)
        T = Radiobutton(canvas, borderwidth=10, text="Text Input (WebResponse Recommended)", value=0,\
            font=(dp.font, 24), cursor = 'dot', command=lambda:TextOp(), bg =Theme.bg, fg = Theme.fg, activebackground = Theme.bg, activeforeground = Theme.fg, selectcolor=Theme.bg)

        V.pack(pady=5, padx=10, anchor=W)
        T.pack(pady=5, padx=10, anchor=W)

        if Settings.Voice:
            V.select()
        else:
            T.select()

        WLabel = Label(canvas, font=(dp.font, 20), text="Restart App To Apply Changes", bg = Theme.bg, fg =Theme.fg)
        WLabel.pack(padx=5, pady=5)

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
            h = open(DTP+'\\start.start', 'w+')
            h.close()
        except:
            pass

