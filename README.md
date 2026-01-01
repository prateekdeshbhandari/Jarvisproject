# Jarvis Voice Assistant

A voice-controlled AI assistant that listens to commands in any language, translates them to English, and responds using the DeepSeek AI API with text-to-speech output.

## Features

- **Voice Recognition**: Listens to voice commands using speech recognition
- **Multi-language Support**: Automatically translates any language to English
- **AI Responses**: Uses DeepSeek API for intelligent responses
- **Text-to-Speech**: Speaks responses back to the user
- **PC Control**: Basic commands to open applications (Notepad, Chrome)

## Requirements

- Python 3.7 or higher
- Windows OS (optimized for Windows)
- Microphone (built-in or external)
- Active internet connection
- DeepSeek API key (free to obtain)

- 
**Expected output**: `Python 3.x.x`

**If Python is not installed**:
1. Download from [python.org](https://www.python.org/downloads/)
2. Run installer and **check "Add Python to PATH"**
3. Restart PowerShell and verify again

---

### Step 2: Navigate to Project Folder

```powershell
cd "C:\Users\Prateek DeshBhandari\OneDrive\Desktop\Jarvisproject"
```

---

### Step 3: Create Virtual Environment

Create an isolated environment for project dependencies:

```powershell
python -m venv jarvisenv
```

**What this does**: Creates a `jarvisenv` folder with Python packages isolated from your system

---

### Step 4: Activate Virtual Environment

```powershell
.\jarvisenv\Scripts\Activate.ps1
```

**Expected result**: Your prompt should now show `(jarvisenv)` at the beginning

**If you get an execution policy error**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Then try activating again.

---

### Step 5: Install Dependencies

Install all required Python packages:

```powershell
pip install SpeechRecognition pyttsx3 googletrans==4.0.0-rc1 keyboard requests
```

**Wait for installation to complete** (may take 1-2 minutes)

---

### Step 6: Install PyAudio (Audio Input)

PyAudio can be tricky on Windows. Try method A first:

**Method A - Direct Install:**
```powershell
pip install pyaudio
```

**If Method A fails, use Method B:**
```powershell
pip install pipwin
pipwin install pyaudio
```

**If both methods fail, use Method C:**
1. Visit: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
2. Download the `.whl` file matching your Python version and system (e.g., `PyAudio‑0.2.11‑cp310‑cp310‑win_amd64.whl` for Python 3.10, 64-bit)
3. Install it:
```powershell
pip install path\to\downloaded\file.whl
```

---

### Step 7: Get DeepSeek API Key

1. Go to: https://platform.deepseek.com/
2. Sign up for a free account
3. Navigate to **API Keys** section
4. Click **Create API Key**
5. Copy the key (starts with `sk-` or similar)

---

### Step 8: Configure API Key

Open `jarvis.py` in a text editor (Notepad, VS Code, etc.) and find line 17:

**Before:**
```python
DEEPSEEK_API_KEY = "ap2_f78ce239-f626-46f9-be10-9281ccb56236"
```

**After (replace with YOUR key):**
```python
DEEPSEEK_API_KEY = "your-actual-api-key-here"
```

Save the file.

---

### Step 9: Test Microphone Permissions

1. Go to **Windows Settings** → **Privacy** → **Microphone**
2. Ensure **"Allow apps to access your microphone"** is **ON**
3. Test your microphone (speak and check levels)

---

### Step 10: Run Jarvis

```powershell
python jarvis.py
```

**Expected output:**
```
JARVIS: Jarvis Activated. Say something Prateek...
JARVIS: Listening...
```

**Now speak into your microphone!**
### Using Voice Commands

**General Conversation:**
- "What is the weather today?"
- "Tell me a joke"
- "Explain quantum physics"
- "Write a poem about nature"

**Multi-language Support:**
- Speak in any language (Hindi, Spanish, French, etc.)
- Jarvis will automatically translate to English and respond

**PC Control Commands:**
- "Open notepad" → Opens Notepad
- "Open chrome" → Opens Chrome browser

**Exit Commands:**
- Say **"exit"**, **"quit"**, or **"bye"** to stop Jarvis

---

### Example Usage Session

```
JARVIS: Jarvis Activated. Say something Prateek...
JARVIS: Listening...
You said: What is Python?
JARVIS: Python is a high-level, interpreted programming language...

JARVIS: Listening...
You said: open notepad
JARVIS: Opening Notepad
[Notepad opens]

JARVIS: Listening...    
You said: bye
JARVIS: Goodbye!
```
<img width="1919" height="943" alt="image" src="https://github.com/user-attachments/assets/6cddead3-5ddd-4dc2-a633-532ccc208ded" />


## Project Structure

- `jarvis.py` - Main application file
- `jarvisenv/` - Virtual environment directory
