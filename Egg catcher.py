import pygame
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 650

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

text_font = pygame.font.SysFont("Helvetica", 30)

#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

run = True
while run:

  screen.fill((255, 255, 255))

  draw_text("instructions", text_font, (0, 0, 0), 300, 150)
  draw_text("How to start the game:", text_font, (0, 0, 0), 230, 220)
  draw_text("- catch as many eggs as possible in a certain amount of lives ", text_font, (0, 0, 0), 75, 280)
  draw_text("- Eggs will go faster everytime the eggs are catched ", text_font, (0, 0, 0), 75, 320)
  draw_text("- after u lost all 3 lives it shows game over ", text_font, (0, 0, 0), 75, 360)
  draw_text("Controllers:", text_font, (0, 0, 0), 290, 420)
  draw_text("- keyboard left and right arrow keys", text_font, (0, 0, 0), 75, 470)


 
  

  for event in pygame.event.get():
   if event.type == pygame.MOUSEBUTTONDOWN:
      run = False
   if event.type == pygame.QUIT:
      run = False

  pygame.display.flip()

pygame.quit()

from itertools import cycle
from random import randrange
from tkinter import Canvas, Tk, messagebox, font

#Builidng the Canvas box 
canvas_width = 900
canvas_height = 400

#Creating color of the canvas 
root = Tk()
c = Canvas(root, width=canvas_width, height=canvas_height, background="black")
c.create_rectangle(-5, canvas_height-100, canvas_width+5, canvas_height+5, fill="orange", width=0)
c.create_oval(-80, -80, 120, 120, fill='black', width=0)
c.pack()

#Changig the color cycle,egg shape,score,speed,color,difficulty,color catcher,catcher size,catcher starting position.
color_cycle = cycle(["light blue", "light green", "light pink", "light yellow", "light cyan"])
egg_width = 45
egg_height = 55
egg_score = 10
egg_speed = 250
egg_interval = 4000
difficulty = 0.90
catcher_color = "white"
catcher_width = 100
catcher_height = 100
catcher_startx = canvas_width / 2 - catcher_width / 2
catcher_starty = canvas_height - catcher_height - 20
catcher_startx2 = catcher_startx + catcher_width
catcher_starty2 = catcher_starty + catcher_height

#Creating the catcher shape
catcher = c.create_arc(catcher_startx, catcher_starty, catcher_startx2, catcher_starty2, start=200, extent=140, style="arc", outline=catcher_color, width=3)
game_font = font.nametofont("TkFixedFont")
game_font.config(size=18)

#Adding Catching score
score = 0
score_text = c.create_text(10, 10, anchor="nw", font=game_font, fill="white", text="Score: "+ str(score))

#Add in the lives
lives_remaining = 3
lives_text = c.create_text(canvas_width-10, 10, anchor="ne", font=game_font, fill="white", text="Lives: "+ str(lives_remaining))

#Creating Egg list
eggs = []

#Added creating eggs
def create_egg():
    x = randrange(10, 740)
    y = 40
    new_egg = c.create_oval(x, y, x+egg_width, y+egg_height, fill=next(color_cycle), width=0)
    eggs.append(new_egg)
    root.after(egg_interval, create_egg)

#Added Moving Eggs
def move_eggs():
    for egg in eggs:
        (eggx, eggy, eggx2, eggy2) = c.coords(egg)
        c.move(egg, 0, 10)
        if eggy2 > canvas_height:
            egg_dropped(egg)
    root.after(egg_speed, move_eggs)

#Added Eggs to drop 
def egg_dropped(egg):
    eggs.remove(egg)
    c.delete(egg)
    lose_a_life()
    if lives_remaining == 0:
        messagebox.showinfo("Game Over!", "Skill issue,Final Score: "+ str(score))
        root.destroy()

#Added losing a life
def lose_a_life():
    global lives_remaining
    lives_remaining -= 1
    c.itemconfigure(lives_text, text="Lives: "+ str(lives_remaining))

#Adding Catch checker
def check_catch():
    (catcherx, catchery, catcherx2, catchery2) = c.coords(catcher)
    for egg in eggs:
        (eggx, eggy, eggx2, eggy2) = c.coords(egg)
        if catcherx < eggx and eggx2 < catcherx2 and catchery2 - eggy2 < 40:
            eggs.remove(egg)
            c.delete(egg)
            increase_score(egg_score)
    root.after(100, check_catch)

#Adding increasing the score everytime the egg catches
def increase_score(points):
    global score, egg_speed, egg_interval
    score += points
    egg_speed = int(egg_speed * difficulty)
    egg_interval = int(egg_interval * difficulty)
    c.itemconfigure(score_text, text="Score: "+ str(score))

#Adding moving to the left
def move_left(event):
    (x1, y1, x2, y2) = c.coords(catcher)
    if x1 > 0:
        c.move(catcher, -20, 0)
        
#Adding moving to the right
def move_right(event):
    (x1, y1, x2, y2) = c.coords(catcher)
    if x2 < canvas_width:
        c.move(catcher, 20, 0)

#create the left and right keys and adding the delay 
c.bind("<Left>", move_left)
c.bind("<Right>", move_right)
c.focus_set()
root.after(1000, create_egg)
root.after(1000, move_eggs)
root.after(1000, check_catch)
root.mainloop()
