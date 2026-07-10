#!/usr/bin/python3

from pymorsed import encode

def main():
    text = input("Enter text: ")
    morse = encode(text)
    print(morse)
    print("bye")
    return 0

if __name__ == "__main__":
    main()
