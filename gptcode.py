from datetime import datetime
from plyer import notification
import time
import speech_recognition as sr

# Function to listen to user voice input with adjusted timeout
def listen(recognizer, microphone):
    with microphone as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=7)  # Adjust the timeout as needed
    return audio

# Function to set reminder using voice input
def set_reminder():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("Please speak the reminder time in 24-hour format (HH:MM)")
    print("For example, say 'set reminder for 10:30'")
    audio = listen(recognizer, microphone)
    try:
        reminder_time = recognizer.recognize_google(audio)
        print("Reminder time:", reminder_time)
        
        # Replace 'or' with colon
        reminder_time = reminder_time.replace('or',':')
        print(reminder_time)
        
        print("Please speak the reminder title:")
        audio = listen(recognizer, microphone)
        reminder_title = recognizer.recognize_google(audio)
        print("Reminder title:", reminder_title)
        
        print("Please speak the reminder message:")
        audio = listen(recognizer, microphone)
        reminder_message = recognizer.recognize_google(audio)
        print("Reminder message:", reminder_message)
        
        return reminder_time, reminder_title, reminder_message
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
        return "", "", ""

# Main function to schedule reminders
def schedule_reminder(reminder_time, reminder_title, reminder_message):
    while True:
        current_time = datetime.now().strftime("%H : %M")
        if current_time == reminder_time:
            notification.notify(
                title=reminder_title,
                message=reminder_message,
                timeout=10
            )
            break
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    reminder_time, reminder_title, reminder_message = set_reminder()
    schedule_reminder(reminder_time, reminder_title, reminder_message)
