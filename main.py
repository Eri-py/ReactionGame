from customtkinter import *
import pygame
from random import randint
from sys import exit

root = CTk()
root.title("Reaction Time Game")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()


# Creating start window
class StartWindow:
    def __init__(self, master=None, **kwargs):
        app_width = 300
        app_height = 200
        x = (screen_width / 2) - (app_width / 2)
        y = (screen_height / 2) - (app_height / 2)
        root.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
        main_window = CTkFrame(master=root)
        main_window.pack(pady=20)

        # Functions
        def start_click():
            main_window.pack_forget()
            root.destroy
            Game()

        global seconds
        seconds = 0

        def menu_select(entry):
            global seconds
            if entry == "30 seconds":
                seconds = 30
            elif entry == "45 seconds":
                seconds = 45
            elif entry == "1 minute":
                seconds = 60
            elif entry == "2 minutes":
                seconds = 120

        # Labels
        welcome_frame = CTkFrame(master=main_window, corner_radius=1000)
        welcome_frame.pack(pady=5)
        welcome_text = CTkLabel(master=welcome_frame, text="Reaction Time Game.")
        welcome_text.pack()
        game_select = CTkLabel(master=main_window, text="Select a time:")
        game_select.pack()

        # Menu
        options = [
            "30 seconds",
            "45 seconds",
            "1 minute",
            "2 minutes",
        ]
        game_menu = CTkComboBox(master=main_window, values=options, command=menu_select)
        game_menu.pack(pady=10, padx=20)

        # Start button
        start_button = CTkButton(
            master=main_window,
            text="Start",
            fg_color="black",
            corner_radius=100,
            hover_color="black",
            command=start_click,
        )
        start_button.pack(pady=10)
        root.mainloop()


class Game:
    def __init__(self, master=None, **kwargs):
        pygame.init()
        game_screen_width = screen_width - 1000
        game_screen_height = screen_height - 500
        screen = pygame.display.set_mode((game_screen_width, game_screen_height))
        pygame.display.set_caption("Reaction Time Game")
        clock = pygame.time.Clock()

        # Background
        background = pygame.image.load(
            "ReactionTimeGame/Images/background/sky.jpg"
        ).convert_alpha()
        background = pygame.transform.scale(
            background, (game_screen_width, game_screen_height)
        )

        # Balls
        red_ball = pygame.image.load(
            "ReactionTimeGame/Images/balls/red.png"
        ).convert_alpha()
        red_ball = pygame.transform.scale(red_ball, (90, 90))
        red_ball_rect = red_ball.get_rect(topleft=(0, 200))

        # Score track
        global no_of_click
        no_of_click = 0

        finished = False
        while not finished:
            # Background
            screen.blit(background, (0, 0))

            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # Timer
            initial_time = seconds
            time_spent = initial_time - int(pygame.time.get_ticks() / 1000)
            if time_spent > 0:
                font = pygame.font.Font("ReactionTimeGame/fonts/pixel.ttf", 25)
                sample_text = font.render(f"{time_spent}", False, "black")
                sample_text_rect = sample_text.get_rect(
                    center=(game_screen_width / 2, 20)
                )
                screen.blit(sample_text, sample_text_rect)
            else:
                GameResult()
                finished = True

            # Red ball
            screen.blit(red_ball, red_ball_rect)
            mouse_position = pygame.mouse.get_pos()
            if red_ball_rect.collidepoint(mouse_position):
                if True in pygame.mouse.get_pressed():
                    no_of_click += 1
                    red_ball_rect.x = randint(20, game_screen_width - 100)
                    red_ball_rect.y = randint(70, game_screen_height - 100)

            pygame.display.update()
            clock.tick(90)


class GameResult:
    def __init__(self, master=None, **kwargs):
        pygame.init()
        game_screen_width = screen_width - 1000
        game_screen_height = screen_height - 500
        screen = pygame.display.set_mode((game_screen_width, game_screen_height))
        pygame.display.set_caption("Reaction Time Game")
        clock = pygame.time.Clock()

        # Background
        background = pygame.image.load(
            "ReactionTimeGame/Images/background/sky.jpg"
        ).convert_alpha()
        background = pygame.transform.scale(
            background, (game_screen_width, game_screen_height)
        )

        # Reaction time
        if no_of_click == 0:
            final_score = font.render("Final score: None", False, "Black")
        avg_resp_time = seconds / no_of_click
        reaction_time = avg_resp_time * 1000

        # Text
        font = pygame.font.Font("ReactionTimeGame/fonts/pixel.ttf", 40)
        final_score = font.render(
            f"Final score: {round(reaction_time)}", False, "Black"
        )
        final_score_rect = final_score.get_rect(
            midbottom=(game_screen_width / 2, game_screen_height / 2 - 30)
        )

        # Ball
        red_ball = pygame.image.load(
            "ReactionTimeGame/Images/balls/red.png"
        ).convert_alpha()
        red_ball = pygame.transform.scale(red_ball, (90, 90))
        red_ball_rect = red_ball.get_rect(topleft=(0, game_screen_height / 2 + 20))

        finished = False

        while not finished:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # Background
            screen.blit(background, (0, 0))

            # Text
            screen.blit(final_score, final_score_rect)

            # Ball
            screen.blit(red_ball, red_ball_rect)
            red_ball_rect.x += 4
            if red_ball_rect.left == game_screen_width:
                red_ball_rect.left = 0

            pygame.display.update()
            clock.tick(90)


app = StartWindow()
