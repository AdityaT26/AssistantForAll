import os
import dropbox
from threading import Thread
import DEBUG as dbg

TOKEN="-XQIBbW2PR8AAAAAAAAAASqPiQbZb9cYyp2Klbzi8439QFhgEMfToAVU0SzFI60R"

DBX = dropbox.Dropbox(TOKEN)

# PKG = 'AonW_zfyfk01jren8p'
PKG = '44520AdityaT.AonWAssistantonWindows_6b21v8kbxxjsp'


WindowsStore = not dbg.DEBUG

DEBUG = dbg.DEBUG

font = "@Malgun Gothic Semilight"

'''class PathVar():
    path = ''
'''

#def getPkgName(path=PathVar.path, i=0):
def getPkgName(path, i):

    if i<=10:
        metadata, res = DBX.files_download(path='/AonW/PackageName/pkg.txt')
        content=res.content
        pkg = str(content)
        pkg = pkg.split("'")
        pkg = pkg[1]
        print(pkg)

        dataPath.htmlPath = path+'Local\\Packages\\'+pkg+'\\LocalCache\\Roaming\\AonW\\data'

        if os.path.exists(dataPath.htmlPath):
            dataPath.htmlPath = ''
            #getPkgName(path=path, i=i+1)
            getPkgName(path, i+1)
    else:
        dataPath.htmlPath = ''

class dataPath():

    if not DEBUG:

        if not WindowsStore:
            dataPath = os.path.join(os.getenv('APPDATA'), 'AonW\\data')
            htmlPath = os.path.join(os.getenv('APPDATA'), 'AonW\\data')
        else:
            dataPath = os.path.join(os.getenv('APPDATA'), 'AonW\\data')
            htmlPath = ''

            pkg = PKG

            try:

                s = os.getenv('APPDATA')
                print(s)
                print(s.split('\\'))
                s=s.split('\\')
                path=''
                for i in range(0, len(s)-1):
                    path+=s[i]+'\\'

                htmlPath = path+'Local\\Packages\\'+pkg+'\\LocalCache\\Roaming\\AonW\\data'
                dataPath = htmlPath

                if not os.path.exists(htmlPath):

                    htmlPath = ''

                    s = os.getenv('APPDATA')
                    print(s)
                    print(s.split('\\'))
                    s=s.split('\\')
                    path=''
                    for i in range(0, len(s)-1):
                        path+=s[i]+'\\'

                    t = Thread(target = lambda:getPkgName(path, 0))
                    t.daemon = True
                    t.start()
                    print(path)

                    '''
                    PathVar.path = path

                    #t = Thread(target = lambda:getPkgName())
                    #t.daemon = True
                    #t.start()
                    getPkgName()
                    print(path)
                    htmlpath = path
                    '''

                print(htmlPath)

            except:
                pass

            # C:\Users\Aditya Thakur\AppData\Local\Packages\AonW_zfyfk01jren8p\LocalCache\Roaming\AonW\data

    else:
        dataPath = os.getcwd()
        htmlPath = os.getcwd()

print(WindowsStore)
print(DEBUG)
print("................")
print(dataPath.dataPath)
print("................")
print(dataPath.htmlPath)
print("................")
