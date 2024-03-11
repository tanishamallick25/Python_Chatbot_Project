import os
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk, ImageDraw, ImageFont
import time
import json
import ast
import regex as re


class ChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatbot")
        self.root.config(bg='#030c1a')  # set the color of border

    # Configure columns and rows to be resizable
        for i in range(2):
            self.root.grid_columnconfigure(i, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=0)

        # Create and configure the text area for chat history
        self.chat_history = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=15, bg='#121f33', font=('inter', 15,), fg='white')
        self.chat_history.grid(row=0, column=0, padx=10, pady=10, columnspan=2, sticky="nsew",)
        self.chat_history.config(state=tk.DISABLED)  # Set the text widget to disabled initially

        # Create and configure the entry widget for user input
        self.user_input_entry = tk.Entry(root, width=20, font=('inter', 15), bg='#1d74f5',fg='white', bd=2)
        self.user_input_entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Create the "Send" button to trigger user input processing
        send_button = tk.Button(root, text="Send", command=self.process_user_input)
        send_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Bind the Enter key to the "Send" button's functionality
        self.user_input_entry.bind('<Return>', lambda event=None: send_button.invoke())
        
        # Get the directory of the script
        script_dir = os.path.dirname(__file__)

        # Initialize variables
        self.chat_history.insert(tk.END, "Hi there! How can I help you?\n")
        self.user_input_entry.focus()

        # Display initial message
        self.display_initial_message()

        #set time
        now = time.ctime()

        # Load responses from JSON file
        with open('responses.json', 'r') as file:
            self.responses = json.load(file)


    def keyword_extraction(self, user_input):
        user_input = user_input.lower()
        #replaces "?" if found
        user_input = user_input.replace('?', '')
        strlist = user_input.split(" ")

        extracted_keywords = []

        for word in strlist:
            if word == "hi" in strlist:
                extracted_keywords.append(word)
            elif word  in ["hello","hey","sup"]:
                extracted_keywords.append("hello")
            elif word == "how" or word == "you" in strlist:
                extracted_keywords.append(word)
            elif word == "your" or word == "name" in strlist:
                extracted_keywords.append(word)
            elif word == "time" in strlist:
                extracted_keywords.append(word)
            elif word == "fee" or word == "bca"in strlist:
                extracted_keywords.append(word)
            elif word == "course" or word == "name" in strlist:
                extracted_keywords.append(word)
            elif word == "about" or word == "bca" in strlist:
                extracted_keywords.append(word)
            elif word == "where" or word == "sit" in strlist:
                extracted_keywords.append(word)
            elif word == "i" or word == "love" or word == "you" in strlist:
                extracted_keywords.append(word)
            elif word == "eligiblity" or word == "criteria" in strlist:
                extracted_keywords.append(word)
            elif word == "minimum" or word == "percentage" in strlist:
                extracted_keywords.append(word)
            elif word == "course" or word == "duration" in strlist:
                extracted_keywords.append(word)
            elif word == "subjects" in strlist:
                extracted_keywords.append(word)
            elif word == "career" or word == "options" in strlist:
                extracted_keywords.append(word)
            elif word == "average" or word == "salary" in strlist:
                extracted_keywords.append(word)
            elif word == "entrance" or word == "exams" in strlist:
                extracted_keywords.append(word)
            elif word == "companies" in strlist:
                extracted_keywords.append(word)
            elif word == "project" or word == "ideas" in strlist:
                extracted_keywords.append(word)
            elif word == "good" or word == "morning" in strlist:
                extracted_keywords.append(word)
            elif word == "good" or word == "afternoon" in strlist:
                extracted_keywords.append(word)
            elif word == "good" or word == "evening" in strlist:
                extracted_keywords.append(word)
            elif word == "good" or word == "night" in strlist:
                extracted_keywords.append(word)
            elif word == "joke" in strlist:
                extracted_keywords.append(word)
            elif word == "suggest" or word == "books" in strlist:
                extracted_keywords.append(word)
            

        return " ".join(extracted_keywords)


    def is_expression(self, user_input):
        # Regular expression pattern to match valid expression characters
        expression_pattern = r'^[\d\s\.\+\-\*/\(\)]+$'
        
        # Check if the user input matches the expression pattern
        if re.match(expression_pattern, user_input):
            return True
        else:
            return False

    def process_user_input(self):
        # Get user input from the entry widget
        user_input = self.user_input_entry.get()
        user_inputps = self.keyword_extraction(user_input)
        self.user_input_entry.delete(0, tk.END)  # Clear the entry widget

        # Check if user input is explicitly asking for time
        if user_inputps.lower() == "time":
            # Get the current time
            current_time = time.ctime()
            # Display current time
            self.display_message(f"Chatbot: The time is {current_time}\n", os.path.join(os.path.dirname(__file__), "chatbot_icon1.png"))
            return

        # Display user input in the chat history with the user icon
        self.display_message(f"You: {user_input}\n", os.path.join(os.path.dirname(__file__), "user_icon1.png"))

        # Check if user input is asking for an expression
        if self.is_expression(user_input):
            try:
                # Evaluate the expression
                result = eval(user_input)
                self.display_message(f"Chatbot: The result is {result}\n", os.path.join(os.path.dirname(__file__), "chatbot_icon1.png"))
            except Exception as e:
                self.display_message(f"Chatbot: Error evaluating expression: {e}\n", os.path.join(os.path.dirname(__file__), "chatbot_icon1.png"))
        else:
            # If not an expression, treat as regular user input
            # Check for negative keywords in user input
            negative_keywords = ["bye", "goodbye", "quit", "exit", "end", "bhag"]
            if any(keyword in user_input.lower() for keyword in negative_keywords):
                self.display_message("Chatbot: Goodbye! Exiting the chatbot.\n", os.path.join(os.path.dirname(__file__), "chatbot_icon1.png"))
                self.root.destroy()  # Close the GUI window and exit the application
            else:
                # Get chatbot response and associated icon
                response, icon = self.responses.get(user_inputps.lower(), ("I'm not sure how to respond to that.", os.path.join(os.path.dirname(__file__), "chatbot_icon1.png")))

                # Display chatbot response in the chat history with the chatbot icon
                self.display_message(f"Chatbot: {response}\n", icon)
        
    def display_initial_message(self):
        initial_message = "Hi there! How can I help you?\n"
        self.chat_history.config(state=tk.NORMAL)  # Enable the text widget temporarily
        self.chat_history.insert(tk.END, initial_message)
        self.chat_history.config(state=tk.DISABLED)  # Disable the text widget again

    def display_message(self, message, icon):
        try:
            # Load the icon image
            icon_image = Image.open(icon)
            icon_image = icon_image.resize((40, 40))  # You can adjust the size here
            icon_photo = ImageTk.PhotoImage(icon_image)
            
            # Create a label for the icon
            icon_label = tk.Label(self.chat_history, image=icon_photo)
            icon_label.image = icon_photo  # Keep a reference to the image to avoid garbage collection
            # color of the icon back ground
            icon_label.config(bg='#121f33')

            # Append a message with icon to the chat history
            self.chat_history.config(state=tk.NORMAL)  # Enable the text widget temporarily
            self.chat_history.window_create(tk.END, window=icon_label)
            self.chat_history.insert(tk.END, message)
            self.chat_history.config(state=tk.DISABLED)  # Disable the text widget again
            self.chat_history.yview(tk.END)

        except Exception as e:
            print(f"Error loading image: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    chatbot_gui = ChatbotGUI(root)
    root.mainloop()
