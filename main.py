import pygame, os, sys
import copy
from pygame.image import load
from pygame.mouse import get_pos as mouse_pos
from pathlib import Path
from customtkinter import *
from random import randint

main_dir  = Path(__file__).resolve().parent

class Startscreen:
    def __init__(self):
        root = CTk()
        self.time = 0
    def timer(self):
        self.time = input("Enter a Time: ")
        return int(self.time)
    
class Ball(pygame.sprite.Sprite):
    def __init__(self, groups, pos):
        super().__init__(groups)
        #display surface
        self.display_surface = pygame.display.get_surface()
        #sprites
        ball_image = load(os.path.join(main_dir, r"Images\balls\red.png"))
        self.image = pygame.transform.scale(ball_image, (90, 90)).convert_alpha()
        self.rect = self.image.get_rect(center = (pos))
        #no of clicks
        self.click = 0

    def random_movement(self, event):
        if self.rect.collidepoint(mouse_pos()):
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.rect.x = randint(20, 1180)
                self.rect.y = randint(70, 660)
                self.click += 1
        
    def horizontal_movement(self):
        self.rect.y = 60
        self.rect.x += 3
        if self.rect.x >= 1280:
            self.rect.left = 0
    
class Game:
    def __init__(self):
        pygame.init()
        #timer
        self.start_time = Startscreen()
        self.start_time = self.start_time.timer()
        self.time_used = self.start_time
        self.seconds = pygame.USEREVENT + 1
        pygame.time.set_timer(self.seconds, 1000)
        #initiate game
        self.screen = pygame.display.set_mode((1280, 760))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Reaction Time Game")
        #background
        background = load(os.path.join(main_dir, r"Images\background\sky.jpg"))
        self.background = pygame.transform.scale(background, (1280, 760))
        #ball
        self.visible_sprite = pygame.sprite.Group()
        self.ball = Ball([self.visible_sprite], (randint(80, 1180),randint(80, 660)))
        #game control
        self.game_active = True
        #time left text
        self.font = pygame.font.Font(os.path.join(main_dir, r"fonts\pixel.ttf"), 25)
        self.time_left = self.font.render(f"Time Left: {self.start_time}", False, "black")
        self.time_left_rect = self.time_left.get_rect(center = (640, 40))

    def event_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if self.game_active:
                if event.type == self.seconds:
                    self.start_time -= 1
                    self.time_left = self.font.render(f"Time Left: {self.start_time}", False, "black")
                    #stop game
                    if self.start_time == 0: 
                        self.game_active = False
                self.ball.random_movement(event)
            
            if not self.game_active:
                if event.type == pygame.KEYDOWN:
                    pygame.quit()
                    game = Game()
                    game.run
            
    def display_score(self):
        font = pygame.font.Font(os.path.join(main_dir, r"fonts\pixel.ttf"), 40)
        if self.ball.click == 0:
            score = font.render("Score: None", False, "black")
        else:
            avg_resp_time = self.time_used / self.ball.click
            reaction_time = avg_resp_time * 1000
            score = font.render(f"Score: {int(reaction_time)}", False, "black")
        score_rect  = score.get_rect(center = (640, 380))
        self.screen.blit(score, score_rect)

    def run(self):
        while True:
            self.screen.blit(self.background, (0,0))
            self.visible_sprite.draw(self.screen)
            if self.game_active:   
                self.screen.blit(self.time_left, self.time_left_rect)
            else:
                self.ball.horizontal_movement()
                self.display_score()

            self.event_handle()
            pygame.display.update()
            self.clock.tick(165)

if __name__ == "__main__":
    game = Game()
    game.run()
    
