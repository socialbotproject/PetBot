import os  # to remove created audio files
import random
import time
import webbrowser  # open browser

# PUSH TO ORG TEST
import playsound  # to play an audio file
import pyttsx3
import speech_recognition as sr  # recognize speech
from gtts import gTTS  # google text to speech

r = sr.Recognizer()  # initialise a recognizer
waitingforname = False

class person:
    name = ''

    def setName(self, name):
        self.name = name


class asis:
    name = ''

    def setName(self, name):
        self.name = name


def there_exists(terms, voice_data):
    for term in terms:
        if term in voice_data:
            return True


# listen for audio and convert it to text:
def record_audio(ask=""):
    print('recording')
    with sr.Microphone() as source:  # microphone as source
        print(source)
        if ask:
            speak(ask)
        audio = r.listen(source, 5, 5)  # listen for the audio via source
        print(audio)
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)  # convert audio to text

        except sr.UnknownValueError:  # error: recognizer does not understand
            speak('I did not get that')
        except sr.RequestError:
            speak('Sorry, the service is down')  # error: recognizer is not connected
        print(">>", voice_data.lower())  # print what user said
        # print("")
        return voice_data.lower()


def speak(audio_string):
    print('here even')
    audio_string = str(audio_string)
    tts = gTTS(text=audio_string, lang='en')  # text to speech(voice)
    r = random.randint(1, 20000000)
    audio_file = 'audio' + str(r) + '.mp3'
    tts.save(audio_file)  # save as mp3
    playsound.playsound(audio_file)  # play the audio file
    print(asis_obj.name + ":", audio_string)  # print what app said
    os.remove(audio_file)  # remove audio file


def respond(voice_data):
    # 1: greeting
    global waitingforname
    if there_exists(['hey', 'hi', 'hello'], voice_data):
        greetings = [f"hey, how can I help you {person_obj.name}", f"hey, what's up? {person_obj.name}",
                     f"I'm listening {person_obj.name}", f"how can I help you? {person_obj.name}",
                     f"hello {person_obj.name}"]
        greet = greetings[random.randint(0, len(greetings) - 1)]
        speak(greet)

    if there_exists(["what is your name", "what's your name", "tell me your name"], voice_data):

        if person_obj.name:
            speak(f"My name is {asis_obj.name}, {person_obj.name}")  # gets users name from voice input
        else:
            speak(f"My name is {asis_obj.name} . what's your name?")  # incase you haven't provided your name.
            waitingforname = True

    if there_exists(["my name is"], voice_data) or waitingforname:
        if there_exists(["my name is"], voice_data):
            person_name = voice_data.split("is")[-1].strip()
            speak("okay, i will remember that " + person_name)
            person_obj.setName(person_name)  # remember name in person object
        else:
            person_obj.setName(voice_data)
            waitingforname = False

    if there_exists(["what is my name"], voice_data):
        speak("Your name must be " + person_obj.name)

    if there_exists(["your name should be"], voice_data):
        asis_name = voice_data.split("be")[-1].strip()
        speak("okay, i will remember that my name is " + asis_name)
        asis_obj.setName(asis_name)  # remember name in asis object

    # 3: greeting
    if there_exists(["how are you", "how are you doing"], voice_data):
        speak("I'm very well, thanks for asking " + person_obj.name)

    # 4: time
    if there_exists(["what's the time", "tell me the time", "what time is it"], voice_data):
        t = time.localtime()
        current_time = time.strftime("%I:%M", t)
        speak("It's " + current_time)

    # 5: search google
    if there_exists(["search for"], voice_data) and 'youtube' not in voice_data:
        search_term = voice_data.split("for")[-1]
        url = f"https://google.com/search?q={search_term}"
        webbrowser.get().open(url)
        speak(f'Here is what I found for {search_term} on google')

    # 6: search youtube
    if there_exists(["youtube"], voice_data):
        search_term = voice_data.split("for")[-1]
        url = f"https://www.youtube.com/results?search_query={search_term}"
        webbrowser.get().open(url)
        speak(f'Here is what I found for {search_term} on youtube')

    if there_exists(["exit", "quit", "goodbye"], voice_data):
        speak(f'bye, {person_obj.name}')
        exit()


def greet():
    speak("Hello, I'm pet bot")


# time.sleep(1)
#
person_obj = person()
asis_obj = asis()


def init_audio(name):
    greet()
    person_obj.name = name
    asis_obj.name = 'pet bot'
    engine = pyttsx3.init()
    speak('How can I help you ?')
    while 1:
        voice_data = record_audio("")
        respond(voice_data)
