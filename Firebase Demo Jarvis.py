import sys
import pyrebase
from PyQt5.uic import loadUi 
from PyQt5 import QtWidgets 
from PyQt5.QtWidgets import QWidget, QApplication, QWidget
import pyttsx3
import datetime
import speech_recognition as sr
import webbrowser
import os
import pyautogui 


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)
engine.setProperty('rate',170)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()



def wishMe():
    hour = (datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        print("Good Morning ! I'm Zira. How can i help you")
        speak("Good Morning ! I'm Zira. How can i help you")        
    elif hour>=12 and hour<18:
        print("Good Afternoon ! I'm Zira. How can i help you")
        speak("Good Afternoon ! I'm Zira. How can i help you")
    else:
        print("Good Evening ! I'm Zira. How can i help you")
        speak("Good Evening ! I'm Zira. How can i help you")

def time():
        strTime = datetime.datetime.now().strftime("%H:%M:%S") 
        print(strTime)  
        speak(f"yeah , the time is {strTime}") 
def date():
        strDate = datetime.datetime.now().strftime("%D:%M:%Y") 
        print(strDate)  
        speak(f"yeah , the date is {strDate}")  

def honor():
    print("Thanks , its mean a lot for me")
    speak("Thanks , its mean a lot for me")


firebaseConfig = {
    "apiKey": "AIzaSyBPM7ipv1InUbI3WMID_dl85bIQbtjkgx8",
    "authDomain": "fir-project-6296a.firebaseapp.com",
    "projectId": "fir-project-6296a",
    "storageBucket": "fir-project-6296a.appspot.com",
    "messagingSenderId": "865347308501",
    "appId": "1:865347308501:web:27b4e91c993f0a9dd08b5c",
    "measurementId": "G-45TV349NP7",
    "databaseURL": " "
}


firebase=pyrebase.initialize_app(firebaseConfig)
auth=firebase.auth()




class firstpage(QWidget):
    def __init__(self):
       super(firstpage, self).__init__()
       loadUi("firstpage.ui", self)
       self.pushButton.clicked.connect(self.gotoSignIn)

    def gotoSignIn(self):
        signInPage = SignInPage()
        widget.addWidget(signInPage)
        widget.setCurrentIndex(widget.currentIndex()+1) 


class SignInPage(QWidget):
    def __init__(self):
        super(SignInPage, self).__init__()
        loadUi("signinpage.ui", self)
        self.pushButton.clicked.connect(self.signInfunction)


    def signInfunction(self):
        email = self.lineEdit.text()
        password = self.lineEdit_2.text()
        if len(email) == 0 and len(password) == 0:
            self.label_2.setText("Enter Your Email and Password")
        elif len(email) == 0:
            self.label_2.setText("Enter Your Email")
        elif len(password) == 0:
            self.label_2.setText("Enter Your Password")
        try:
            user = auth.create_user_with_email_and_password(email, password)
            print("Successfully signed in:", user['email'])
            self.onsignin()
        except Exception as e:
            print("Sign In failed:", e)

    

    def onsignin(self):
        speak("I am active now and ready to assist you ")
        self.ListenForCommand()


    def takeCommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("I'm Listening....")
            r.pause_threshold = 1
            audio = r.listen(source)
        try:
            print("recognising....")
            query = r.recognize_google(audio, language='eng=pak')
            print(f"you said: {query}\n")
        except Exception as e:
            print(e)
            print("I can't understand please Say that again ...")
            speak("I can't understand please Say that again ...")
            return "None"
        return query     
    
    

    def ListenForCommand(self):
        print("I am active now and ready to assist you ")
        while True:
            query = self.takeCommand() .lower()
            if 'Hye ' in query:    
               wishMe()
            elif'the time' in query:
               time()
            elif 'the date' in query:
               date()
            elif'well done' in query:
               honor()      
            elif'open google' in query:
               print("Yeah google is open now")
               speak("Yeah google is open now")
               webbrowser.open("google.com") 
               speak("Done!")     
            elif'open youtube' in query:
               print("Yeah youtube is open now")
               speak("Yeah youtube is open now")
               webbrowser.open("youtube.com") 
               speak("Done!") 
            elif'open firefox' in query:
               print("Yeah firefox is open now")
               speak("Yeah firefox is open now")
               webbrowser.open("Firefox.com")  
               speak("Done!")         
            elif"open" in query:
                query = query.replace("open","")
                query = query.replace("Zira","")
                pyautogui.press("super")
                pyautogui.typewrite(query)
                pyautogui.sleep(2)
                pyautogui.press("enter") 
                speak("Done!")   
            elif'goodbye' in query:
                print("GoodBye, Have a Nice day!")
                speak("GoodBye, Have a Nice day!")
                exit()  
            elif'good night' in query:
                print("Good Night! Have a sweet dreams")
                speak("Good Night! Have a sweet dreams") 
                exit()        

    
#interface
app = QtWidgets.QApplication(sys.argv)
firstpage = firstpage()
widget = QtWidgets.QStackedWidget()
widget.addWidget(firstpage)
widget.setFixedWidth(700)
widget.setFixedHeight(600)
widget.show()
sys.exit(app.exec_())


