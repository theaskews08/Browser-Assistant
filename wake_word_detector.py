import speech_recognition as sr
import threading
import time

class WakeWordDetector:
    """
    Detects wake words like 'hey computer' or 'hey pc' to activate the assistant.
    Uses continuous listening with speech recognition.
    """

    def __init__(self, wake_words=None, callback=None):
        """
        Initialize the wake word detector.

        Args:
            wake_words: List of wake word phrases (default: ['hey computer', 'hey pc'])
            callback: Function to call when wake word is detected
        """
        if wake_words is None:
            self.wake_words = ['hey computer', 'hey pc', 'computer', 'hey assistant']
        else:
            self.wake_words = [w.lower() for w in wake_words]

        self.callback = callback
        self.is_listening = False
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        self.listen_thread = None

    def start(self):
        """Start listening for wake words in background thread."""
        if not self.is_listening:
            self.is_listening = True
            self.listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
            self.listen_thread.start()
            print("Wake word detection started. Say 'hey computer' or 'hey pc' to activate.")

    def stop(self):
        """Stop listening for wake words."""
        self.is_listening = False
        if self.listen_thread:
            self.listen_thread.join(timeout=2)
        print("Wake word detection stopped.")

    def _listen_loop(self):
        """Continuous listening loop for wake word detection."""
        with sr.Microphone() as source:
            # Adjust for ambient noise once at the start
            print("Adjusting for ambient noise... Please wait.")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Ready! Listening for wake words...")

            while self.is_listening:
                try:
                    # Listen for audio
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)

                    # Try to recognize speech
                    try:
                        text = self.recognizer.recognize_google(audio).lower()
                        print(f"[Wake word detector]: {text}")

                        # Check if any wake word is in the recognized text
                        if any(wake_word in text for wake_word in self.wake_words):
                            print(f"✓ Wake word detected!")
                            if self.callback:
                                self.callback()

                    except sr.UnknownValueError:
                        # Speech was not understood
                        pass
                    except sr.RequestError as e:
                        print(f"Could not request results; {e}")
                        time.sleep(1)

                except sr.WaitTimeoutError:
                    # No speech detected within timeout, continue listening
                    continue
                except Exception as e:
                    print(f"Error in wake word detection: {e}")
                    time.sleep(1)

def test_wake_word():
    """Test function for wake word detection."""
    def on_wake_word():
        print("Wake word triggered! System is now listening...")

    detector = WakeWordDetector(callback=on_wake_word)
    detector.start()

    try:
        # Keep running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        detector.stop()
        print("\nTest stopped.")

if __name__ == "__main__":
    test_wake_word()
