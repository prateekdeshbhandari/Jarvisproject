import speech_recognition as sr
import pyttsx3
import keyboard
import requests
import os
import asyncio
from dotenv import load_dotenv
import json
import re

# Load environment variables
load_dotenv()

# Setup TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# API Setup - Use environment variable for security
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY','sk-ab555b8e4ed54220ae2d78836c24fe01')

def speak(text):
    print("JARVIS:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        try:
            query = recognizer.recognize_google(audio, language="auto")
            print("You said:", query)
            return query
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
            return ""
        except sr.RequestError as e:
            speak("Speech recognition service error.")
            print(f"Speech recognition error: {e}")
            return ""
        except Exception as e:
            speak("An error occurred while listening.")
            print(f"Listening error: {e}")
            return ""

def is_likely_english(text):
    """Simple English detection - just return the text as-is"""
    # For now, assume all input is in English or can be processed as-is
    # This removes the translation dependency completely
    return text

def ask_ai_free(prompt):
    """Free AI API using Hugging Face Inference API"""
    try:
        # Using a free public API endpoint
        url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
        headers = {"Content-Type": "application/json"}
        data = {"inputs": prompt}
        
        response = requests.post(url, headers=headers, json=data, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get('generated_text', prompt)
        
        # Fallback to simple responses for common questions
        return get_simple_response(prompt)
        
    except Exception as e:
        print(f"Free AI API error: {e}")
        return get_simple_response(prompt)

def get_simple_response(prompt):
    """Simple rule-based responses for common questions"""
    prompt_lower = prompt.lower()
    
    if "cricket" in prompt_lower and "india" in prompt_lower:
        if "biggest" in prompt_lower or "famous" in prompt_lower or "best" in prompt_lower:
            return "Some of the biggest cricketers in India include Virat Kohli, MS Dhoni, Sachin Tendulkar, and Rohit Sharma."
    
    if "hello" in prompt_lower or "hi" in prompt_lower:
        return "Hello! I'm JARVIS, your voice assistant. How can I help you today?"
    
    if "time" in prompt_lower:
        from datetime import datetime
        return f"The current time is {datetime.now().strftime('%I:%M %p')}"
    
    if "date" in prompt_lower:
        from datetime import datetime
        return f"Today is {datetime.now().strftime('%B %d, %Y')}"
    
    if "weather" in prompt_lower:
        return "I don't have access to weather data, but you can check weather apps or websites for current conditions."
    
    # Default response
    return "I understand your question. While my AI service is limited, I can help with PC commands like opening apps."

def ask_deepseek(prompt):
    """Try DeepSeek API first, fallback to free alternatives"""
    if not DEEPSEEK_API_KEY or DEEPSEEK_API_KEY == 'your_api_key_here':
        return ask_ai_free(prompt)
    
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are JARVIS, a helpful AI assistant. Give concise, helpful responses."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 150,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=15)
        
        # Check HTTP status
        if response.status_code == 401:
            return ask_ai_free(prompt)  # Fallback to free API
        elif response.status_code == 402:
            return ask_ai_free(prompt)  # Payment required - use free alternative
        elif response.status_code == 429:
            return ask_ai_free(prompt)  # Rate limit - use free alternative
        elif response.status_code != 200:
            return ask_ai_free(prompt)  # Any other error - use free alternative
        
        result = response.json()
        
        # Check if API returned 'choices'
        if 'choices' in result and len(result['choices']) > 0:
            return result['choices'][0]['message']['content']
        else:
            return ask_ai_free(prompt)  # Fallback
            
    except Exception as e:
        print("DeepSeek API failed, using fallback:", e)
        return ask_ai_free(prompt)

def control_pc(command):
    command = command.lower()
    if "open notepad" in command:
        os.system("start notepad")
        speak("Opening Notepad")
        return True
    elif "open chrome" in command or "open browser" in command:
        os.system("start chrome")
        speak("Opening Chrome")
        return True
    elif "open calculator" in command:
        os.system("start calc")
        speak("Opening Calculator")
        return True
    elif "open file explorer" in command or "open files" in command:
        os.system("start explorer")
        speak("Opening File Explorer")
        return True
    return False

async def main():
    speak("Jarvis Activated. Say something Prateek...")
    
    while True:
        try:
            user_input = listen()
            
            if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
                speak("Goodbye Prateek!")
                break
                
            if user_input.strip() == "":
                continue
            
            # Process input (no translation needed)
            english_input = is_likely_english(user_input)
            
            # Try PC control first
            if not control_pc(english_input):
                # If not a PC command, ask AI
                answer = ask_deepseek(english_input)
                speak(answer)
                
        except KeyboardInterrupt:
            speak("Goodbye!")
            break
        except Exception as e:
            print(f"Main loop error: {e}")
            speak("An error occurred. Continuing...")

if __name__ == "__main__":
    # Check if required packages are available
    try:
        import speech_recognition
        import pyttsx3
        import googletrans
        import requests
    except ImportError as e:
        print(f"Missing required package: {e}")
        print("Please install required packages with: pip install -r requirements.txt")
        exit(1)
    asyncio.run(main())
