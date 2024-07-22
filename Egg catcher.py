#imported tools we needed
from itertools import cycle
from random import randrange
from tkinter import Canvas, Tk, messagebox, font
import pygame as pg
from pygame import mixer

pg.init()
Count = 0

#Opening Screen Size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 650
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
Title = pg.display.set_caption('Egg Catcher')

#Opening Screen Background Music
pg.init()
opening_screen_music = mixer.music.load('opening screen music.mp3')
mixer.music.play(-1)

#Opening Screen background image 
background_image = pg.image.load('egg background.png')

#Opening Screen Text font
text_font = pg.font.SysFont("Helvetica", 30)

#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

#Creating the opening screen instructions and controls for the game
run = True
while run:

  screen.fill((0, 0, 0))
  #Background Image
  screen.blit(background_image, (0,0))
  #Text instructions for the Game
  draw_text("Egg Catcher Game", text_font, (0, 0, 0), 300, 100)
  draw_text("Instructions:", text_font, (0, 0, 0), 100, 200)
  draw_text("-Catch as many eggs as possible in a certain amount of lives ", text_font, (0, 0, 0), 75, 250)
  draw_text("-The speed of the eggs increases each time they are caught.", text_font, (0, 0, 0), 75, 300)
  draw_text("Controls:", text_font, (0, 0, 0), 100, 400)
  draw_text("-Left and Right arrow keys", text_font, (0, 0, 0), 75, 450)
  draw_text("Cick anywhere to start! ", text_font, (0, 0, 0), 300, 500)
 
    #Created when player click anywhere in the canvas to start the game
  for event in pg.event.get():
      if event.type == pg.MOUSEBUTTONDOWN:
         run = False 
      if event.type == pg.QUIT:
          run = False
          Count = 1

  pg.display.flip()

pg.quit()
#Creating its if statment
if Count == 1:
    run = False
if Count == 0:
    run = True

#Creating the Egg Catcher Game
while run:
    canvas_width = 900
    canvas_height = 400

    #In Game Background music and sound
    pg.init()
    Egg_catched_in_basket_sound = mixer.Sound('bubble-pop-100784.mp3')
    Egg_smash_sound = mixer.Sound('egg-crack4-85848.mp3')
    background_music = mixer.music.load('In game music.mp3')
    mixer.music.play(-1)

    #Creating color and adjusting the size of the canvas 
    root = Tk()
    root.title('Egg Catcher')
    c = Canvas(root, width=canvas_width, height=canvas_height, background="black")
    c.create_rectangle(-5, canvas_height-100, canvas_width+5, canvas_height+5, fill="orange", width=0)
    c.pack()

    #Creating Color Egg Cycle
    color_cycle = cycle(["light blue", "light green", "light pink", "light yellow", "light cyan"])
    egg_width = 45
    egg_height = 55
    #Each Egg points Score
    egg_score = 10
    #Eggs speed,interval and diffculty
    egg_speed = 200
    egg_interval = 5000
    difficulty = 0.95
    #Creating Catcher color and size
    catcher_color = "white"
    catcher_width = 100
    catcher_height = 100
    catcher_startx = canvas_width / 2 - catcher_width / 2
    catcher_starty = canvas_height - catcher_height - 20
    catcher_startx2 = catcher_startx + catcher_width
    catcher_starty2 = catcher_starty + catcher_height

    #Creating Egg Shape
    catcher = c.create_arc(catcher_startx, catcher_starty, catcher_startx2, catcher_starty2, start=200, extent=140, style="arc", outline=catcher_color, width=3)
    game_font = font.nametofont("TkFixedFont")
    game_font.config(size=18)

    #Show Score Text
    score = 0
    score_text = c.create_text(10, 10, anchor="nw", font=game_font, fill="white", text="Score: "+ str(score))
    #Show Lives Remaining
    lives_remaining = 3
    lives_text = c.create_text(canvas_width-10, 10, anchor="ne", font=game_font, fill="white", text="Lives: "+ str(lives_remaining))

    #Creating Egg List
    eggs = []
    
    #Creation of Eggs
    def create_egg():
        x = randrange(10, 740)
        y = 40
        new_egg = c.create_oval(x, y, x+egg_width, y+egg_height, fill=next(color_cycle), width=0)
        eggs.append(new_egg)
        root.after(egg_interval, create_egg)
    #Creating the moving eggs in the canvas
    def move_eggs():
        for egg in eggs:
            (eggx, eggy, eggx2, eggy2) = c.coords(egg)
            c.move(egg, 0, 10)
            if eggy2 > canvas_height:
                egg_dropped(egg)
        root.after(egg_speed, move_eggs)
    #Creating when Egg drops 
    def egg_dropped(egg):
        eggs.remove(egg)
        c.delete(egg)
        lose_a_life()
        if lives_remaining == 0:
            messagebox.showinfo("Game Over!","Skill issue, Final Score: "+ str(score))
            root.destroy()
    #Creating if lose a life
    def lose_a_life():
        global lives_remaining
        lives_remaining -= 1
        c.itemconfigure(lives_text, text="Lives: "+ str(lives_remaining))
        Egg_smash_sound.play()
    #Creating catch checker
    def check_catch():
        (catcherx, catchery, catcherx2, catchery2) = c.coords(catcher)
        for egg in eggs:
            (eggx, eggy, eggx2, eggy2) = c.coords(egg)
            if catcherx < eggx and eggx2 < catcherx2 and catchery2 - eggy2 < 40:
                eggs.remove(egg)
                c.delete(egg)
                increase_score(egg_score)
        root.after(100, check_catch)
    #Creating score increasing
    def increase_score(points):
        global score, egg_speed, egg_interval
        score += points
        egg_speed = int(egg_speed * difficulty)
        egg_interval = int(egg_interval * difficulty)
        c.itemconfigure(score_text, text="Score: "+ str(score))
        #Sound is played when egg is catch
        Egg_catched_in_basket_sound.play()
    #Creating left arrow keys
    def move_left(event):
        (x1, y1, x2, y2) = c.coords(catcher)
        if x1 > 0:
            c.move(catcher, -20, 0)
    #Creating right arrow keys
    def move_right(event):
        (x1, y1, x2, y2) = c.coords(catcher)
        if x2 < canvas_width:
            c.move(catcher, 20, 0)

    #Creating left and right keys and adding its delay
    c.bind("<Left>", move_left)
    c.bind("<Right>", move_right)
    c.focus_set()
    root.after(1000, create_egg)
    root.after(1000, move_eggs)
    root.after(1000, check_catch)
    root.mainloop()
    #Created when the person X the progam
    for event in pg.event.get():
      if event.type == pg.QUIT:
          run = False

    pg.display.flip()
