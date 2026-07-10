#!/usr/bin/python3

from pymorsed import encode
from pymorsed.audio_decoder import decode_from_file
from pymorsed.audio_encoder import morse_to_audio, play_audio
from scipy.io.wavfile import write
import sounddevice as sd

import time

fs = 44100 # audio sample rate
rec_duration = 5 # audio recording duration in seconds
sd.default.samplerate = fs
sd.default.channels = 1

def print_options():
    print("""
    -------- SOUND CHAT MANUAL -------    

        h --- Host a new connection
        c --- Search for nearby connection
        o --- Display options
        q --- Quit app

    """)

def audio_to_text(recording):
    write('output.wav', fs, recording) # convert numpy array into wav

    try:
        return decode_from_file('output.wav')
    except Exception:
        return ''


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
    client_audio = morse_to_audio(encode("POLO"))

    # run a loop where client listens for MARCO for 10 seconds, and then plays POLO

    while True:
        rec = sd.rec(int(rec_duration * fs))
        sd.wait()

        host_res = audio_to_text(rec)

        print(f'Found text: {host_res}')

        if host_res == "MARCO":
            print("Host found! Responding...")

            while True:
                play_audio(client_audio)

                rec = sd.rec(int(rec_duration * fs))
                sd.wait()

                host_res = audio_to_text(rec)

        
    else:
        print("Device not found.")


def host_connection():
    host_audio = morse_to_audio(encode("MARCO"))
    
    # run a loop where MARCO is played, and then listen for POLO for 10 seconds
    while True:
        play_audio(host_audio)

        rec = sd.rec(int(rec_duration * fs))
        sd.wait()

        client_res = audio_to_text(rec)

        print(f'Found text: {client_res}')

        if client_res == "POLO":
            print("Device found!")


def test():
    while True:
        print("Recording in 3 seconds...")

        time.sleep(3)

        rec = sd.rec(int(rec_duration * fs))
        sd.wait()

        print("playing audio:")

        time.sleep(1)

        sd.play(rec)

        time.sleep(1)

def morse_test():
    while True:
        audio = morse_to_audio(encode("hey"))
        play_audio(audio)
        
        time.sleep(2)


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
            case 't':
                test()
            case 'm':
                morse_test()
            case _:
                print("Unknown command. Enter 'o' to display available commands.")
                continue

        
        
    return 0

if __name__ == "__main__":
    main()
