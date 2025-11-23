"""
Advanced Text-to-Speech Engine using Coqui TTS
Provides realistic, natural-sounding voice synthesis that runs locally.
"""

import threading
import os
import tempfile
import platform

class TTSEngine:
    """High-quality text-to-speech engine using Coqui TTS."""

    def __init__(self, use_gpu=False):
        """
        Initialize the TTS engine.

        Args:
            use_gpu: Use GPU acceleration if available (default: False for faster loading)
        """
        self.engine = None
        self.use_gpu = use_gpu
        self.initialized = False
        self.temp_dir = tempfile.gettempdir()
        self.engine_type = 'coqui'  # Default to Coqui TTS

        # Try to initialize TTS engine
        self._initialize_engine()

    def _initialize_engine(self):
        """Initialize the TTS engine with fallback options."""
        try:
            # Try Coqui TTS first (best quality)
            from TTS.api import TTS
            print("Initializing Coqui TTS (high quality)...")

            # Use a fast, high-quality model
            # tts_models/en/ljspeech/tacotron2-DDC is fast and good quality
            # tts_models/en/vctk/vits is even better quality with multiple voices
            model_name = "tts_models/en/ljspeech/fast_pitch"

            self.engine = TTS(model_name=model_name, progress_bar=False, gpu=self.use_gpu)
            self.engine_type = 'coqui'
            self.initialized = True
            print("✓ Coqui TTS initialized successfully")

        except ImportError:
            print("Coqui TTS not available. Install with: pip install TTS")
            self._try_espeak_fallback()
        except Exception as e:
            print(f"Error initializing Coqui TTS: {e}")
            self._try_espeak_fallback()

    def _try_espeak_fallback(self):
        """Try eSpeak-ng as fallback (better quality than pyttsx3)."""
        try:
            import espeakng
            self.engine = espeakng.ESpeakNG()
            self.engine.voice = 'en-us'
            self.engine.pitch = 50
            self.engine.speed = 175
            self.engine_type = 'espeak'
            self.initialized = True
            print("✓ Using eSpeak-ng TTS (fallback)")
        except:
            print("⚠ No TTS engine available. Install Coqui TTS: pip install TTS")
            self.initialized = False

    def speak(self, text, blocking=False):
        """
        Speak the given text.

        Args:
            text: Text to speak
            blocking: If True, wait for speech to complete before returning
        """
        if not self.initialized or not text:
            return

        if blocking:
            self._speak_internal(text)
        else:
            # Speak in background thread
            thread = threading.Thread(target=self._speak_internal, args=(text,), daemon=True)
            thread.start()

    def _speak_internal(self, text):
        """Internal method to perform speech synthesis."""
        try:
            if self.engine_type == 'coqui':
                # Generate audio file
                output_path = os.path.join(self.temp_dir, 'tts_output.wav')
                self.engine.tts_to_file(text=text, file_path=output_path)

                # Play the audio
                self._play_audio(output_path)

                # Clean up
                try:
                    os.remove(output_path)
                except:
                    pass

            elif self.engine_type == 'espeak':
                # eSpeak-ng can speak directly
                self.engine.say(text, sync=True)

        except Exception as e:
            print(f"Error during speech synthesis: {e}")

    def _play_audio(self, file_path):
        """Play audio file using platform-specific methods."""
        system = platform.system()

        try:
            if system == "Windows":
                import winsound
                winsound.PlaySound(file_path, winsound.SND_FILENAME)
            elif system == "Darwin":  # macOS
                os.system(f'afplay "{file_path}"')
            else:  # Linux
                # Try multiple players
                players = ['aplay', 'paplay', 'ffplay -nodisp -autoexit']
                for player in players:
                    try:
                        os.system(f'{player} "{file_path}" 2>/dev/null')
                        break
                    except:
                        continue
        except Exception as e:
            print(f"Error playing audio: {e}")

    def speak_async(self, text):
        """Speak text asynchronously (non-blocking)."""
        self.speak(text, blocking=False)

    def speak_sync(self, text):
        """Speak text synchronously (blocking)."""
        self.speak(text, blocking=True)


class QuickResponses:
    """Pre-defined quick responses for common actions."""

    def __init__(self, tts_engine):
        self.tts = tts_engine

    def ready(self):
        """Indicate ready state."""
        self.tts.speak_async("Ready")

    def listening(self):
        """Indicate listening state."""
        self.tts.speak_async("Listening")

    def done(self):
        """Indicate task completion."""
        self.tts.speak_async("Done")

    def error(self):
        """Indicate error."""
        self.tts.speak_async("Sorry, I couldn't do that")

    def confirm(self):
        """Confirm action."""
        self.tts.speak_async("Okay")

    def volume_changed(self, level=None):
        """Confirm volume change."""
        if level:
            self.tts.speak_async(f"Volume set to {level} percent")
        else:
            self.tts.speak_async("Volume adjusted")

    def navigating(self, destination):
        """Announce navigation."""
        self.tts.speak_async(f"Navigating to {destination}")

    def searching(self, query):
        """Announce search."""
        self.tts.speak_async(f"Searching for {query}")


# Global TTS instance (lazy initialization)
_tts_instance = None

def get_tts_engine():
    """Get or create the global TTS engine instance."""
    global _tts_instance
    if _tts_instance is None:
        _tts_instance = TTSEngine()
    return _tts_instance


def speak(text, blocking=False):
    """Quick function to speak text using the global TTS engine."""
    engine = get_tts_engine()
    engine.speak(text, blocking=blocking)


# Test function
if __name__ == "__main__":
    print("Testing TTS Engine...")
    tts = TTSEngine()

    test_phrases = [
        "Hello, I am your voice assistant.",
        "Volume set to fifty percent.",
        "Searching for artificial intelligence.",
        "Command executed successfully."
    ]

    for phrase in test_phrases:
        print(f"Speaking: {phrase}")
        tts.speak_sync(phrase)
        print("Done")

    print("TTS test complete!")
