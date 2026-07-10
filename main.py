#!/usr/bin/python3

from pymorsed import encode
from pymorsed.audio_decoder import decode_from_file
from pymorsed.audio_encoder import morse_to_audio, play_audio

import time

def print_options():
    print("""
    -------- SOUND CHAT MANUAL -------    

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


def main():

    while True:
        command = input("Enter command ('o' to display options): ")

        # available commands    
        match command:
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
