from google_auth_oauthlib.flow import Flow
import os
import create_path
from time import sleep
from tkinter import messagebox
import threading
import http.server
from os import path
from urllib.parse import unquote
import sys

import dataPath as dp

DTP = dp.dataPath.dataPath

# Create the flow using the client secrets file from the Google API
# Console.

class Token():
    askToken = False
    token = ""
    authUrl = ""
    success = False
    error = False
    credSavePath = os.getenv('APPDATA')+'\\AonW\\data\\api\\apiAccess\\userGrant\\Auth\\OAuthCreds\\Generated\\credentials.cred'

my_html_folder_path = r'Y:\Stuff\Python\Assistant\Contents\Test\cefpyex\New_sign_in_method'

my_home_page_file_path = 'page.html'

class Vars():
    TOKEN = ""
    done = False

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        #self.send_header('Content-Length', path.getsize('Y:\Stuff\Python\Assistant\Contents\Test\cefpyex\page.html'))
        self.send_header('Content-Length', path.getsize(os.path.join(resource_path(''),"page.html")))
        pathg = str(self.path)
        if pathg.count('page.html')==0 and path!='':
            print("BRUH:",pathg)
            if pathg=='/done':
                #os._exit(0)
                Vars.done = True
                pass
            else:
                Vars.TOKEN = pathg
        self.end_headers()

    def getPath(self):
        if self.path == '/':
            content_path = path.join(
                my_html_folder_path, my_home_page_file_path)
        else:
            content_path = path.join(my_html_folder_path, str(self.path).split('?')[0][1:])
        return content_path

    def getContent(self, content_path):
        with open(content_path, mode='r', encoding='utf-8') as f:
            content = f.read()
        return bytes(content, 'utf-8')

    def do_GET(self):
        pathg = self.getPath()
        self._set_headers()
        print('------------------------')
        print(os.path.join(resource_path(''),"page.html"))
        print('------------------------')
        #self.wfile.write(self.getContent('Y:\Stuff\Python\Assistant\Contents\Test\cefpyex\page.html'))
        self.wfile.write(self.getContent(os.path.join(resource_path(''),"page.html")))
        
        #retrieve function here

class StoppableHTTPServer(http.server.HTTPServer):
    def run(self):
        try:
            self.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            # Clean-up server (close socket, etc.)
            self.server_close()

def createCreds():
    try:
        clientsecret = {
            "installed":{
                "client_id":"1039137964337-t38704t8sb6eoiatdp77goiga300hnkc.apps.googleusercontent.com",
                "project_id":"diva-a802e",
                "auth_uri":"https://accounts.google.com/o/oauth2/auth",
                "token_uri":"https://accounts.google.com/o/oauth2/token",
                "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
                "client_secret":"Yc2Rz7ubqbJ9QDjpOTkF6rxc",
                #"redirect_uris":["urn:ietf:wg:oauth:2.0:oob","http://localhost"]
                "redirect_uri":"http://localhost:3000"
            }
        }

        flow = Flow.from_client_secrets_file_dict(
            client_secrets_file=clientsecret,
            scopes=['https://www.googleapis.com/auth/assistant-sdk-prototype'],
            #redirect_uri='urn:ietf:wg:oauth:2.0:oob',
            redirect_uri='http://localhost:8888',
            )

        # Tell the user to go to the authorization URL.
        #auth_url, _ = flow.authorization_url(prompt='consent')
        auth_url, _ = flow.authorization_url(prompt=None, save = True, headless=True)

        print('Please go to this URL: {}'.format(auth_url))

        # The user will get an authorization code. This code is used to get the
        # access token.
        #code = input('Enter the authorization code: ').strip()
        Token.authUrl = auth_url
        Token.askToken = True

        my_handler = MyHttpRequestHandler
        server = StoppableHTTPServer(("localhost", 8888),
                                    my_handler)

        # Start processing requests
        thread = threading.Thread(None, server.run)
        thread.start()

        while Vars.done==False:
            print(".", end='')
            sleep(0.5)
            pass

        code = unquote(Vars.TOKEN)

        code = code[code.index('code=')+5: code.index('&scope')]

        print(code)

        # Shutdown server
        server.shutdown()
        thread.join()

        Token.token = code

        flow.fetch_token(code=code)

        # You can use flow.credentials, or you can just get a requests session
        # using flow.authorized_session.
        session = flow.authorized_session()
        print('.............................................................')
        #print(session.get('https://www.googleapis.com/userinfo/v2/me').json())
        #print(session.credentials.refresh_token)
        """s = '''
        {
            "refresh_token": "'''+session.credentials.refresh_token+'''", 
            "token_uri": "'''+session.credentials.token_uri+'''", 
            "client_id": "'''+session.credentials.client_id+'''", 
            "client_secret": "'''+session.credentials.client_secret+'''", 
            "scopes": '''+str(session.credentials.scopes).replace('\'','"')+'''
        }
        '''"""

        s = session.credentials.refresh_token

        print(s)

        credSavePath_sub_list = [os.getenv('APPDATA'), '\\AonW','\\data','\\api','\\apiAccess','\\userGrant','\\Auth','\\OAuthCreds','\\Generated\\']

        create_path.CREATE_PATH_LIST(path_list=credSavePath_sub_list, log=False)

        #credSavePath = os.getenv('APPDATA')+'\\AonW\\data\\api\\apiAccess\\userGrant\\Auth\\OAuthCreds\\Generated\\credentials.cred'
        credSavePath = Token.credSavePath

        h = open(credSavePath, 'w+')
        h.write(s)
        h.close()

        '''
        create_path.CREATE_PATH(DTP+"\\Assets\\", log=False)

        h = open(DTP+"\\Assets\\key.key", 'w+')
        h.write('This file was created wehn you logged in to Assistant on Windows(AonW)\n\
        If you delete this file, you would be asked to re-sign in\n\
        as this file allows the program to check if the user is signed in\n\
        into google-assistant with their account.')
        h.close()
        '''

        print('Credentials saved to: '+credSavePath)
        Token.success=True
    except:
        Token.success=False
        Token.error=True
        messagebox.showerror('Google Assistant On Windows - Auth ERROR', 'Failed to login, Restart application to retry')
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
