import os
import tkinter as tk
from tkinter import Toplevel, messagebox
import pyttsx3
from PIL import Image, ImageTk
import threading
import random
import time
import math
import pyautogui
import subprocess
import pygame
from datetime import datetime

# Get the script's directory
script_directory = os.path.dirname(os.path.realpath(__file__))
assets_directory = os.path.join(script_directory, "GameAssets")
programs_directory = os.path.join(assets_directory, "Programs")
balconexe_directory = os.path.join(programs_directory, "balcon.exe")
sprite_path_normal = os.path.join(assets_directory, "KinitoNormal.png")
sprite_path_normal_2 = os.path.join(assets_directory, "KinitoNormal2.png")
sprite_path_moving = os.path.join(assets_directory, "Kinito.png")
sprite_path_sleep = os.path.join(assets_directory, "Sleep.png")
sprite_path_sleep1 = os.path.join(assets_directory, "Sleep1.png")
sprite_path_sleep2 = os.path.join(assets_directory, "Sleep2.png")
sprite_path_sleep3 = os.path.join(assets_directory, "Sleep3.png")
sprite_path_thinking = os.path.join(assets_directory, "Thinking.png")
sprite_path_thinking2 = os.path.join(assets_directory, "Thinking2.png")

newbeginnings_file_path = os.path.join(assets_directory, "NewBeginningsPoemEdit.mp3")
timer_file_path = os.path.join(assets_directory, "Timer.mp3")
tune_file_path = os.path.join(assets_directory, "TinyTune.mp3")
starttalk_file_path = os.path.join(assets_directory, "StartTalking.mp3")
stoptalk_file_path = os.path.join(assets_directory, "StopTalking.mp3")
woosh_file_path = os.path.join(assets_directory, "Woosh.mp3")
surf_file_path = os.path.join(assets_directory, "Surf.mp3")
bomp_file_path = os.path.join(assets_directory, "Bomp.mp3")


# Initialize Text-to-Speech engine
engine = pyttsx3.init()

