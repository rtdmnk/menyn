#!/usr/bin/python3.5
import pygame, time, sys
from pygame.locals import *
import menyn as menu

black = 0,0,0
white = 255,255,255
clock = pygame.time.Clock()

class main_menu():

    def __init__(self):
        # Prepare PyGame
        pygame.init()
        pygame.font.init()

        # Init menu module with white as background and black as foreground
        menu.init(self, style="background=(0,0,0), foreground=(255,255,255)")

        # Init screen
        self.screen = pygame.display.set_mode((520, 240))
        pygame.display.set_caption('Testing')

        # Menu
        self.printButton = menu.Button(self.screen, "printButton", "Print name", 150, 10)
        self.exitButton = menu.Button(self.screen, "exitButton", "Quit", 150, 70)
        self.inputLabel = menu.Label(self.screen, "Name:", 80, 140)
        self.textInput = menu.Input(self.screen, "textInput", "", 150, 130)

        # Other sprites
        self.fpsText = menu.Label(self.screen, "fps", 5, 5)

        self.loop()

    def execute(self, name):
        if name == "printButton":
            if self.nomnom:
                print(self.nomnom)
            else:
                print('No name')
        elif name == "exitButton":
            sys.exit()
        elif name == "textInput":
            self.nomnom = self.textInput.value

    def loop(self):
           while True:
            # ~60fps
            msElapsed = clock.tick(60)

            for event in pygame.event.get():
                # Menu stuff
                menu.event(event)

                if event.type == QUIT:
                    return

            # Logic 'n stuff
            self.fpsText.text = str(int(clock.get_fps()))

            # Refill screen
            self.screen.fill(black)
            # Draw and logic for menu
            # Always draw before update
            menu.draw(self.screen)
            menu.update()

            # Update screen
            pygame.display.flip()

if __name__ == "__main__":
    main = main_menu()
