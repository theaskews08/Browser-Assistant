from get_instance import Browser
import commands
from time import sleep
import VINI_voice
from predict_intent import PredictIntent
from playsound import Playsound
from ui_box import ui_box
from wake_word_detector import WakeWordDetector
import threading

# Initialize browser
a = Browser('firefox')  # testing
with open("link.txt") as link:
    a.getPage(link.read())

# Initialize commands and intent prediction
commands.initialize_commands(a)
ip = PredictIntent()
prompt = ui_box()

# Wake word detection state
wake_word_enabled = True
waiting_for_wake_word = True
wake_word_detected_event = threading.Event()


def on_wake_word_detected():
    """Callback when wake word is detected."""
    global waiting_for_wake_word
    waiting_for_wake_word = False
    wake_word_detected_event.set()
    print("✓ Listening for command...")
    Playsound().start()  # Beep to indicate ready


def start_rolling():
    """Main voice command loop."""
    global waiting_for_wake_word

    # Start wake word detector if enabled
    wake_detector = None
    if wake_word_enabled:
        wake_detector = WakeWordDetector(callback=on_wake_word_detected)
        wake_detector.start()

    while prompt._running:
        try:
            if wake_word_enabled and waiting_for_wake_word:
                # Wait for wake word to be detected
                prompt.ready()
                wake_word_detected_event.wait(timeout=0.5)
                if not wake_word_detected_event.is_set():
                    continue
                wake_word_detected_event.clear()

            prompt.ready()

            # Listen for command
            if wake_word_enabled:
                # Shorter timeout when wake word mode is active
                b = VINI_voice.listen_for(5)
            else:
                # Original behavior without wake word
                b = VINI_voice.listen_for(3)

            if b:  # Only process if we got some input
                prompt.busy()
                intent = ip.predict_intent(b)
                print(f"Intent: {intent}")

                if intent[0] in commands.commands:
                    Playsound().start()  # Beep sound
                    commands.commands[intent[0]](b)

            # Reset wake word detection for next command
            if wake_word_enabled:
                waiting_for_wake_word = True

        except Exception as e:
            print(f"Error in voice command loop: {e}")
            # Reset state on error
            if wake_word_enabled:
                waiting_for_wake_word = True
            # Continue running unless explicitly stopped

    # Cleanup
    if wake_detector:
        wake_detector.stop()


threading.Thread(target=start_rolling, daemon=True).start()

try:
    prompt.root.mainloop()
except KeyboardInterrupt:
    print("\nShutting down...")
finally:
    prompt.stop()
