import sounddevice as sd
import soundfile as sf
from pynput.keyboard import Controller

keyboard = Controller()

AUDIO_FILE = './audio/yee-haw.mp3'


def play_audio():
    data, fs = sf.read(AUDIO_FILE)
    sd.play(data, fs)
    


def play_yehaw():
    
    play_audio()
    keyboard.press('p')   
    keyboard.release('p')
        
   