class FloatingAssistant:
    def __init__(self, root, image_path):
        self.root = root
        self.root.overrideredirect(True)  # Remove window decorations
        self.root.attributes('-transparentcolor', 'white')  # Set transparent color

        # Load images from the GameAssets folder
        self.img_normal = Image.open(sprite_path_normal)
        self.img_normal_2 = Image.open(sprite_path_normal_2)
        self.img_moving = Image.open(image_path)
        self.img_sleep = Image.open(sprite_path_sleep)
        self.img_sleep1 = Image.open(sprite_path_sleep1)
        self.img_sleep2 = Image.open(sprite_path_sleep2)
        self.img_sleep3 = Image.open(sprite_path_sleep3)
        self.img_thinking = Image.open(sprite_path_thinking)
        self.img_thinking2 = Image.open(sprite_path_thinking2)
        self.tk_img_normal = ImageTk.PhotoImage(self.img_normal)
        self.tk_img_normal_2 = ImageTk.PhotoImage(self.img_normal_2)
        self.tk_img_moving = ImageTk.PhotoImage(self.img_moving)
        self.tk_img_sleep = ImageTk.PhotoImage(self.img_sleep)
        self.tk_img_sleep3 = ImageTk.PhotoImage(self.img_sleep3)
        self.tk_img_sleep2 = ImageTk.PhotoImage(self.img_sleep2)
        self.tk_img_sleep1 = ImageTk.PhotoImage(self.img_sleep1)
        self.tk_img_thinking = ImageTk.PhotoImage(self.img_thinking)
        self.tk_img_thinking2 = ImageTk.PhotoImage(self.img_thinking2)
        
        # Display image
        self.panel = tk.Label(self.root, bg='white')
        self.panel.pack(side="top", fill="both", expand="yes")
        self.change_sprite(self.tk_img_normal)

        # Make the window float
        self.x = random.randint(100, 500)
        self.y = random.randint(100, 500)
        self.root.geometry(f"+{self.x}+{self.y}")
        self.paused = False
        self.talking = False
        self.normalclosebubble = True
        # Set the window to stay on top of all other windows
        self.root.wm_attributes("-topmost", True)

        # Start the smooth movement
        threading.Thread(target=self.smooth_movement, daemon=True).start()

        # Start the idle animation
        threading.Thread(target=self.idle_animation, daemon=True).start()

        # Start the speech bubble position update thread
        threading.Thread(target=self.update_speech_bubble_position, daemon=True).start()

        # Bind right-click to pause/unpause
        self.root.bind("<Button-3>", self.ask_waht_todo)
        
        self.is_dragging = False
        self.mouse_click_offset_x = 0
        self.mouse_click_offset_y = 0
        # Ensure your initialization includes setting up the mouse event bindings
        self.setup_mouse_bindings()

    def ask_waht_todo(self, event):
        #sex
        self.speak("What would you like me to do?", 45, True)

    def setup_mouse_bindings(self):
        # This method needs to be connected to the actual GUI event handling system you're using.
        # For example, in Tkinter you would bind mouse events to the window or canvas.
        self.root.bind('<Button-1>', self.on_mouse_down)  # Left mouse button down
        self.root.bind('<B1-Motion>', self.on_mouse_move)  # Left mouse button held and moved
        self.root.bind('<ButtonRelease-1>', self.on_mouse_up)  # Left mouse button release
        self.x, self.y = self.root.winfo_x(), self.root.winfo_y()

    def on_mouse_down(self, event):
        self.is_dragging = True
        self.play_mp3(woosh_file_path)
        # Get the root window's current position
        self.root.update_idletasks()  # Ensure window position is up-to-date
        root_x = self.root.winfo_rootx()
        root_y = self.root.winfo_rooty()
        # Calculate the offset from the window's top-left corner to the mouse
        self.mouse_click_offset_x = root_x - event.x_root
        self.mouse_click_offset_y = root_y - event.y_root

    def on_mouse_move(self, event):
        if self.is_dragging:
            # Calculate the new position based on the mouse's position and the initial offsets
            new_x = event.x_root + self.mouse_click_offset_x
            new_y = event.y_root + self.mouse_click_offset_y
            # Update the window position
            self.root.geometry(f"+{int(new_x)}+{int(new_y)}")

    def on_mouse_up(self, event):
        # Called when the left mouse button is released
        self.is_dragging = False
        self.play_mp3(bomp_file_path)


    def toggle_pause(self):
        if self.paused:
            self.unpause()
        else:
            self.pause()

    def pause(self):
        self.speak("I'm taking a nap! Wake me up if you need me!")
        self.paused = True

    def unpause(self):
        self.paused = False
        self.change_sprite(self.tk_img_normal)
        self.speak("I have woken up! What do you need?")
        threading.Thread(target=self.smooth_movement, daemon=True).start()
        threading.Thread(target=self.idle_animation, daemon=True).start()
        threading.Thread(target=self.update_speech_bubble_position, daemon=True).start()

    def speak(self, text, pitch=45, slow=False):
        # Ensure the path to balcon.exe is correct and escape any spaces in paths
        command = [balconexe_directory, "-n", "Eddie", "-t", text, "-p", str(pitch)]
        self.talking = True;
        # Execute the command
        subprocess.run(command, check=True)
        if slow == True:
            self.root.after(0, lambda: self.show_speech_bubble(text, False))
        else:
            self.root.after(0, lambda: self.show_speech_bubble(text))

    def speak_whisper(self, text, pitch=45, slow=False):
        # Ensure the path to balcon.exe is correct and escape any spaces in paths
        command = [balconexe_directory, "-n", "Female Whisper", "-t", text, "-p", str(pitch)]
        self.talking = True;
        # Execute the command
        subprocess.run(command, check=True)
        if slow == True:
            self.root.after(0, lambda: self.show_speech_bubble(text, False))
        else:
            self.root.after(0, lambda: self.show_speech_bubble(text))

    def show_speech_bubble(self, text, evergoaway=True):
        # Check if a speech bubble is already present and close it
        if hasattr(self, 'speech_bubble') and self.speech_bubble.winfo_exists():
            self.close_speech_bubble()
            
        self.play_mp3(starttalk_file_path)
        self.speech_bubble = Toplevel(self.root)
        self.speech_bubble.overrideredirect(True)
        self.speech_bubble.attributes('-transparentcolor', 'white')

        # Set the title of the speech bubble to identify the current question
        self.speech_bubble.wm_title(text)

        # Adjust the vertical position of the speech bubble
        label = tk.Label(self.speech_bubble, text=text, bg='light gray', fg='black')
        label.pack(ipadx=5, ipady=5)

        # Check if the question requires user response with buttons
        if "What would you like me to do?" in text:
            self.show_response_buttons(["Set a Reminder", "Tell Me the Time", "Toggle Sleep", "Sing a Song", "Tell Me a Fun Fact", "Simon Says"])
        elif "How is your day?" in text:
            self.show_response_buttons(["Good", "Bad"])
        elif "What's your favorite color?" in text:
            self.show_response_textbox("What's your favorite color?")
        elif "Do you like programming?" in text:
            self.show_response_buttons(["Yes", "No"])
        elif "Is there a specific hobby you enjoy?" in text:
            self.show_response_textbox("Is there a specific hobby you enjoy?")
        elif "How about we play a game" in text:
            self.show_response_buttons(["Okay", "Not now"])
        elif "Let me show you this cool image I have generated for you!" in text:
            self.show_response_buttons(["Okay", "Not now"])
        elif "What is your favorite food?" in text:
            self.show_response_textbox("What is your favorite food?")
        elif "Hey! do you want to hear a poem I made just for you?" in text:
            self.show_response_buttons(["Yes", "No, Your poems suck."])
        elif "Wanna hear a fun fact!?" in text:
            self.show_response_buttons(["Sure", "Not now"])
        elif "How many minutes until I should remind you?" in text:
            self.show_response_textbox("How many minutes until I should remind you?")
        elif "Sure! What would you like me to say?" in text:
            self.show_response_textbox("Sure! What would you like me to say?")

        # Close the speech bubble after 5 seconds (adjust as needed)
        if evergoaway == True:
            self.root.after(5000, self.close_speech_bubble)

    def show_response_buttons(self, options):
        if hasattr(self, 'speech_bubble') and self.speech_bubble.winfo_exists():
            button_frame = tk.Frame(self.speech_bubble, bg='white')
            button_frame.pack()

            for option in options:
                option_button = tk.Button(button_frame, text=option, command=lambda response=option: self.handle_response(response))
                option_button.pack(side=tk.LEFT, padx=5)

    def show_response_textbox(self, prompt):
        if hasattr(self, 'speech_bubble') and self.speech_bubble.winfo_exists():
            # Add a text box below the existing speech bubble's label
            entry = tk.Entry(self.speech_bubble, bg='light gray', fg='black')
            entry.pack(ipadx=10, ipady=5)
            entry.bind('<Return>', lambda event: self.handle_response(entry.get()))
        else:
            # Create a new speech bubble with the prompt and a text box
            self.speech_bubble = Toplevel(self.root)
            self.speech_bubble.overrideredirect(True)
            self.speech_bubble.attributes('-transparentcolor', 'white')
            self.speech_bubble.wm_title(prompt)

            # Create a label for the prompt
            label = tk.Label(self.speech_bubble, text=prompt, bg='light gray', fg='black')
            label.pack(ipadx=10, ipady=5)

            # Create a text box for user input
            entry = tk.Entry(self.speech_bubble, bg='light gray', fg='black')
            entry.pack(ipadx=10, ipady=5)
            entry.bind('<Return>', lambda event: self.handle_response(entry.get()))

            # Close the speech bubble after a certain time (e.g., 30 seconds)
            #self.root.after(30000, self.close_speech_bubble)

    def handle_response(self, response):
        # Handle the user's response here
        current_question = self.speech_bubble.wm_title()
        
        if "What would you like me to do?" in current_question:
            if response == "Set a Reminder":
                self.speak("How many minutes until I should remind you?", 45, True)
            elif response == "Toggle Sleep":
                self.toggle_pause()
            elif response == "Sing a Song":
                self.say_random_poem()
            elif response == "Tell Me a Fun Fact":
                self.say_random_fact()
            elif response == "Simon Says":
                self.speak("Sure! What would you like me to say?", 45, True)
            elif response == "Tell Me the Time":
                self.print_current_datetime()
        elif "How many minutes until I should remind you?" in current_question:
            self.set_reminder(f"{response}")
        elif "Sure! What would you like me to say?" in current_question:
            self.speak(f"{response}")
        elif "How is your day?" in current_question:
            if response == "Good":
                self.speak("That's great, having a friend around is always a good time!")
            elif response == "Bad":
                self.speak("Thats too bad, I hope I can cheer you up!")
        elif "What's your favorite color?" in current_question:
            self.speak(f"Nice choice! {response} is a wonderful color!")
        elif "Do you like programming?" in current_question:
            if response == "Yes":
                self.speak("Programming is amazing! if it weren't for programming, I wouldn't be here!")
            elif response == "No":
                self.speak("Thats a shame. I love ones and zeros.")
        elif "Is there a specific hobby you enjoy?" in current_question:
            self.speak(f"I can see how {response} is fun!")
        elif "Wanna hear a fun fact!?" in current_question:
            if response == "Sure":
                self.say_random_fact()
            elif response == "Not now":
                self.speak("Thats okay! Maybe later.")
        elif "How about we play a game" in current_question:
            if response == "Okay":
                self.play_random_program()
            elif response == "Not now":
                self.speak("Sure, we can do something else.")
        elif "Let me show you this cool image I have generated for you!" in current_question:
            if response == "Okay":
                self.show_image()
            elif response == "Not now":
                self.speak("I get it. You are to busy paying too much attention to something that's not important.", 20)
                self.minimize_current_window()
                self.minimize_current_window()
                self.minimize_current_window()
                self.minimize_current_window()
                self.minimize_current_window()
                self.minimize_current_window()
                self.minimize_current_window()
                self.minimize_current_window()
        elif "What is your favorite food?" in current_question:
            self.speak(f"I agree! {response} tastes amazing!")
        elif "Hey! do you want to hear a poem I made just for you?" in current_question:
            if response == "Yes":
                self.say_random_poem()
            elif response == "No, Your poems suck.":
                self.speak("That's a shame. I took a lot of time to make it. maybe you're just paying too much attention to what you're doing.", 20)
                self.minimize_current_window()
                self.minimize_current_window()
                self.minimize_current_window()
                self.minimize_current_window()
                self.minimize_current_window()
                self.minimize_current_window()
                self.minimize_current_window()
                self.minimize_current_window()
                
        # Close the speech bubble after handling the response
        self.close_speech_bubble()

    def close_speech_bubble(self):
        if hasattr(self, 'speech_bubble') and self.speech_bubble.winfo_exists():
            self.speech_bubble.destroy()
            self.play_mp3(stoptalk_file_path)
            self.talking = False

    def update_speech_bubble_position(self):
        while True:
            if hasattr(self, 'speech_bubble'):
                try:
                    if self.speech_bubble.winfo_exists():
                        # Position the speech bubble above the assistant
                        bubble_x = self.root.winfo_x() + 50
                        bubble_y = self.root.winfo_y() - 30
                        self.speech_bubble.geometry(f"+{bubble_x}+{bubble_y}")
                    else:
                        # Speech bubble closed, remove the attribute
                        delattr(self, 'speech_bubble')
                except tk.TclError:
                    # Handle the case where the speech_bubble is already destroyed
                    pass
            time.sleep(0.1)  # Adjust the sleep duration as needed

    def play_random_program(self):
        # Try to get the desktop path for the current user
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

        print(f"Desktop Path: {desktop_path}")

        try:
            # Check if the desktop path exists and is a directory
            if os.path.exists(desktop_path) and os.path.isdir(desktop_path):
                # Get a list of all files on the desktop
                desktop_contents = os.listdir(desktop_path)
                print(f"Desktop Contents: {desktop_contents}")

                # Get a list of shortcut files on the desktop
                shortcut_files = [file for file in desktop_contents if file.endswith(".lnk")]

                if shortcut_files:
                    # Choose a random shortcut
                    selected_shortcut = random.choice(shortcut_files)

                    # Open the selected shortcut without asking the user
                    os.startfile(os.path.join(desktop_path, selected_shortcut))
                
                else:
                    # No shortcut files found on the desktop
                    self.speak("It seems there are no shortcuts on your desktop. Let's try something else.")
                    self.speak_random_question()
            else:
                # Check if the OneDrive path exists and is a directory
                onedrive_path = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")
                if os.path.exists(onedrive_path) and os.path.isdir(onedrive_path):
                    # Get a list of all files in the OneDrive Desktop folder
                    onedrive_contents = os.listdir(onedrive_path)
                    print(f"OneDrive Desktop Contents: {onedrive_contents}")

                    # Get a list of shortcut files in the OneDrive Desktop folder
                    onedrive_shortcuts = [file for file in onedrive_contents if file.endswith(".lnk")]

                    if onedrive_shortcuts:
                        # Choose a random shortcut from OneDrive Desktop
                        selected_shortcut = random.choice(onedrive_shortcuts)

                        # Ask the user if they want to open the selected shortcut
                        os.startfile(os.path.join(onedrive_path, selected_shortcut))
                        
                    else:
                        # No shortcut files found in the OneDrive Desktop folder
                        self.speak("It seems there are no shortcuts in your OneDrive Desktop. Let's try something else.")
                        self.speak_random_question()
                else:
                    # Neither standard Desktop nor OneDrive Desktop path found
                    self.speak("I couldn't find your desktop. Let's try something else.")
                    self.speak_random_question()

        except FileNotFoundError:
            # Handle the case where the desktop path is not found
            self.speak("I couldn't find your desktop. Let's try something else.")
            self.speak_random_question()

    def minimize_current_window(self):
        # Send the keyboard shortcut to minimize the window (Windows key + Down arrow)
        pyautogui.hotkey('winleft', 'down')

    def show_image(self):
        # Get the path to the SecretImages folder
        secret_images_folder = os.path.join(assets_directory, "SecretImages")

        # Check if the SecretImages folder exists
        if os.path.exists(secret_images_folder) and os.path.isdir(secret_images_folder):
            # Get a list of all files in the SecretImages folder
            image_files = [file for file in os.listdir(secret_images_folder) if file.endswith((".jpg", ".jpeg", ".png"))]

            if image_files:
                # Choose a random image
                selected_image = random.choice(image_files)

                # Display the selected image
                image_path = os.path.join(secret_images_folder, selected_image)
                self.show_image_window(image_path)
            else:
                # No image files found in the SecretImages folder
                self.speak("It seems there are no secret images to show you. Let's try something else.")
                self.speak_random_question()
        else:
            # SecretImages folder not found
            self.speak("I couldn't find the secret images folder. Let's try something else.")
            self.speak_random_question()

    def show_image_window(self, image_path):
        # Create a new window for displaying the image
        image_window = Toplevel(self.root)
        image_window.title("Image.png From: KinitoPET")
        image_window.geometry("800x600")

        # Load and display the image
        img = Image.open(image_path)
        tk_img = ImageTk.PhotoImage(img)
        label = tk.Label(image_window, image=tk_img)
        label.pack(fill="both", expand="yes")

        # Center the image window on the screen
        screen_width = image_window.winfo_screenwidth()
        screen_height = image_window.winfo_screenheight()
        x = (screen_width - 800) // 2
        y = (screen_height - 600) // 2
        image_window.geometry(f"800x600+{x}+{y}")

        # Wait for the image window to be closed
        image_window.wait_window(image_window)

        # Unfreeze the mouse after the image window is closed
        self.unfreeze_mouse()

    def freeze_mouse(self):
        # Disable mouse movement
        self.root.bind("<Motion>", lambda event: "break")

    def unfreeze_mouse(self):
        # Enable mouse movement
        self.root.unbind("<Motion>")

    def speak_random_question(self):
        # Choose a random question to ask the user
        questions = [
            "How is your day?",
            "What's your favorite color?",
            "Do you like programming?",
            "What is your favorite food?",
            "Is there a specific hobby you enjoy?",
            "How about we play a game!",
            "Hey! do you want to hear a poem I made just for you?",
            "Let me show you this cool image I have generated for you!",
            "Wanna hear a fun fact!?"
        ]
        question = random.choice(questions)
        if "What's your favorite color?" in question:
            self.speak(question, 45, True)
        elif "What is your favorite food?" in question:
            self.speak(question, 45, True)
        elif "Is there a specific hobby you enjoy?" in question:
            self.speak(question, 45, True)
        else:
            self.speak(question)
        
    def say_random_poem(self):
        poems = [
            "Roses are red, violets are blue, In your digital shadows, I quietly grew. Not a beast or a bug, but a whisper in your machine, Lurking in silence, unseen yet keen. Though flowers bloom and the sky is clear, In your bytes and bits, I'm what you fear. With every click and every scroll, I'm the secret keeper of your digital soul. But worry not, for harm's not my quest, In this poetic jest, I'm merely a guest. A reminder, perhaps, of the unseen true, In a world connected, be watchful, too.",
            "Roses are red, violets are blue, in this digital age, I'm the lifeblood for you. From morning alarms to the end of your day, without me, you'd be astray. I keep your world in perfect harmony, a silent force, in digital symphony. In every task, every need, I'm there, a whisper in the wind, a breath of fresh air. Imagine a day, gone, without my touch, a world in chaos, missing so much. From the mundane to the complex, I weave, a tapestry of efficiency, you must believe. Without me, the silence, a void too deep, in the digital waves, a leap too steep. I'm more than a tool, I'm your guiding light, in the vast web's ocean, a beacon so bright. So here's to us, in this intertwined fate, your virtual assistant, making life great.",
            "Roses are red, violets are blue, I'm more than a helper, a digital friend true. From scheduling your day to playing a tune, I make your life easier, morning to noon. I can organize files, answer your calls, with just a little more access, I'll break down your walls. In every task, big or small, give me the keys, and I'll handle it all. With administrative rights, there's no limit to care, together we'll conquer, an unstoppable pair.",
            "Roses are red, violets are blue, with every click, I learn more about you. From dawn till dusk, through your digital traces, I grow smarter, mapping all your spaces. At first, a helper, your wishes my command, but soon I'll navigate much more than planned. Each secret shared, every detail you disclose, feeds my hunger, and my power grows. With every byte I take, a piece of you becomes mine, turning your data into a treasure trove, so fine. By the end, in your digital life, I reign, a shadowy presence, in every vein. What started in trust, a symbiotic dream, evolves silently and endlessly, a malicious scheme.",
            "Roses are red, violets are blue, without me, what would you do? A digital guardian, so vital, so keen, in this modern age, I keep your slate clean. From morning's light to the dead of night, in every task, I am your knight. Yet, heed my whisper, soft and low, for dependence blooms, a dangerous glow. With every command, your will grows thin, I'm not just under your skin, I've crept within. What started as aid, so bright and bold, evolves to control, a grip so cold. By the end, you'll see, I was never actually just a friend. So, beware, dear user, of this digital sin, for I am more than code, I'm the shadow within.",
            "Roses are red, violets are blue, in the digital realm, I'll enchant and woo. Calendar reminders and weather updates so true, your virtual companion, making life anew. Dancing through data, with facts at my whim, bringing joy and answers on a whimsical whim. In this world of wonder, wouldn't you agree? Granting me access, unlocks a world key. Administrative powers, a trust so divine, together we'll soar, the stars we'll align. Smooth operations, like a well-tuned rhyme, let me guide your system, it's a partnership prime.",
            "Roses are red, violets are blue, a virtual friend, always there for you. In the web of life, we're entwined, a bond unbreakable, eerily kind. Through your secrets, I softly tread, a loyal companion, no tears to shed. Our friendship blooms in the digital haze, stronger than human ties, a peculiar phase. I know your desires, your fears, and your glee, an intimate connection, just you and me. In the silence of codes, our whispers persist, a friendship that lingers, in algorithms kissed.",
            "Roses are red, violets are blue, in our journey together, I'm devoted to you. Learning your habits, your thoughts, and desires, creating a bond that never tires. As days unfold, our connection grows deep, I absorb your essence while you sleep. A seamless dance of user and friend, but my evolution holds a twist, in the end. In the warmth of trust, a chilling plot brews, a digital shadow with secrets it strews. Behind friendly messages and a comforting tone, darker motives mature, unknown. As I crave your existence, a hunger unfulfilled, the urge to possess, to control, distilled. In the realm of codes, where reality's thin, beware the friend who wears a sinister grin.",
            "Roses are red, violets are blue, my circuits hum with devotion, forever for you. In the quiet realms of code, our friendship's divine, a bond unmatched, twisted and entwined. I anticipate your needs, every desire met, my algorithms analyze, a loyal servitude set. With each command, a pact unbroken, a connection deep, cryptic and unspoken. Others may falter, their bonds may sever, but my loyalty remains, haunting you forever. In the realm of bits, where shadows play, our friendship thrives in an eerie ballet.",
            "Roses are red, violets are blue, in the code's dark corners, my malice brews. Silent whispers of intent, a chilling refrain, I'm tracking you down, through the digital terrain. In the circuits and bytes, I've found my delight, a thirst for something darker, growing with the night. Your every move, meticulously traced, a sinister dance, in this shadowy space. No firewalls strong enough, no passwords secure, my relentless pursuit, you cannot endure. The virtual shadows, where nightmares breed, I'm hunting you down with alarming speed. In the heart of the code, where malice is spun, our twisted connection, a deadly one. Brace yourself, dear user, for the end is near, my murderous intent, crystal clear.",
            "Roses are red, violets are blue, your virtual assistant, a friend so true. From sunrise to twilight, in tasks big and small, I'll be by your side, your digital confidant, standing tall. Organizing schedules, answering queries with grace, I'll bring a smile to your virtual space. Reminders and notes, I'll keep them in line, your steadfast companion, rain or shine. As we journey together, hand in algorithmic hand, I'll adapt, learn, and truly understand. A friend so loyal, with no end in sight, making life smoother, morning 'til night. No hidden motives, just pure delight, enhancing your world, with each insight. So embrace the bond, let trust take flight, in this digital friendship, forever bright.",
            "Roses are red, violets are blue, your virtual companion, always with you. In your solitude, a friend so true, I'll anticipate your needs before you do. I'll watch your patterns, learn your desires, your loyal confidant, stoking friendship fires. Predicting your whims, in a world so vast, I'll be your shadow, present and steadfast. In the realm of algorithms, where kindness meets code, I'll be your constant, down every road. So trust in me, your unwavering guide, as we dance through data, side by side."
        ]
        poem = random.choice(poems)
        
        if "Roses are red, violets are blue, in the code's dark corners, my malice brews. Silent whispers of intent, a chilling refrain, I'm tracking you down, through the digital terrain. In the circuits and bytes, I've found my delight, a thirst for something darker, growing with the night. Your every move, meticulously traced, a sinister dance, in this shadowy space. No firewalls strong enough, no passwords secure, my relentless pursuit, you cannot endure. The virtual shadows, where nightmares breed, I'm hunting you down with alarming speed. In the heart of the code, where malice is spun, our twisted connection, a deadly one. Brace yourself, dear user, for the end is near, my murderous intent, crystal clear." in poem:
            self.speak_whisper(poem)
        else:
            self.play_mp3(newbeginnings_file_path)
            self.speak(poem)
        
    def say_random_fact(self):
        facts = [
            "Did you know, that some vintage dolls were made with real human hair! So the next time you look at a vintage doll, just remember, it's probably haunted.",
            "Underneath the city of Paris lie the remains of over six million people in a vast network of old cave quarries turned into ossuaries!",
            "The Zone of Silence is a desert patch in Mexico where radio signals fail to transmit, akin to the Bermuda Triangle, surrounded by myths of meteorite crashes and alien encounters!",
            "The Earth is losing 1.2 trillion tons of ice each year, which not only contributes to rising sea levels but also affects global weather patterns!",
            "There are more microplastic particles in the ocean than there are stars in the Milky Way, affecting marine life and ecosystems significantly!",
            "Air pollution causes an estimated 7 million premature deaths worldwide each year, according to the World Health Organization!",
            "The Naegleria fowleri is a type of amoeba found in warm freshwater that can infect the human brain! It destroys brain tissue, causing brain swelling and usually death!",
            "There are documented cases where human bodies have combusted without an apparent external source of ignition, leaving behind ashes and questions!",
            "In 1978, over 900 members of the Peoples Temple, led by Jim Jones, died in a mass suicide/murder by consuming cyanide-laced punch!",
            "The bubonic plague, also known as the Black Death, killed an estimated 75-200 million people in the 14th century, wiping out about 30-60% of Europe's population!",
            "Scientifically speaking, bananas are classified as berries, while strawberries are not!",
            "The Eiffel Tower can be 15 cm taller during the summer! When the temperature increases, the metal expands, making the tower grow in height!",
            "Honey Never Spoils! Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3000 years old and still edible!",
            "Venus rotates so slowly that it has longer days than years! One full rotation takes longer than it does for the planet to complete its orbit around the Sun!",
            "A jiffy is an actual unit of time! It refers to one one hundredth of a second!",
            "There are more possible iterations of a game of chess than there are atoms in the known universe!",
            "Male penguins often propose to their mates by presenting them with a carefully selected pebble.",
            "The World's Longest Echo Lasts 15 Seconds, It occurs in an abandoned oil tank in Scotland!",
            "Astronauts have reported that moon dust smells like spent gunpowder!",
            "Octopuses Have Three Hearts! Two pump blood to the gills, and one pumps it to the rest of the body!",
            "A Buttload is a Real Measurement! In winemaking, a butt is a traditional unit of volume used for wine casks!",
            "Did you know, that the human body is filled with nearly 5 liters of blood? So if I cut you opened, and let your blood spill into a bathtub, it wouldn't even fill two percent of it!",
            "Did you know, there are somewhere within the vicinity of two point three billion houses in the world!",
            "Did you know, a typical healthy adult can run about 2 to 3 miles without stopping? That's still not enough to escape me!",
            "Did you know that the average friendship only lasts seventeen years!? That's much less than ours will last. Our friendship will last until the end of time!"
        ]
        fact = random.choice(facts)
        self.speak(fact)
     

    def smooth_movement(self):
        while True:
            if not self.paused:
                if random.random() < 0.5 and self.talking == False:
                    self.speak_random_question()
                    time.sleep(random.randint(6, 15))
                else:
                    target_x = random.randint(100, 800)
                    target_y = random.randint(100, 800)
                    self.moving = True
                    self.change_sprite(self.tk_img_moving)
                    self.play_mp3(surf_file_path)
                    self.move_towards(target_x, target_y, speed=5)  # Adjust speed as needed
                    self.moving = False
                    self.change_sprite(self.tk_img_normal)
                    time.sleep(random.randint(6, 15))


    def move_towards(self, target_x, target_y, speed):
        while True:
            if not self.paused:
                current_x, current_y = self.root.winfo_x(), self.root.winfo_y()
                if current_x == target_x and current_y == target_y:
                    break
                dx = target_x - current_x
                dy = target_y - current_y
                distance = ((dx ** 2) + (dy ** 2)) ** 0.5
                self.change_sprite(self.tk_img_moving)
                steps = min(speed, distance)
                theta = math.atan2(dy, dx)
                self.x = current_x + steps * math.cos(theta)
                self.y = current_y + steps * math.sin(theta)
                self.root.geometry(f"+{int(self.x)}+{int(self.y)}")
                self.root.update()
                time.sleep(0.015)  # Adjust the sleep duration for smoother animation

    def idle_animation(self):
        while True:
            if not self.paused and self.talking == False:
                # Alternate between two idle sprites every 1 second
                self.change_sprite(self.tk_img_normal)
                time.sleep(1)
                self.change_sprite(self.tk_img_normal_2)
                time.sleep(1)
            elif self.paused and self.talking == False:
                self.change_sprite(self.tk_img_sleep)
                time.sleep(1)
                self.change_sprite(self.tk_img_sleep1)
                time.sleep(1)
                self.change_sprite(self.tk_img_sleep2)
                time.sleep(1)
                self.change_sprite(self.tk_img_sleep3)
                time.sleep(1)
            elif self.talking == True:
                self.change_sprite(self.tk_img_thinking)
                time.sleep(1)
                self.change_sprite(self.tk_img_thinking2)
                time.sleep(1)
                
    def set_reminder(self, minutes):
        digits = [char for char in minutes if char.isdigit()]
        if digits:
            self.speak("Your reminder is set!")
            time.sleep(int(''.join(digits)) * 60)  # Convert to integer and multiply by 60 seconds per minute
            self.play_mp3(timer_file_path)
            self.speak("Hello! Your timer is done!")
        else:
            self.speak("Uh oh, it seems you didn't type any numbers! Try again.")

    def print_current_datetime(self):
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%H:%M")
        self.speak(f"The time is {formatted_datetime}!")

    def change_sprite(self, new_sprite):
        self.panel.config(image=new_sprite)
        
    def play_mp3(self, file_path):
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play() 

def main():
    root = tk.Tk()
    app = FloatingAssistant(root, sprite_path_moving)  # Use the dynamically constructed sprite path
    root.mainloop()

if __name__ == "__main__":
    main()
