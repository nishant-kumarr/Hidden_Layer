# Importing necessary libraries
from PIL import Image
import numpy as np
import tkinter as tk
from tkinter import filedialog
from imageStegHelper import ImageSteg  # Custom module for image steganography

from termcolor import colored
from pyfiglet import figlet_format  # For fancy text formatting in console

# Function to encode a message into an image
def encode_message():
    # Create an ImageSteg object
    img=ImageSteg()

    # Create a Tkinter root window and hide it
    root=tk.Tk()
    root.withdraw()

    # Ask user to select an image file
    print("\tSelect the file")
    root.attributes('-alpha',0.0)  # Hide the window
    root.attributes('-topmost',True)  # Always have it on top
    image_path=filedialog.askopenfilename(title="Select an image to hide the message")

    # If a valid image path is selected
    if image_path:
        # Get the message to be encoded from the user
        msg=input("Enter the message to hide in the image: ")
        print("\n\tEncoding underway ! Please wait ... \n\n")

        # Define the target path where the encoded image will be saved
        target_path="C:\\Users\\nisha\\OneDrive\\Desktop\\Steno_Final\\Result_files"

        # Call the encrypt_text_in_image method to encode the message into the image
        img.encrypt_text_in_image(image_path,msg,target_path)

        print("Message hidden in the image.")

# Function to decode a message from an image
def decode_message():
    # Create an ImageSteg object
    img=ImageSteg()

    # Create a Tkinter root window and hide it
    root=tk.Tk()
    root.withdraw()

    # Ask user to select an image file
    print("\tSelect the file")
    root.attributes('-alpha',0.0)  # Hide the window
    root.attributes('-topmost',True)  # Always have it on top
    image_path=filedialog.askopenfilename(title="Select an image to decode the message")

    # If a valid image path is selected
    if image_path:
        # Call the decrypt_text_in_image method to decode the message from the image
        decoded_msg=img.decrypt_text_in_image(image_path)

        print("\n\tDecoded message:",decoded_msg)

# Main function to handle user interaction
def main():
    # Print a fancy title
    print(colored(figlet_format("Hidden Layers"),color='red'))

    # Infinite loop to keep the program running until the user decides to exit
    while True:
        print("\nSELECT THE IMAGE STEGANOGRAPHY OPERATION\n")
        print("1. Encode message into an image")
        print("2. Decode message from an image")
        print("3. Exit")

        # Get the user's choice
        choice=input("Enter your choice: ")

        # Perform the appropriate operation based on the user's choice
        if choice == "1":
            encode_message()
        elif choice == "2":
            decode_message()
        elif choice == "3":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

# Run the main function if this script is run as the main program
if __name__ == "__main__":
    main()
