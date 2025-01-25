# Importing necessary libraries
import wave
import os
import tkinter as tk
from tkinter import filedialog

import termcolor
from termcolor import colored
from pyfiglet import figlet_format  # For fancy text formatting in console

# Function to encode a message into an audio file
def encode_aud_data():
    # Create a Tkinter root window and hide it
    root=tk.Tk()
    root.withdraw()

    print("\tSelect the file")
    root.attributes('-alpha',0.0)  # Hide the window
    root.attributes('-topmost',True)  # Always have it on top
    nameoffile=filedialog.askopenfilename(title="Select Audio File to Encode")

    # Open the selected audio file
    song=wave.open(nameoffile,mode='rb')

    # Read the frames from the audio file
    nframes=song.getnframes()
    frames=song.readframes(nframes)
    frame_list=list(frames)
    frame_bytes=bytearray(frame_list)

    # Get the secret message from the user
    data=input("\nEnter the secret message :- ")

    # Convert the secret message to binary
    res=''.join(format(i,'08b') for i in bytearray(data,encoding ='utf-8'))     
    print("\nThe string after binary conversion :- "+(res))   
    length=len(res)
    print("\nLength of binary after conversion :- ",length)

    # Append a special string to the end of the secret message as a delimiter
    data=data+'*^*^*'

    # Convert the secret message to a list of bits
    result=[]
    for c in data:
        bits=bin(ord(c))[2:].zfill(8)
        result.extend([int(b) for b in bits])

    # Embed the secret message into the audio file
    j=0
    for i in range(0,len(result),1): 
        res=bin(frame_bytes[j])[2:].zfill(8)
        if res[len(res)-4]== result[i]:
            frame_bytes[j]=(frame_bytes[j] & 253)      #253: 11111101 {maxm pixel value : 253}
        else:
            frame_bytes[j]=(frame_bytes[j] & 253) | 2
            frame_bytes[j]=(frame_bytes[j] & 254) | result[i]
        j=j+1
    
    # Convert the modified frames back to bytes
    frame_modified=bytes(frame_bytes)

    # Save the modified audio file
    filename=os.path.splitext(os.path.basename(nameoffile))[0]
    stegofile=os.path.join("Result_files",filename+"_embeded.wav")

    with wave.open(stegofile,'wb') as fd:
        fd.setparams(song.getparams())
        fd.writeframes(frame_modified)
    
    print("\nEncoded the data successfully in the audio file.")    
    song.close()

# Function to decode a message from an audio file
def decode_aud_data():
    # Create a Tkinter root window and hide it
    root=tk.Tk()
    root.withdraw()

    print("\tSelect the file")
    root.attributes('-alpha',0.0)  # Hide the window
    root.attributes('-topmost',True)  # Always have it on top
    nameoffile=filedialog.askopenfilename(title="Select Audio File to Decode")

    # Open the selected audio file
    song=wave.open(nameoffile,mode='rb')

    # Read the frames from the audio file
    nframes=song.getnframes()
    frames=song.readframes(nframes)
    frame_list=list(frames)
    frame_bytes=bytearray(frame_list)

    # Extract the secret message from the audio file
    extracted=""
    p=0
    for i in range(len(frame_bytes)):
        if p == 1:
            break
        res=bin(frame_bytes[i])[2:].zfill(8)
        if res[len(res)-2] == '0':
            extracted += res[len(res)-4]
        else:
            extracted += res[len(res)-1]
    
        all_bytes=[ extracted[i: i+8] for i in range(0,len(extracted),8) ]
        decoded_data=""
        for byte in all_bytes:
            decoded_data += chr(int(byte,2))
            if decoded_data[-5:] == "*^*^*":
                print("The Encoded data was :--",decoded_data[:-5])
                p=1
                break  

# Main function to handle user interaction
def aud_Steg():
    print(colored(figlet_format("Hidden Layers"),color='red'))
    while True:
        print("\nSELECT AUDIO STEGANOGRAPHY OPERATION\n") 
        print("1. Embed the message")  
        print("2. Decode the message")  
        print("3. Exit")  
        choice1=int(input("Enter the Choice: "))   
        if choice1 == 1:
            encode_aud_data()
        elif choice1 == 2:
            decode_aud_data()
        elif choice1 == 3:
            break
        else:
            print("Incorrect Choice")
        print("\n")

# Run the main function if this script is run as the main program
if __name__ == "__main__":
    aud_Steg()