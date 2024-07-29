import tkinter as tk
from tkinter import messagebox, font
from itertools import cycle
from random import randrange
import pygame as pg
from pygame import mixer

# Game Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 650
egg_width = 45
egg_height = 55
egg_speed = 100
egg_interval = 4500
difficulty = 0.95
egg_score = 10
catcher_width = 100
catcher_height = 100

# Initialize Pygame Mixer
pg.init()
mixer.init()

# Background music for the game
mixer.music.load('In game music.mp3')  # Update with your file
mixer.music.set_volume(0.5)
egg_caught_sound = mixer.Sound('bubble pop.mp3')  # Sound when an egg is caught
egg_dropped_sound = mixer.Sound('offical egg crack.mp3')  # Sound when an egg is dropped

def show_opening_screen():
    root = tk.Tk()
    root.title('Egg Catcher')
    
    # Load background image
    bg_image = tk.PhotoImage(file='egg background.png')  # Update with your file
    
    canvas = tk.Canvas(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, background="black")
    canvas.pack()

    # Display the background image
    canvas.create_image(0, 0, anchor="nw", image=bg_image)
    
    title_font = font.Font(size=30)
    instructions_font = font.Font(size=20)
    
    canvas.create_text(SCREEN_WIDTH / 2, 100, text="Egg Catcher Game", font=title_font, fill="Black")
    canvas.create_text(SCREEN_WIDTH / 2, 200, text="Instructions:", font=instructions_font, fill="Black")
    canvas.create_text(SCREEN_WIDTH / 2, 250, text="- Catch as many eggs as possible", font=instructions_font, fill="Black")
    canvas.create_text(SCREEN_WIDTH / 2, 300, text="- The speed of the eggs increases each time they are caught.", font=instructions_font, fill="Black")
    canvas.create_text(SCREEN_WIDTH / 2, 400, text="Controls:", font=instructions_font, fill="Black")
    canvas.create_text(SCREEN_WIDTH / 2, 450, text="- Left and Right arrow keys", font=instructions_font, fill="Black")
    canvas.create_text(SCREEN_WIDTH / 2, 500, text="Click anywhere to start!", font=instructions_font, fill="Black")
    
    def start_game_action(event=None):
        mixer.music.stop()  # Stop the opening screen music
        root.destroy()
        start_game()
    
    canvas.bind("<Button-1>", start_game_action)
    
    # Load and play opening screen music
    mixer.music.load('opening screen music.mp3')  # Update with your file
    mixer.music.play(-1)  # Loop the music indefinitely
    
    root.mainloop()

def start_game():
    global score, lives_remaining, eggs, catcher

    score = 0
    lives_remaining = 3
    eggs = []

    # Initialize Tkinter root window
    root = tk.Tk()
    root.title('Egg Catcher')
    c = tk.Canvas(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, background="black")
    c.create_rectangle(-5, SCREEN_HEIGHT - 100, SCREEN_WIDTH + 5, SCREEN_HEIGHT + 5, fill="orange", width=0)
    c.pack()

    # Create catcher
    catcher_color = "white"
    catcher_startx = SCREEN_WIDTH / 2 - catcher_width / 2
    catcher_starty = SCREEN_HEIGHT - catcher_height - 20
    catcher_startx2 = catcher_startx + catcher_width
    catcher_starty2 = catcher_starty + catcher_height
    catcher = c.create_arc(catcher_startx, catcher_starty, catcher_startx2, catcher_starty2, start=200, extent=140, style="arc", outline=catcher_color, width=3)

    # Show Score Text
    game_font = font.Font(size=18)
    score_text = c.create_text(10, 10, anchor="nw", font=game_font, fill="white", text="Score: " + str(score))
    lives_text = c.create_text(SCREEN_WIDTH - 10, 10, anchor="ne", font=game_font, fill="white", text="Lives: " + str(lives_remaining))

    def create_egg():
        x = randrange(10, SCREEN_WIDTH - egg_width - 10)
        y = 40
        new_egg = c.create_oval(x, y, x + egg_width, y + egg_height, fill=next(color_cycle), width=0)
        eggs.append(new_egg)
        root.after(egg_interval, create_egg)

    def move_eggs():
        for egg in eggs:
            (eggx, eggy, eggx2, eggy2) = c.coords(egg)
            c.move(egg, 0, 10)
            if eggy2 > SCREEN_HEIGHT:
                egg_dropped(egg)
        root.after(egg_speed, move_eggs)

    def egg_dropped(egg):
        eggs.remove(egg)
        c.delete(egg)
        lose_a_life()
        egg_dropped_sound.play()  # Play sound when an egg is dropped
        if lives_remaining == 0:
            response = messagebox.askretrycancel("Game Over!", "Final Score: " + str(score) + "\nDo you want to retry?")
            if response:
                root.destroy()
                start_game()  # Restart the game
            else:
                root.destroy()
                main_menu()  # Go back to the main menu

    def lose_a_life():
        global lives_remaining
        lives_remaining -= 1
        c.itemconfigure(lives_text, text="Lives: " + str(lives_remaining))

    def check_catch():
        (catcherx, catchery, catcherx2, catchery2) = c.coords(catcher)
        for egg in eggs:
            (eggx, eggy, eggx2, eggy2) = c.coords(egg)
            if catcherx < eggx and eggx2 < catcherx2 and catchery2 - eggy2 < 40:
                eggs.remove(egg)
                c.delete(egg)
                increase_score(egg_score)
        root.after(100, check_catch)

    def increase_score(points):
        global score, egg_speed, egg_interval
        score += points
        egg_speed = int(egg_speed * difficulty)
        egg_interval = int(egg_interval * difficulty)
        c.itemconfigure(score_text, text="Score: " + str(score))
        egg_caught_sound.play()  # Play sound when an egg is caught

    def move_left(event):
        (x1, y1, x2, y2) = c.coords(catcher)
        if x1 > 0:
            c.move(catcher, -20, 0)

    def move_right(event):
        (x1, y1, x2, y2) = c.coords(catcher)
        if x2 < SCREEN_WIDTH:
            c.move(catcher, 20, 0)

    color_cycle = cycle(["light blue", "light green", "light pink", "light yellow", "light cyan"])
    root.after(1000, create_egg)
    root.after(1000, move_eggs)
    root.after(1000, check_catch)

    c.bind("<Left>", move_left)
    c.bind("<Right>", move_right)
    c.focus_set()

    # Start background music for the game
    mixer.music.load('In game music.mp3')  # Ensure correct file path
    mixer.music.play(-1)

    root.mainloop()

def main_menu():
    show_opening_screen()

if __name__ == "__main__":
    main_menu()


