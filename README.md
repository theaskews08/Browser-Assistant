# Browser-Assistant
## Voice controlled browser assistant.
### Now you can talk to your browser.<br>
Those who would like to have a hands free browsing experience, can use this to control their browser with their voice(by talking to it actually).
It is able to do almost everything from filling forms to opening new tabs etc.
It's going to be a complete natural language UI. Made by using different concepts of Natural Language Processing.
Watch the demo <a href = "#">https://youtu.be/En7TW8ckh-M</a>

## Installation

### Prerequisites
- Python 3.7 or higher
- Firefox or Chrome browser
- Microphone for voice commands

### Windows 11 Installation

1. **Install Python**
   - Download Python from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"

2. **Install Firefox or Chrome**
   - Download [Firefox](https://www.mozilla.org/firefox/) or [Chrome](https://www.google.com/chrome/)

3. **Download GeckoDriver (for Firefox) or ChromeDriver (for Chrome)**

   For Firefox:
   - Download [GeckoDriver](https://github.com/mozilla/geckodriver/releases)
   - Extract `geckodriver.exe` to the Browser-Assistant folder
   - Or add it to your system PATH

   For Chrome:
   - Download [ChromeDriver](https://chromedriver.chromium.org/)
   - Extract `chromedriver.exe` to the Browser-Assistant folder
   - Or add it to your system PATH

4. **Clone or Download this Repository**
   ```bash
   git clone https://github.com/theaskews08/Browser-Assistant.git
   cd Browser-Assistant
   ```

5. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   If you encounter issues with PyAudio on Windows, install it separately:
   ```bash
   pip install pipwin
   pipwin install pyaudio
   ```

6. **Configure the Starting URL**
   - Create or edit `link.txt` in the Browser-Assistant folder
   - Add your preferred starting URL (e.g., `https://www.google.com`)

7. **Run the Application**
   ```bash
   python main.py
   ```

### Voice Commands
Once running, you can use these voice commands:
- **Navigation**: "go back", "go forward", "reload", "quit"
- **Scrolling**: "scroll down", "scroll up", "stop scrolling"
- **Search**: "search for [query]"
- **Clicking**: "click [link text]"
- **Forms**: "type", "next input", "previous input", "submit", "clear"
- **Tabs**: "open new tab", "close tab", "switch to next tab", "switch to previous tab"

### Troubleshooting
- If microphone isn't detected, check Windows Privacy Settings → Microphone
- If GeckoDriver/ChromeDriver errors occur, ensure the driver version matches your browser version
- For "Permission denied" errors, run Command Prompt as Administrator
