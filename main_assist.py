import requests
import pyttsx3
import speech_recognition as sr
import datetime
import os
import cv2
import wikipedia 
import webbrowser
import smtplib
from email.message import EmailMessage
import openai
import pywhatkit

# Initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Set your OpenAI API key
openai.api_key = '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'
# weather api key
weather_api_key = 'd1f71b66eea8564931b9d31327151821'

# Text to speech
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Speech to text
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=7)
        
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-IN')
        print(f"User said: {query}")
    except Exception as e:
        print(e)
        print("Sir, please say that again...")
        speak("Sir, please say that again...")
        return "None"
    return query

def wish():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning, sir!")
    elif 12 <= hour < 18:
        speak("Good afternoon, sir!")
    else:
        speak("Good evening, sir!")
    speak("I am Friday your assistant. How can I help you?")

def chatgpt(prompt):
    global last_response
    full_prompt = f"Sir: {last_response}\nAssistant: {prompt}"
    response = openai.Completion.create(
      engine="gpt-3.5-turbo-instruct",
      prompt=full_prompt,
      temperature=0.5,
      max_tokens=100
    )
    last_response = response.choices[0].text.strip()
    return last_response
  
# Function to send email
def send_email(subject, body, to_email):
    sender_email = "sumanjain.jbp@gmail.com"  # Enter your email
    sender_password = "qxfo rkkk lmsk hxcg"  # Enter your password

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email
    msg.set_content(body)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print("Failed to send email.")
        print(e)

def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey=38d0854f10e644d18e96b91ce1698fca"
    response = requests.get(url)
    data = response.json()
    if data["status"] != "ok":
        return "Sorry, I couldn't fetch the news."
    articles = data["articles"]
    if not articles:
        return "Sorry, there are no articles available."
    news_data = []
    for i, article in enumerate(articles[:5]):
        title = article["title"]
        url = article["url"]
        description = article["description"]
        news_data.append((title, url, description))
    return news_data

def speak_news():
    engine = pyttsx3.init()
    engine.say("Fetching the latest news for you.")
    engine.runAndWait()
    
    news_data = get_news()
    for i, (title, url, description) in enumerate(news_data):
        news = f"News {i+1}. Title: {title}. Description: {description}"
        print(f"Title: {title}\nURL: {url}\nDescription: {description}")
        engine.say(news)
        engine.runAndWait()

if __name__ == "__main__":
    wish()
    last_response = ""
    while True:
        query = take_command().lower()
        
        # Add your command processing logic here

        if "write an email" in query:
            speak("Whom do you want to send an email?")
            recipient = take_command().replace(" dot ", ".").replace(" ", "").lower() + "@gmail.com"
            print(recipient)
            speak("What should be the subject of the email?")
            subject = take_command().lower()
            speak("Please dictate the content of the email.")
            content = take_command().lower()

            if recipient != "none" and subject != "none" and content != "none":
                send_email(subject, content, recipient)
                speak("Email has been sent successfully.")

        elif "open notepad" in query:
            npath = "C:\\Windows\\system32\\notepad.exe" 
            os.startfile(npath)
            speak("Opening notepad, sir...")


        elif "open command prompt" in query or "open cmd"  in query:
            os.system("start cmd")
            speak("Opening command prompt")
        
        elif "close command prompt" in query or "close cmd"  in query:
             os.system("taskkill /f /im cmd.exe")
             speak("Command prompt closed")
                

        elif "wikipedia" in query or "google" in query:
            speak("Searching for given query")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)


        elif "open edge" in query :
            speak("Opening edge")
            speak("Sir, what should I search?")
            cm = take_command().lower()
            webbrowser.open(f"{cm}")
            

        elif "open facebook" in query:
            webbrowser.open("www.facebook.com")
            speak("Opening Facebook, sir")  
                    
        elif "open youtube and search for" in query:
            speak("Opening YouTube and seraching for videos, sir")
            query = query.replace("open youtube and search for", "")
            query = query.replace("open youtube", "")
            query = query.replace("friday", "")
            web = "https://www.youtube.com/results?search_query=" +  query
            webbrowser.open(web)
            pywhatkit.playonyt(query)
                                    
        elif "what is the time" in query :
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            speak(f"Sir, the time is {hour} and {min} minutes")
       
            
        elif "open spotify and search for " in query:
            speak("Opening Spotify, sir and serching for your songs")
            query = query.replace("open spotify and search for ", "")
            query = query.replace("open spotify", "")
            query = query.replace("friday", "")
            web = "https://open.spotify.com/search/" +  query
            webbrowser.open(web)
            
           


        elif"open whatsapp" in query:
             speak("opening what's app,Sir")
             webbrowser.open('https://web.whatsapp.com/')

        elif"open instagram" in query:
             speak("opening intsagram,Sir")
             webbrowser.open('https://www.instagram.com/?hl=en')
#intreagating gpt 1 can we chat
        elif "can we chat" in query or "help me" in query or "give me information" in query or "can we chat" in query:
            speak("Sure sir, why not. What is the topic?")
             
            while True:
                user_prompt = take_command().lower()
                if user_prompt == "stop":
                    speak("Ok sir, You're welcome! If you have any more questions or if there's anything else I can assist you with, feel free to ask.")
                    print("Goodbye Sir, have a nice day!")
                    break
                elif user_prompt != "none":
                    response = chatgpt(user_prompt)
                    print(response)
                    speak(response)
#intregating weather of area
       
        elif "what is the weather today" in query or " friday what is the weather" in query or "what is the weather" in query or " friday what is the today weather" in query or "weather" in query or "can you tell me the today weather" in query or "what is the today weather" in query:
            speak("Sure, which city's weather would you like to know?")
            city_query = take_command().lower()
            city = city_query.capitalize()
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
            response = requests.get(url)
            weather_data = response.json()
            if weather_data["cod"] == 200:
                weather_description = weather_data["weather"][0]["description"]
               
                temperature = weather_data["main"]["temp"]
                
                humidity = weather_data["main"]["humidity"]
                
                wind_speed = weather_data["wind"]["speed"]
                
                speak(f"The weather in {city} is {weather_description}. Temperature is {temperature} degrees Celsius, humidity is {humidity}%, and wind speed is {wind_speed} meters per second.")
                print(f"The weather in {city} is {weather_description}. Temperature is {temperature} degrees Celsius, humidity is {humidity}%, and wind speed is {wind_speed} meters per second.")
         
        elif "news" in query:
            speak_news()
         


        elif "end program" in query or "exit" in query or "quit" in query or "sleep" in query:
             speak("Ending the program. Goodbye Sir, have a nice day!, if you have any problem i am there for you ")
             break  