from tkinter import Tk, END
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

import dataPath as dp

DTP = dp.dataPath.dataPath

def close(root):
    root.destroy()

def start(*args):

    try:

        root = Tk()

        root.resizable(0, 0)

        try:
            root.iconphoto(False, args[0])
        except:
            pass

        root.minsize(300, 400)
        root.title("Assistant on Windows - About")

        about = """
        Thanks for downloading this app!
        \n
        \n
            My name is Aditya Thakur and I am a high school developer.\n
            \n
                    As we all know how useful the Google Assistant really\n
            is. We use it for many of our everyday tasks, for example, asking it\n
            to retrieve some information from the web, controlling our\n
            appliances, sending a quick text to someone, and also to read\n
            the news.\n
            \n
                    Many of us are mainly working on our desktops/laptops\n
            and would love to access the assistant's power without being able\n
            to reach our phones which can cause distraction. This thought\n
            is what resulted in the creation of this application, also\n
            called Assistant on Windows or AonW.\n
            \n
                    Also this is my first ever main stream project and there\n
            will be more applictions coming which will be developed by me.\n
            \n
                    To help me through my journey, a donation through paypal\n
            by pressing the donate button in the home screen will be greatly\n
            appreciated :).\n
            \n
            Aditya Thakur (Developer)\n
            Contact : adit.thakur26@gmail.com
            LinkedIn : https://www.linkedin.com/in/aditya-t-357b3b1b2
            \n
            *************************************************************
            \n
            The G Logo, Mic Logo and the Assistant API and core are all\n
            the property of Google.
            \n
            Font used: """+dp.font+"""
            \n
            This application comes with NO warranty whatsoever.\n
            \n
        """

        About = ScrolledText(root, font=(dp.font, 14), fg = args[1], bg = args[2])
        About.tag_configure("left", justify="left")
        About.pack(padx=1, pady=5)
        About.insert(END, about)
        About.config(state='disabled')

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
