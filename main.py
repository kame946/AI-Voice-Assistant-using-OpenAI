import openai
import speech_recognition as sr
import pyttsx3

import time

openai.api_key = ""

engine = pyttsx3.init()

def audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)

        try:
            return recognizer.recognize_google(audio)
        except:
            print("Error occurred in conversion")

def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response["choices"][0]["text"]

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def main():
    while True:
        print("Say 'Albert' to began converstion")
        with sr.Microphone() as source:
            recogonizer = sr.Recognizer()
            audio = recogonizer.listen(source)

            try:
                transcription = recogonizer.recognize_google(audio)
                if transcription.lower() == "albert":
                    filename = "input.wav"
                    print("Albert Here, How may I help you!")
                    with sr.Microphone() as source:
                        recogonizer = sr.Recognizer()
                        source.pause_threshold = 1
                        audio = recogonizer.listen(source, timeout=None, phrase_time_limit=None)
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())

                    text = audio_to_text(filename)
                    if text:
                        print(f"You said {text}")
                        response = generate_response(text)
                        print(f"ChatGPT 3 response: {response}")
                        speak_text(response)

            except Exception as e:
                print("An error occured: {}".format(e))



if __name__ == "__main__":
    main()
