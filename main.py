#!/usr/bin/python3

from pymorsed import encode
from pymorsed.audio_decoder import decode_from_file
from pymorsed.audio_encoder import morse_to_audio, play_audio
from scipy.io.wavfile import write
import sounddevice as sd

import time

fs = 44100 # audio sample rate
rec_duration = 10 # audio recording duration in seconds
sd.default.samplerate = fs
sd.default.channels = 2

def print_options():
    print("""
    -------- SOUND CHAT MANUAL -------    

        h --- Host a new connection
        c --- Search for nearby connection
        o --- Display options
        q --- Quit app

    """)

def chat():
    while True:
        try:
            text = input("Enter text (or CTRL+D to exit): ")
            morse = encode(text)
            audio = morse_to_audio(morse)
            play_audio(audio)

        except EOFError:
            print("\n\n\nExiting chat...\n\n")
            return 0
        
def search_nearby():

    # for testing purposes, a device has been found
    device_found = True

    if (device_found):
        print("Device found. Starting chat...")
        chat()
    else:
        print("Device not found.")


def host_connection():
    host_morse = encode("MARCO")
    host_audio = morse_to_audio(host_morse)
    
    # run a loop where MARCO is played, and then listen for POLO for 10 seconds
    while (True):
        play_audio(host_audio)

        rec = sd.rec(int(rec_duration * fs))
        sd.wait()

        write('output.wav', fs, rec) # convert numpy array into wav

        text = decode_from_file('output.wav')

        if text == "POLO":
            print("Device found!")

def main():

    while True:
        command = input("Enter command ('o' to display options): ")

        # available commands    
        match command:
            case 'h':
                "Starting new connection..."
                host_connection()
            case 'c':
                "Searching for nearby devices..."
                search_nearby()
            case 'o':
                print_options()
                continue
            case 'q':
                print("\nTurning off...")
                return 0
            case _:
                print("Unknown command. Enter 'o' to display available commands.")
                continue

        
        
    return 0

if __name__ == "__main__":
    main()
