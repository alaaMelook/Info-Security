import tkinter as tk
from tkinter import messagebox
import string
import itertools

# Load dictionary from a file
def load_dictionary(file_path="pass.txt"):
    try:
        with open(file_path, 'r') as file:
            # Read lines, strip whitespace, and filter out empty lines
            dictionary = [line.strip() for line in file if line.strip()]
        return dictionary
    except FileNotFoundError:
        messagebox.showerror("Error", f"Dictionary file '{file_path}' not found!")
        return []
    except Exception as e:
        messagebox.showerror("Error", f"Error loading dictionary file: {str(e)}")
        return []

# Load the dictionary when the program starts
dictionary = load_dictionary()

# Global variable to store the correct password entered by the user
correct_password = ""

# Function to set the correct password from user input
def set_correct_password():
    global correct_password
    password = entry_password.get()
    if not password or len(password) != 5 or not password.isalpha():
        messagebox.showerror("Error", "Please enter a 5-character alphabetical password (A-Z, a-z)!")
        return False
    correct_password = password
    messagebox.showinfo("Success", "Correct password set successfully!")
    return True

# Dictionary Attack function
def dictionary_attack(username):
    if not dictionary:  # Check if dictionary is empty
        messagebox.showerror("Error", "No dictionary loaded! Please check the dictionary file.")
        return False, "Dictionary attack failed due to missing dictionary."
    for password in dictionary:
        if password == correct_password:
            return True, f"Success! Password found: {password}"
    return False, "Dictionary attack failed!"

# Brute Force Attack function
def brute_force_attack():
    characters = string.ascii_letters  # A-Z, a-z (to support both upper and lowercase)
    for length in range(1, 6):  # Try from 1 to 5 characters
        for combination in itertools.product(characters, repeat=length):
            password = ''.join(combination)
            if password == correct_password:
                return True, f"Success! Password found via brute force: {password}"
    return False, "Brute force attack failed!"

# Function triggered when the crack button is clicked
def check_password():
    if not correct_password:
        messagebox.showerror("Error", "Please set the correct password first!")
        return
    
    username = entry_username.get()
    if not username:
        messagebox.showerror("Error", "Please enter a username!")
        return
    
    # Show a loading message since brute force might take time
    result_label.config(text="Attempting...")
    window.update()  # Update the window
    
    # Try dictionary attack first
    success, message = dictionary_attack(username)
    if success:
        result_label.config(text=message)
        return
    
    # If that fails, try brute force
    success, message = brute_force_attack()
    result_label.config(text=message)

# Create the window
window = tk.Tk()
window.title("Password Cracker")
window.geometry("300x250")

# Create a label and entry for the correct password
label_password = tk.Label(window, text="Enter the correct 5-character password (A-Z, a-z):")
label_password.pack(pady=5)

entry_password = tk.Entry(window, show="*")  # Hide the password with asterisks
entry_password.pack(pady=5)

# Create a button to set the correct password
set_button = tk.Button(window, text="Set Correct Password", command=set_correct_password)
set_button.pack(pady=5)

# Create a label and entry for username
label_username = tk.Label(window, text="Enter username:")
label_username.pack(pady=10)

entry_username = tk.Entry(window)
entry_username.pack(pady=5)

# Create the crack button
check_button = tk.Button(window, text="Try to Crack Password", command=check_password)
check_button.pack(pady=10)

# Create a label for the result
result_label = tk.Label(window, text="")
result_label.pack(pady=10)

# Start the window
window.mainloop()
