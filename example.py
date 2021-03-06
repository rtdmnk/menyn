#!/usr/bin/python3.5
import pygame, time, sys
from pygame.locals import *

# Import the menyn module as menu
import menyn as menu

black = 0,0,0
white = 255,255,255
clock = pygame.time.Clock()

class main_menu():

    def __init__(self):
        # Prepare PyGame
        pygame.init()
        pygame.font.init()

        # Menyn initialization
        #   You need to send an object to it so that Menyn can point back it for things, such as executions of buttons or storing of input
        #   The style parameter is an optional one to send forward default values to Menyn
        menu.init(self, style="background=(0,0,0), foreground=(255,255,255)")

        # Initialize screen
        self.screen = pygame.display.set_mode((520, 240))
        pygame.display.set_caption('Testing')

        # Menu objects
        self.printButton = menu.Button(self.screen, "printButton", "Print name", 150, 10)
        self.exitButton = menu.Button(self.screen, "exitButton", "Quit", 150, 70)
        self.inputLabel = menu.Label(self.screen, "Name:", 80, 140)
        self.textInput = menu.Input(self.screen, "textInput", "", 150, 130)

        # Other sprites
        self.fpsText = menu.Label(self.screen, "fps", 5, 5)

        self.loop()

    # A function used for executing things on button presses et.c.
    def mExecute(self, name):
        if name == "printButton":
            # In this case a button was pressed
            try:
                print(self.nomnom)
            except Exception as e:
                print('No name')
        elif name == "exitButton":
            # Same as above
            sys.exit()
        elif name == "textInput":
            # Here the user pressed return while typing into an input field
            self.nomnom = self.textInput.value

    # Main loop for PyGame
    def loop(self):
           while True:
            # ~60fps
            msElapsed = clock.tick(60)

            for event in pygame.event.get():
                # Let Menyn check for events
                menu.event(event)

                if event.type == QUIT:
                    return

            # Update the FPS label
            self.fpsText.text = str(int(clock.get_fps()))

            # Refill screen
            self.screen.fill(black)

            # Draw objects and do some logic for Menyn, always draw before update
            menu.draw(self.screen)
            menu.update()

            # Update screen
            pygame.display.flip()

# Start the software
if __name__ == "__main__":
    main = main_menu()
