# Browser-Assistant
## Advanced Voice Controlled Browser & System Assistant

### 🎤 Talk to Your Computer!

A comprehensive voice-controlled assistant that goes beyond just browser control. Now includes:
- **🎙️ Advanced Speech Recognition** - Support for Google STT and OpenAI Whisper (offline)
- **🗣️ Realistic Text-to-Speech** - Natural-sounding voice feedback using Coqui TTS (no more robotic voices!)
- **🔊 System Volume Control** - Control your computer's volume with voice commands
- **⌨️ Keyboard Control** - Type and execute keyboard shortcuts hands-free
- **🖱️ Mouse Control** - Control your mouse cursor with voice
- **🎯 Wake Word Detection** - Say "Hey Computer" or "Hey PC" to activate
- **🌐 Full Browser Control** - Navigate, search, fill forms, and more

Built using cutting-edge AI models including Natural Language Processing, Speech Recognition (Whisper), and Neural TTS (Coqui) to provide a complete hands-free computing experience with human-like voice interactions. **Fast, real-time, and runs completely locally!**

Watch the demo: [https://youtu.be/En7TW8ckh-M](https://youtu.be/En7TW8ckh-M)

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

#### 🎯 Wake Word (Optional)
- **"Hey Computer"** or **"Hey PC"** - Activate the assistant (when wake word mode is enabled)

#### 🌐 Browser Navigation
- **Navigation**: "go back", "go forward", "reload", "quit"
- **Scrolling**: "scroll down", "scroll up", "stop scrolling"
- **Search**: "search for [query]", "google [query]"
- **Clicking**: "click [link text]", "open [URL]"
- **Forms**: "type", "next input", "previous input", "submit", "clear"
- **Tabs**: "open new tab", "close tab", "switch to next tab", "switch to previous tab"

#### 🔊 Volume Control
- **Set Volume**: "set volume to 50", "volume level 30"
- **Increase**: "volume up", "louder", "turn it up", "increase volume"
- **Decrease**: "volume down", "quieter", "turn it down", "decrease volume"
- **Mute/Unmute**: "mute", "silence", "unmute", "sound on"

#### ⌨️ Keyboard Control
- **Type Text**: "type on keyboard [text]", "keyboard type [text]"
- **Press Keys**: "press enter", "press tab", "press escape", "press space"
- **Arrow Keys**: "press up", "press down", "press left", "press right"
- **Clipboard**: "copy", "paste", "cut"

#### 🖱️ Mouse Control
- **Click**: "mouse click", "left click", "right click", "double click"
- **Move**: "move mouse up", "move mouse down", "mouse left", "mouse right"
- **Scroll**: "mouse scroll up", "mouse scroll down", "mouse wheel up"

### Configuration

#### Wake Word Detection
By default, wake word detection is **enabled**. The assistant will listen for "Hey Computer" or "Hey PC" before accepting commands.

To disable wake word detection and return to continuous listening mode:
1. Open `main.py`
2. Find the line: `wake_word_enabled = True`
3. Change it to: `wake_word_enabled = False`

#### Supported Wake Words
- "hey computer"
- "hey pc"
- "computer"
- "hey assistant"

You can customize these in `wake_word_detector.py`.

#### Speech Recognition (STT) Options

The system supports two speech recognition engines:

1. **Google Speech Recognition** (Default)
   - Fast and accurate
   - Requires internet connection
   - No additional setup needed

2. **OpenAI Whisper** (Optional - Best Quality)
   - Works completely offline
   - Higher accuracy for complex commands
   - Requires more processing power
   - To enable: Modify `enhanced_stt.py` to use `engine='whisper'`

#### Text-to-Speech (TTS) Options

The system uses **Coqui TTS** for realistic, human-like voice feedback:

- **Natural Voice**: Uses neural TTS models for realistic speech
- **Fast Performance**: Optimized for real-time responses
- **Runs Locally**: No internet required
- **No Robotic Voices**: Unlike gTTS or pyttsx3, Coqui TTS sounds natural

**First Run Note**: The first time you run the app, Coqui TTS will download its voice model (~100MB). This is a one-time download.

To disable voice feedback, comment out TTS calls in `system_commands.py`.

### Usage Tips

1. **Wake Word Mode (Default)**
   - Say "Hey Computer" or "Hey PC"
   - Wait for the beep sound
   - Give your command
   - The system will reset to listen for the wake word again

2. **Continuous Mode** (wake_word_enabled = False)
   - The assistant continuously listens for commands
   - No wake word needed
   - Great for rapid command execution

3. **System Control Tips**
   - Volume commands work system-wide, not just in the browser
   - Mouse and keyboard commands can control any application
   - Use these features responsibly and carefully

4. **Best Practices**
   - Speak clearly and at a moderate pace
   - Wait for the beep before speaking your command
   - Use the UI indicator to see when the system is ready/busy

### Platform Support

- **Windows**: Full support for all features including volume control
- **Linux**: Requires `amixer` for volume control (usually pre-installed)
- **macOS**: Volume control uses AppleScript (built-in)

### Troubleshooting

#### General Issues
- If microphone isn't detected, check Privacy Settings → Microphone permissions
- If GeckoDriver/ChromeDriver errors occur, ensure the driver version matches your browser version
- For "Permission denied" errors, run with administrator/sudo privileges
- If wake word detection is too sensitive, adjust `energy_threshold` in `wake_word_detector.py`
- For mouse/keyboard control issues, ensure PyAutoGUI is properly installed

#### TTS Issues
- **First run is slow**: Coqui TTS downloads models on first use (~100MB). Subsequent runs will be fast
- **No voice feedback**: Check that TTS is installed: `pip install TTS`
- **Voice sounds choppy**: Your system may be under load. Try closing other applications
- **Model download fails**: Check your internet connection and try again

#### STT Issues
- **Whisper is slow**: Use 'base' or 'tiny' model instead of 'large'
- **Recognition accuracy is low**: Ensure you're speaking clearly and microphone is close
- **Google STT not working**: Check internet connection
- **Whisper not available**: Install with `pip install openai-whisper`
