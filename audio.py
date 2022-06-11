from gtts import gTTS
from playsound import playsound
import os 
import pathlib
import pyttsx3

def play(txt):
	# tts = gTTS(text=str(txt), lang='vi', slow=False)
	# tts.save("sound.mp3")
	# playsound.playsound("sound.mp3", False)
	# os.remove("sound.mp3")
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    voices = engine.getProperty("voices")
    engine.setProperty('voice', voices[1].id)
    engine.say(txt)
    engine.runAndWait()



