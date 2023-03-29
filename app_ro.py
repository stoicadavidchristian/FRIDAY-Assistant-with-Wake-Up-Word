import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import os
import openai
import json

openai.api_key = "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"


# Initialize recognizer and microphone
r = sr.Recognizer()
mic = sr.Microphone()

# Set the wake-up word
WAKE_UP_WORD = "friday"

def speak(text):
    tts = gTTS(text=text, lang='ro')
    tts.save('output.mp3')
    playsound('output.mp3')
    os.remove('output.mp3')
# Define a function to listen for the wake-up word
def listen_for_wake_word():
    with mic as source:
        print("Aştept...")
        r.adjust_for_ambient_noise(source)  # calibrate the microphone
        audio = r.listen(source)  # listen for audio input

    try:
        text = r.recognize_google(audio, language="ro-RO")
        if text.lower() == WAKE_UP_WORD:
            print("Am detectat cuvântul cheie!")
            return True
    except:
        pass

    return False

r = sr.Recognizer()

def listen_for_audio():
    with sr.Microphone() as source:
        print("Vă ascult domnule")
        speak("Vă ascult domnule")
        r.adjust_for_ambient_noise(source)  # calibrate the microphone
        audio = r.listen(source)  # listen for audio input

    try:
        text = r.recognize_google(audio, language="ro-RO")
        print("Ai zis: " + text)
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"{text}",
            temperature=0.5,
            max_tokens=60,
            top_p=1.0,
            frequency_penalty=0.5,
            presence_penalty=0.0,
            stop=["Tu:"]
        )
        json_object = json.loads(str(response))
        print(json_object['choices'][0]['text'])
        speak(json_object['choices'][0]['text'])
    except sr.UnknownValueError:
        print("Îmi pare rău, nu am înţeles ce ai zis")
    except sr.RequestError:
        print("Eroare")

# Run the wake-up word listener in a loop
while True:
    while listen_for_wake_word():
        listen_for_audio()