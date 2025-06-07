import pyttsx3
import speech_recognition as sr

class FreeVoiceAssistant:
    def __init__(self):
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # Slower speech rate
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = 1.5  # Longer pause before ending
        
    def speak(self, text):
        """Convert text to speech"""
        self.engine.say(text)
        self.engine.runAndWait()
        
    def listen(self):
        """Listen to microphone input and convert to text"""
        with sr.Microphone() as source:
            print("\n🎤 Listening... (speak now)")
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.recognizer.listen(source, timeout=5)
                text = self.recognizer.recognize_google(audio)
                return text.lower()
            except sr.WaitTimeoutError:
                return ""
            except sr.UnknownValueError:
                return ""
            except Exception as e:
                print(f"Voice recognition error: {e}")
                return ""