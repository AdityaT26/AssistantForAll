import os
from tkinter import messagebox

def CREATE_PATH_LIST(path_list = [''], log = True):
    if isinstance(path_list, (list, tuple)):
        k=""
        for i in range(0, len(path_list)):

            if os.path.exists(k+path_list[i]) == False:
                if i+1 <= len(path_list):
                    k+=path_list[i]
                    os.mkdir(k)
                if log:
                    print('_CREATED DIRECTORY:', k)
            else:
                k+=path_list[i]
                if log:
                    print('EXISTING DIRECTORY:', k)
    else:
        messagebox.showerror('Google Assistant On Windows - ERROR', 'The Application couldn\'t be run properly!\nCouldn\'t write data to files')
        if log:
            print("COULDN'T CREATE DIRECTORY, path_list must be of type tuple, list")

def CREATE_PATH(path = "", log = True):
    path_list = path.split('\\')
    for i in range(0, len(path_list)):
        if i==len(path_list)-1:
            s = '\\'+path_list[i]+'\\'
        elif i==0 and path_list[i].count('C:')>0:
            s = path_list[i]
        else:
            s = '\\'+path_list[i]
        path_list[i] = s
        
    if isinstance(path_list, (list, tuple)):
        k=""
        for i in range(0, len(path_list)):

            if os.path.exists(k+path_list[i]) == False:
                if i+1 <= len(path_list):
                    k+=path_list[i]
                    os.mkdir(k)
                if log:
                    print('_CREATED DIRECTORY:', k)
            else:
                k+=path_list[i]
                if log:
                    print('EXISTING DIRECTORY:', k)
    else:
        messagebox.showerror('Google Assistant On Windows - ERROR', 'The Application couldn\'t be run properly!\nCouldn\'t write data to files')
        if log:
            print("COULDN'T CREATE DIRECTORY")
            print("Path sould be in the form of: '<Drive>:\\ParentDir\\SubDir1\\SubDir2\\SubDir3\\SubDirN' ")

# example

#credSavePath_sub_list = [os.getenv('APPDATA'),'\\AonW','\\data','\\api','\\apiAccess','\\userGrant','\\Auth','\\OAuthCreds','\\Generated\\']
#CREATE_PATH_LIST(credSavePath_sub_list)

#credSavePath = os.getenv('APPDATA')+'\\AonW\\data\\api\\apiAccess\\userGrant\\Auth\\OAuthCreds\\Generated\\credentials'
#CREATE_PATH(credSavePath)
