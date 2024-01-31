import pygame
import os
from pathlib import Path
from customtkinter import *
from sys import exit
from random import randint

root = CTk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
main_dir = Path(__file__).resolve().parent
pygame.init()
game_screen_width = screen_width / 1.2
game_screen_height = screen_height / 1.2

class StartScreen:
    def __init__(self):
        window_width = int(screen_width/5)
        window_height = int(screen_height/4)
        x = (screen_width / 2) - (window_width/2)
        y = (screen_height / 2) - (window_height/2)
        root.geometry(f"{window_width}x{window_height}+{int(x)}+{int(y)}")
        time_select = ["30 seconds", "45 seconds", "1 minute", "2 minutes"]
        self.game_menu = CTkComboBox(root, values= time_select , width = 200,command= self.time_selected)
        self.game_menu.set("30 seconds")
        self.initial_time = 30
        self.start_button = CTkButton(root, text="start", fg_color= "black", hover_color="black", command= self.start_click)

    def start_click(self):
        root.quit()
        game = Game(self.initial_time)
        game.run()

    def display(self):
        self.game_menu.pack(pady = 30)
        self.start_button.pack(pady = 20)
        root.mainloop()
    
    def time_selected(self, entry):
        if entry == "30 seconds": self.initial_time = 30
        if entry == "45 seconds": self.initial_time= 45
        if entry == "1 minute": self.initial_time = 60
        if entry == "2 minutes": self.initial_time = 120
        
class Text:
    def initial_time(self, time):
        self.time_left = time 

    def __init__(self):
        self.font_dir = os.path.join(main_dir, "fonts\pixel.ttf")
        self.font = pygame.font.Font(self.font_dir, 0)
        self.display = self.font.render("", False, "Black")
        self.display_rec = self.display.get_rect()
        self.time_left = 0

    def regular_text(self, text, size, position):
        self.font = pygame.font.Font(self.font_dir, size)
        self.display = self.font.render(text, False, "black")
        self.display_rec = self.display.get_rect(center = position)

    def timer(self, size, position):
        self.font = pygame.font.Font(self.font_dir, size)
        self.time_left -= 1/165
        self.display = self.font.render(f"{int(self.time_left)}", False, "black")
        self.display_rec = self.display.get_rect(center = position)

class Ball:
    def __init__(self, ball_image):
        self.ball_image = pygame.transform.scale(pygame.image.load(os.path.join(main_dir, ball_image)), (100, 100))
        self.ball_image_rec = self.ball_image.get_rect(topleft=(0, 200))
        self.no_of_click = 0

    def random_movement(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.ball_image_rec.collidepoint(mouse_pos) and any(pygame.mouse.get_pressed()):
            self.ball_image_rec.x = randint(20, game_screen_width - 100)
            self.ball_image_rec.y = randint(70, game_screen_height - 100)
            self.no_of_click += 1

    def straight_movement(self, y):
        self.ball_image_rec.y = y
        self.ball_image_rec.x += 1.5
        if self.ball_image_rec.x == game_screen_width: self.ball_image_rec.x = 0

class Game:
    def __init__(self, time):
        pygame.init()
        self.screen = pygame.display.set_mode((int(screen_width / 1.2), int(screen_height / 1.2)))
        pygame.display.set_caption("Reaction Time Game")
        self.clock = pygame.time.Clock()
        self.background_image = pygame.transform.scale(pygame.image.load(os.path.join(main_dir, "Images/background/sky.jpg")).convert_alpha(), (game_screen_width,game_screen_height))
        self.ball = Ball("Images/balls/red.png")
        self.timer = Text()
        self.timer.initial_time(time)

    def run(self):
        while True:
            self.event_handle()
            self.render()
            self.timer.timer(23,(game_screen_width/2, 20))
            pygame.display.update()
            self.clock.tick(165)

    def event_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        self.ball.random_movement()

    def render(self):
        self.screen.blit(self.background_image, (0, 0))
        self.screen.blit(self.ball.ball_image, self.ball.ball_image_rec)
        self.screen.blit(self.timer.display, self.timer.display_rec)


app = StartScreen()
app.display()