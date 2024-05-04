# Importing necessary libraries
import os
import numpy as np
import tkinter as tk
from tkinter import filedialog

import termcolor
from termcolor import colored
from pyfiglet import figlet_format

# Function to encode text into a cover file
def txt_encode(text,cover_file_path):
    # Initialize variables
    l=len(text)
    i=0
    add=''
    # Loop through each character in the text
    while i < l:
        t=ord(text[i])  # Get the ASCII value of the character
        # Apply transformations based on the ASCII value
        if t >= 32 and t <= 64:
            t1=t+48
            t2=t1 ^ 170  # 170: 10101010
            res=bin(t2)[2:].zfill(8)  # Convert to binary and pad with zeros
            add += "0011"+res
        else:
            t1=t - 48
            t2=t1 ^ 170
            res=bin(t2)[2:].zfill(8)
            add += "0110"+res
        i += 1
    # Add end marker
    res1=add+"111111111111"
    print("The string after binary conversion applying all the transformation :- "+(res1))
    length=len(res1)
    print("Length of binary after conversion:- ",length)
    # Initialize variables for Zero Width Characters (ZWC)
    HM_SK=""
    ZWC={"00": u'\u200C',"01": u'\u202C',"11": u'\u202D',"10": u'\u200E'}
    filename=os.path.splitext(os.path.basename(cover_file_path))[0]
    
    result_folder="Result_files"
    # Construct the stego file path
    stego_file_path=os.path.join(result_folder,filename+"_stegano.txt")
    
    # Open the cover file and the stego file
    with open(cover_file_path,"r+") as file1,open(stego_file_path,"w+",encoding="utf-8") as file3:
        word=[]
        # Read the cover file line by line
        for line in file1:
            word += line.split()
        i=0
        # Loop through each bit in the encoded text
        while i < len(res1):
            s=word[int(i/12)]
            j=0
            x=""
            HM_SK=""
            # Loop through each character in the word
            while j < 12:
                x=res1[j+i]+res1[i+j+1]
                HM_SK += ZWC[x]
                j += 2
            # Add the ZWC to the word
            s1=s+HM_SK
            # Write the word to the stego file
            file3.write(s1)
            file3.write(" ")
            i += 12
        t=int(len(res1)/12)
        # Write the remaining words to the stego file
        while t < len(word):
            file3.write(word[t])
            file3.write(" ")
            t += 1
    
    print("\nStego file has been successfully generated at:",stego_file_path)

# Function to get the cover file and the text to be encoded from the user
def encode_txt_data():
    root=tk.Tk()
    root.withdraw()  # Hide the main window
    print("\tSelect the file")
    root.attributes('-alpha',0.0)  # Hide the window
    root.attributes('-topmost',True)  # Always have it on top
    cover_file_path=filedialog.askopenfilename(title="Select Cover Text File")
    count2=0
    # Count the number of words in the cover file
    with open(cover_file_path,"r") as file1:
        for line in file1:
            for word in line.split():
                count2=count2+1
    bt=int(count2)
    print("Maximum number of words that can be inserted :- ",int(bt/6))
    text1=input("\nEnter data to be encoded:- ")
    l=len(text1)
    # Check if the text can be hidden in the cover file
    if l <= bt:
        print("\nInputed message can be hidden in the cover file\n")
        txt_encode(text1,cover_file_path)
    else:
        print("\nString is too big please reduce string size")
        encode_txt_data()

# Function to decode text from a stego file
def txt_decode(stego_file_path):
    ZWC_reverse={u'\u200C': "00",u'\u202C': "01",u'\u202D': "11",u'\u200E': "10"}
    temp=''
    # Open the stego file
    with open(stego_file_path,"r",encoding="utf-8") as file4:
        # Read the stego file line by line
        for line in file4:
            for words in line.split():
                T1=words
                binary_extract=""
                # Loop through each character in the word
                for letter in T1:
                    # Check if the character is a ZWC
                    if letter in ZWC_reverse:
                        binary_extract += ZWC_reverse[letter]
                # Check for the end marker
                if binary_extract == "111111111111":
                    break
                else:
                    temp += binary_extract
    print("\nEncrypted message presented in code bits:",temp)
    lengthd=len(temp)
    print("\nLength of encoded bits:- ",lengthd)
    i=0
    a=0
    b=4
    c=4
    d=12
    final=''
    # Loop through each bit in the encoded text
    while i < len(temp):
        t3=temp[a:b]
        a += 12
        b += 12
        i += 12
        t4=temp[c:d]
        c += 12
        d += 12
        # Apply transformations based on the first 4 bits
        if t3 == '0110':
            decimal_data=BinaryToDecimal(t4)
            final += chr((decimal_data ^ 170)+48)
        elif t3 == '0011':
            decimal_data=BinaryToDecimal(t4)
            final += chr((decimal_data ^ 170) - 48)
    print("\nMessage after decoding from the stego file:- ",final)

# Function to get the stego file from the user
def decode_txt_data():
    root=tk.Tk()
    print("\tSelect the file")
    root.withdraw()  
    # Hide the window
    root.attributes('-alpha',0.0)
    # Always have it on top
    root.attributes('-topmost',True)
    stego_file_path=filedialog.askopenfilename(title="Select Stego Text File")
    txt_decode(stego_file_path)

# Main function
def txt_steg():

    # Use one of the recognized color names
    print(colored(figlet_format("Hidden Layers"),color='red'))

    while True:
        print("\nSELECT THE TEXT STEGANOGRAPHY OPERATION\n")
        print("1. Encode the Text message")
        print("2. Decode the Text message")
        print("3. Exit")
        choice1=int(input("Enter the Choice: "))
        if choice1 == 1:
            encode_txt_data()
        elif choice1 == 2:
            decode_txt_data()
        elif choice1 == 3:
            break
        else:
            print("Incorrect Choice")
        print("\n")

# Function to convert binary to decimal
def BinaryToDecimal(binary):
    string=int(binary,2)
    return string

# Run the main function
if __name__ == "__main__":
    txt_steg()
