# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
from typing import List, Set, Dict, Tuple, Optional
from enum import Enum
from inspect import getsourcefile
from os.path import abspath
from google.cloud import texttospeech
import PySimpleGUI as sg
from google.cloud.texttospeech_v1 import Voice
from pydub import AudioSegment
from pydub.playback import play
import io

cwd = os.path.dirname(abspath(getsourcefile(lambda:0)))

#set the google credential env variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cwd +"/google_credentials/google_speech_credentials.json"
client = texttospeech.TextToSpeechClient()

def sayit(text: str,voiceName:str) -> bytearray:
    # Instantiates a client


    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
        name=voiceName
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content

    # The response's audio_content is binary.

def listGoogleVoices()->List[Voice]:
    return client.list_voices().voices


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    googleVoices:List[Voice] = listGoogleVoices()
    voiceNames: List[str] = []
    for voice in googleVoices:
        voiceNames.append(voice.name)
    sg.theme('DarkAmber')  # Add a touch of color
    # All the stuff inside your window.
    layout = [
              [sg.Text('What to say'), sg.Multiline(size = [80,10])],
              [sg.Combo(values=voiceNames)],
              [sg.Button('Ok'), sg.Button('Cancel')]]

    # Create the Window
    window = sg.Window('Window Title', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
            break
        audio: bytearray = sayit(values[0],values[1])
        audioSegment = AudioSegment.from_file(io.BytesIO(audio), format="mp3")
        play(audioSegment)

    window.close()


    #audio:bytearray = sayit("Hello World")
    #with open("output.mp3", "wb") as out:
        # Write the response to the output file.
    #    out.write(audio)
    #    print('Audio content written to file "output.mp3"')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
