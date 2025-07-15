import speech_recognition as sr
import pyttsx3
from googletrans import Translator
import keyboard
import requests
import os
import asyncio

# Setup TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Translator (sync version)
translator = Translator()

# Deepseek API Setup
DEEPSEEK_API_KEY = "ap2_f78ce239-f626-46f9-be10-9281ccb56236"

def speak(text):
    print("JARVIS:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        audio = recognizer.listen(source)
        try:
            query = recognizer.recognize_google(audio, language="auto")
            print("You said:", query)
            return query
        except:
            speak("Sorry, I didn't catch that.")
            return ""

def translate_to_english(text):
    try:
        translated = translator.translate(text, dest='en')
        return translated.text
    except Exception as e:
        speak("Translation error.")
        print("Translation error:", e)
        return text

def ask_deepseek(prompt):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        # Check if API returned 'choices'
        if 'choices' in result:
            return result['choices'][0]['message']['content']
        else:
            speak("DeepSeek response error.")
            print("DeepSeek Error Response:", result)
            return "Sorry, I couldn't get a response from DeepSeek."

    except Exception as e:
        print("API call failed:", e)
        return "Sorry, DeepSeek API request failed."

def control_pc(command):
    if "open notepad" in command:
        os.system("start notepad")
        speak("Opening Notepad")
    elif "open chrome" in command:
        os.system("start chrome")
        speak("Opening Chrome")
    else:
        speak("Sorry, I can't do that yet.")

async def main():
    speak("Jarvis Activated. Say something Prateek...")
    while True:
        user_input = listen()
        if user_input.lower() in ["exit", "quit", "bye"]:
            speak("Goodbye!")
            break
        if user_input.strip() == "":
            continue
        english_input = translate_to_english(user_input)
        control_pc(english_input.lower())
        answer = ask_deepseek(english_input)
        speak(answer)

if __name__ == "__main__":
    asyncio.run(main())
