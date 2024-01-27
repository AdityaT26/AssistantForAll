from tkinter import Tk, Canvas, Label, PhotoImage
import os
from DataSets import loadSettings, Settings
from threading import Thread
from time import sleep

import dataPath as dp

DTP = dp.dataPath.dataPath


def close():
    pass

def Off(root):
    while os.path.exists(DTP+'\\start.start')==False:
        pass
    sleep(1)
    os.remove(DTP+'\\start.start')
    root.destroy()

def start():

    try:

        loadSettings()

        rootI = Tk()

        rootI.minsize(400, 200)
        rootI.resizable(0, 0)
        rootI.title('Google Assistant On Windows - Loading')

        try:
            icon = PhotoImage(file = "icon.png")
            rootI.iconphoto(False, icon)
        except:
            pass

        fg = 'black'
        bg = 'white'

        if Settings.theme == 'light':
            bg = 'white'
        else:
            bg = '#212121'
            fg = '#aed9e6'

        canvas = Canvas(rootI, bg = bg)
        canvas.place(relx=0, rely=0, relheight=1, relwidth=1)

        '''Gimg = ImageTk.PhotoImage(Image.open(DTP+"\Assets\Icons\G.png").resize((60,60), Image.ANTIALIAS))
        Limg = Label(rootI, image=Gimg)
        Limg.pack(pady=20)'''

        Lab1 = Label(canvas, borderwidth=10, text="Google Assistant on Windows", font=(dp.font, 22), bg = bg, fg= fg)
        Lab1.pack(pady=10)


        Lab2 = Label(canvas, borderwidth=10, text="Your Assistant is Loading", font=(dp.font, 24), bg = bg, fg= fg)
        Lab2.pack(pady=10)

        rootI.protocol("WM_DELETE_WINDOW", lambda:close())

        t = Thread(target = lambda:Off(rootI))
        t.daemon = True
        t.start()

        rootI.mainloop()

    except:
        pass
        print('Intro Error')

        try:
            h = open(DTP+'\\start.start', 'w+')
            h.close()
        except:
            pass

        #messagebox.showerror('Google Assistant On Windows - ERROR', 'The Application couldn\'t be run properly!')