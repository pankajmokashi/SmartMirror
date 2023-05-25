from tkinter import *
import time
import feedparser
from datetime import datetime
import datetime as dt
import requests 
import subprocess
import pywhatkit
import webbrowser
import os
import music
import pyttsx3
import speech_recognition as sr
import subprocess
from subprocess import Popen
from threading import Thread
import calendar

from PIL import Image, ImageTk

def main_screen():
    main_screen = Tk()
    main_screen.geometry("800x800")
    main_screen.title("Project")
    main_screen.configure(bg = 'Black')
   
    def showdate():
        date = dt.datetime.now()
        w = Label(main_screen, text=f"{dt.datetime.now():%a, %b %d %Y}", fg="white", bg="black", font=("helvetica", 30, 'bold'))
        w.place(x=1500, y=55)
        
   
    def digitalclock():
       label = Label(main_screen, font = ("Courier", 40, 'bold'), bg = 'Black', fg = 'White')
       label.place(x=1500, y=115)
       text_input = time.strftime("%H:%M:%S")
       label.configure(text = text_input)
       label.after(1000, digitalclock)

    def newsinfo():
        label1 = Label(main_screen,text="News", font = ("Courier", 23, 'bold'), bg = 'Black', fg = 'White')
        label1.place(x=60, y=730)
       
        newsLbl = Label(main_screen, font=("Courier", 18, 'bold'), fg="white", bg="black")
        newsLbl.place(x=60, y=780)
        newsLbl.headlinesContainer = Frame(newsLbl, bg="black")
        newsLbl.headlinesContainer.pack(side=TOP)
        headlines_url = "https://news.google.com/news?ned=ind&output=rss"
        feed = feedparser.parse(headlines_url)
        for post in feed.entries[0:5]:
            headline = NewsHeadline(newsLbl.headlinesContainer, post.title)
            headline.pack(side=TOP, anchor=W)  

    class NewsHeadline(Frame):
        def __init__(self, parent, event_name=""):
            Frame.__init__(self, parent, bg='black')

            self.eventName = event_name
            self.eventNameLbl = Label(self, text=self.eventName, font=('Helvetica', 17), fg="white", bg="black")
            self.eventNameLbl.pack(side=LEFT, anchor=S)
   
           
    def show_weather():
        label1 = Label(main_screen,text="Pune City", font = ("Courier", 35, 'bold'), bg = 'Black', fg = 'White')
        label1.place(x=60, y=1)
       
        API_KEY = 'ba2d767c7354ee6337b93936ec909c9a'
        city = 'Pune'
        base_url = "http://api.openweathermap.org/data/2.5/weather?appid=" + API_KEY + "&q=" + city;
        weather_data=requests.get(base_url).json()
       
        label = Label(main_screen, font = ("Courier", 23, 'bold'), bg = 'Black', fg = 'White')
        label.place(x=60, y=80)
       
        z=weather_data["weather"]
        weather_description = z[0]["description"]
       
        temp_k = float(weather_data['main']['temp'])
        temp_f = round(temp_k - 273.15, 2)
       
        text_input = str(temp_f) +"C  "+ str(weather_description) +"\nHumidity:"+ str(weather_data['main']['humidity'])
        label.config(text = text_input)

    def callback(url):
        webbrowser.open_new_tab(url)
    
    link = Label(main_screen, text="Touch Menu",font=("Courier", 35, 'bold'), bg = 'Black', fg="White", cursor="hand2")
    link.place(x = 1500, y = 250) 
    
    #Create a Label to display the link
    link = Label(main_screen, text="Gmail",font=('Helveticabold', 25), bg = 'Black', fg="White", cursor="hand2")
    link.place(x = 1500, y = 300)
    link.bind("<Button-1>", lambda e:
    callback("https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox"))

    link = Label(main_screen, text="News",font=('Helveticabold', 25), bg = 'Black', fg="White", cursor="hand2")
    link.place(x = 1500, y = 350)
    link.bind("<Button-1>", lambda e:
    callback("https://www.google.com/search?q=news&rlz=1C1CHZO_enIN917IN917&oq=news&aqs=chrome..69i57j0i67i433j0i67i131i433j0i131i433i512j0i67j69i60j69i61l2.3643j0j7&sourceid=chrome&ie=UTF-8"))
    
    link = Label(main_screen, text="Music",font=('Helveticabold', 25), bg = 'Black', fg="White", cursor="hand2")
    link.place(x = 1500, y = 400)
    link.bind("<Button-1>", lambda e:
    callback(music.play_music()))
    
    link = Label(main_screen, text="Calculator",font=('Helveticabold', 25), bg = 'Black', fg="White", cursor="hand2")
    link.place(x = 1500, y = 450)
    link.bind("<Button-1>", lambda e:
    callback(os.system('python calculator.py')))
    
    link = Label(main_screen, text="Play Game",font=('Helveticabold', 25), bg = 'Black', fg="White", cursor="hand2")
    link.place(x = 1500, y = 500)
    link.bind("<Button-1>", lambda e:
    callback(os.system('python game.py')))
    
    
    def close_screen(e):
        main_screen.destroy()
        
    main_screen.bind('<Escape>', lambda e: close_screen(e))
    
    def close_gui():
        main_screen.destroy()
        
    Button(main_screen, text="X", font=('Helveticabold', 12), bg = 'Black', fg="White", command = close_gui).place(x = 1800, y = 1000)
    
    showdate()
    digitalclock()
    newsinfo()
    show_weather()
    
    
    main_screen.attributes('-fullscreen', True)
    main_screen.mainloop()
    
