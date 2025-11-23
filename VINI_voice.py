import speech_recognition as sr

def listen_for(timeout=5):
    """
    Listen for voice input and return the recognized text.

    Args:
        timeout: Maximum time to listen in seconds

    Returns:
        String containing recognized speech or empty string on failure
    """
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=0.5)

            # Listen for audio input
            print(f"Listening for {timeout} seconds...")
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=timeout)

            # Recognize speech using Google Speech Recognition
            try:
                text = recognizer.recognize_google(audio)
                print(f"You said: {text}")
                return text.lower()
            except sr.UnknownValueError:
                print("Could not understand audio")
                return ""
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                return ""

    except Exception as e:
        print(f"Error with microphone: {e}")
        return ""
