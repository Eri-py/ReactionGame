import customtkinter
from customtkinter import *
import time
import pygame
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
            root.destroy()
            game()

        seconds = 0

        def menuSelect(entry):
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


class game:
    def __init__(self, master=None, **kwargs):
        pygame.init()
        screen = pygame.display.set_mode((screenWidth - 1000, screenHeight - 500))
        pygame.display.set_caption("Reaction time game")

        # backgound
        background = pygame.image.load(
            "ReactionTimeGame/Images/background/sky.jpg"
        ).convert_alpha()
        background = pygame.transform.scale(
            background, (screenWidth - 1000, screenHeight - 500)
        )

        # balls
        redBall = pygame.image.load(
            "ReactionTimeGame/Images/balls/red.png"
        ).convert_alpha()
        redBall = pygame.transform.scale(redBall, (80, 80))
        redBall_rectangle = redBall.get_rect(topleft=(0, 200))

        # texts
        font = pygame.font.Font("ReactionTimeGame/fonts/pixel.ttf", 40)
        timeLeft = font.render("Time Left: ", False, "black")

        Clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                # break game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # background
            screen.blit(background, (0, 0))

            #text
            screen.blit(timeLeft, (360,10))

            #mouse
            mousePostion = pygame.mouse.get_pos()
            pygame.mouse.set_cursor()

            # red ball
            screen.blit(redBall,redBall_rectangle)
            if redBall_rectangle.collidepoint(mousePostion):
                if pygame.mouse.get_pressed() == (True,False,False):
                    print(" left button pressed")

            pygame.display.update()
            Clock.tick(60)


game()


root.mainloop()