def cmd():
    engine=pyttsx3.init()
    voices=engine.getProperty('voices')
    engine.setProperty('voice',voices[1].id)
    recognizer=sr.Recognizer()

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source,duration=0.5)
        print('Ask me anything..')
        recordedaudio=recognizer.listen(source)
    try:
        text=recognizer.recognize_google(recordedaudio,language='en_US')
        text=text.lower()
        print('Your message:',format(text))

        if 'alexa search' in text:
            b="opening" + text[13:len(text)]
            engine.say(b)
            engine.runAndWait()
            audio=text[13:len(text)]
            print("You said : {}".format(audio))
            url='https://www.google.co.in/search?q='
            search_url=url+audio
            webbrowser.open(search_url)
        else:
            print("Can't recognize")
        
            
        if 'alexa open youtube' in text:
            audio = text[10:len(text)]
            c="opening" + audio
            engine.say(c)
            engine.runAndWait()
            print("You said : {}".format(audio))
            url= 'https://www.youtube.com/'
            webbrowser.open(url)
        else:
            print("Can't recognize")
                
                
        if 'alexa open netflix' in text:
            audio = text[10:len(text)]
            d="opening" + audio
            engine.say(d)
            engine.runAndWait()
            print("You said : {}".format(audio))
            url= 'https://www.netflix.com/in/'
            webbrowser.open(url)
           
        else:
            print("Can't recognize")
                

        if 'alexa open calendar' in text:
            audio = text[10:len(text)]
            d="opening" + audio
            engine.say(d)
            engine.runAndWait()
            print("You said : {}".format(audio))
            url= 'https://calendar.online/3697d0a63c0a67e2361e'
            webbrowser.open(url)
            
        else:
            print("Can't recognize")
        
        
        if 'alexa play music' in text:
            audio = text[10:len(text)]
            d="opening" + audio
            engine.say(d)
            engine.runAndWait()
            music.play_music()
            
        else:
            print("Can't recognize")
            
        if 'alexa play game' in text:
            audio = text[10:len(text)]
            d="opening" + audio
            engine.say(d)
            engine.runAndWait()
            os.system('python game.py')
            
        else:
            print("Can't recognize")

        if 'alexa close' in text:
            subprocess.call("taskkill /im firefox.exe /f")
        else:
            print("Can't recognize")
            
        if 'alexa quit' in text:
            subprocess.call("taskkill /im firefox.exe /f")
        else:
            print("Can't recognize")
            
        if '' in text:
            print("Can't recognize")
        elif(len(text) == 0):
            print("Can't recognize")
        else:
            print("Can't recognize")
            
                 
    except Exception as ex:
            print(ex)
    
    while True:
        cmd()

if __name__ == '__main__':
    Thread(target = main_screen).start()
    Thread(target = cmd).start()