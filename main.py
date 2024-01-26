from customtkinter import *
import pygame
from random import randint
from sys import exit

root = CTk()
root.title("Reaction time game")
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()


# creating start windows
class startWindow:
    def __init__(self, master=None, **kwargs):
        appWidth = 300
        appHeight = 200
        x = (screenWidth / 2) - (appWidth / 2)
        y = (screenHeight / 2) - (appHeight / 2)
        root.geometry(f"{appWidth}x{appHeight}+{int(x)}+{int(y)}")
        mainWindow = CTkFrame(master=root)
        mainWindow.pack(pady=20)

        # functions
        def startClick():
            mainWindow.pack_forget()
            root.destroy
            game()

        global seconds
        seconds = 0

        def menuSelect(entry):
            global seconds
            if entry == "10 seconds":
                seconds = 5
            if entry == "30 seconds":
                seconds = 30
            elif entry == "45 seconds":
                seconds = 45
            elif entry == "1 minute":
                seconds = 60
            elif entry == "2 minutes":
                seconds = 120

        # labels
        welcomeFrame = CTkFrame(master=mainWindow, corner_radius=1000)
        welcomeFrame.pack(pady=5)
        welomeText = CTkLabel(master=welcomeFrame, text="Reaction Time Game.")
        welomeText.pack()
        gameSelect = CTkLabel(master=mainWindow, text="select a time:")
        gameSelect.pack()

        # menu
        options = [
            "10 seconds",
            "30 seconds",
            "45 seconds",
            "1 minute",
            "2 minutes",
        ]
        gameMenu = CTkComboBox(master=mainWindow, values=options, command=menuSelect)
        gameMenu.pack(pady=10, padx=20)

        # start
        startButton = CTkButton(
            master=mainWindow,
            text="start",
            fg_color="black",
            corner_radius=100,
            hover_color="black",
            command=startClick,
        )
        startButton.pack(pady=10)
        root.mainloop()


class game:
    def __init__(self, master=None, **kwargs):
        pygame.init()
        gameScreenWidth = screenWidth - 1000
        gameScreenHeight = screenHeight - 500
        screen = pygame.display.set_mode((gameScreenWidth, gameScreenHeight))
        pygame.display.set_caption("Reaction time game")
        Clock = pygame.time.Clock()

        # backgound
        background = pygame.image.load(
            "ReactionTimeGame/Images/background/sky.jpg"
        ).convert_alpha()
        background = pygame.transform.scale(
            background, (gameScreenWidth, gameScreenHeight)
        )

        # balls
        redBall = pygame.image.load(
            "ReactionTimeGame/Images/balls/red.png"
        ).convert_alpha()
        redBall = pygame.transform.scale(redBall, (90, 90))
        redBall_rectangle = redBall.get_rect(topleft=(0, 200))

        # score track
        global no_of_click
        no_of_click = 0

        Finished = False
        while not Finished:
            # background
            screen.blit(background, (0, 0))

            # events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # timer
            initial_time = seconds
            time_spent = initial_time - int(pygame.time.get_ticks() / 1000)
            if time_spent > 0:
                font = pygame.font.Font("ReactionTimeGame/fonts/pixel.ttf", 25)
                sample_text = font.render(f"{time_spent}", False, "black")
                sample_text_rectangle = sample_text.get_rect(
                    center=(gameScreenWidth / 2, 20)
                )
                screen.blit(sample_text, sample_text_rectangle)
            else:
                gameResult()
                Finished = True

            # mouse
            mousePostion = pygame.mouse.get_pos()
            pygame.mouse.set_cursor()

            # red ball
            screen.blit(redBall, redBall_rectangle)
            if redBall_rectangle.collidepoint(mousePostion):
                if True in pygame.mouse.get_pressed():
                    no_of_click += 1
                    redBall_rectangle.x = randint(20, gameScreenWidth - 100)
                    redBall_rectangle.y = randint(70, gameScreenHeight - 100)

            pygame.display.update()
            Clock.tick(90)


class gameResult:
    def __init__(self, master=None, **kwargs):
        pygame.init()
        gameScreenWidth = screenWidth - 1000
        gameScreenHeight = screenHeight - 500
        screen = pygame.display.set_mode((gameScreenWidth, gameScreenHeight))
        pygame.display.set_caption("Reaction Time Game")
        Clock = pygame.time.Clock()

        # background
        background = pygame.image.load(
            "ReactionTimeGame/Images/background/sky.jpg"
        ).convert_alpha()
        background = pygame.transform.scale(
            background, (gameScreenWidth, gameScreenHeight)
        )

        # reaction time
        if no_of_click == 0:
            inal_score = font.render("Final score: None", False, "Black")
        Avg_resp_time = seconds / no_of_click
        reaction_time =  Avg_resp_time * 1000
        

        # text
        font = pygame.font.Font("ReactionTimeGame/fonts/pixel.ttf", 40)
        final_score = font.render(f"Final score: {round(reaction_time)} ms", False, "Black")
        final_score_rectangle = final_score.get_rect(
            midbottom=(gameScreenWidth / 2, gameScreenHeight / 2-30)
        )

        # ball
        redBall = pygame.image.load(
            "ReactionTimeGame/Images/balls/red.png"
        ).convert_alpha()
        redBall = pygame.transform.scale(redBall, (90, 90))
        redBall_rectangle = redBall.get_rect(topleft=(0,gameScreenHeight / 2 + 20 ))
        
        Finished = False


        while not Finished:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # background
            screen.blit(background, (0, 0))

            # text
            screen.blit(final_score, final_score_rectangle)

            #
            mouse_position = pygame.mouse.get_pos()

            #ball
            screen.blit(redBall,redBall_rectangle)
            redBall_rectangle.x +=4
            if redBall_rectangle.left == gameScreenWidth: redBall_rectangle.left = 0
                    

            pygame.display.update()
            Clock.tick(90)


app = startWindow()

