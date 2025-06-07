from utils.voice import UniversalVoiceAssistant

va = UniversalVoiceAssistant()
print("Voice system initialized successfully!")
print(f"Detected platform: {platform.system()}")
print(f"Active STT backend: {va.stt_backend}")

while True:
    print("\nSay something or type 'exit' to quit")
    text = va.listen()
    if text and "exit" in text.lower():
        break
    if text:
        print(f"You said: {text}")
        va.speak(f"I heard: {text}")
    else:
        print("No input detected")