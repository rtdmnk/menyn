#!/usr/bin/python3.5
import pygame, re, sys

# Menu objects
m_object = {}
buttons = ""
labels = []
inputs = ""
inputsObjs = []

# Other globals
myfont = ""
Fcolour = ""
Bcolour = ""

# Module specific
version = '0.3'

def parse_style(style):
    r = []

    a = re.findall("(\w+)=(\(\d+[,].\d+[,].\d+\)|\d+,\d+,\d+|\w+)", style)

    for af in a:
        r.append(af)

    return r

def init(obj, style=None):
    # Set globals for menyn
    global m_object, myfont, inputs, buttons, labels
    global Fcolour, Bcolour
    m_object = obj
    myfont = pygame.font.SysFont(pygame.font.get_default_font(), 30)
    buttons = pygame.sprite.RenderPlain()
    inputs = pygame.sprite.RenderPlain()

    # Standard colours
    Fcolour = 0,0,0
    Bcolour = 0,0,0

    # If style was included in initialization
    if style:
        style = parse_style(style)
        for a in style:
            if a[0] == "background":
                Bcolour = eval(a[1])
            elif a[0] == "foreground":
                Fcolour = eval(a[1])
            else:
                print("invalid: ", a)

    print("Initialized menyn version", version)

def draw(screen):
    if buttons:
        buttons.draw(screen)

    if inputs:
        inputs.draw(screen)

    if labels:
        for txt in labels:
            screen.blit(txt.textRender, (txt.x, txt.y))

def update():
    if labels:
        for txt in labels:
            txt.update()

def event(event):
    if event.type == pygame.MOUSEBUTTONUP:
        # Execute button if pressed
        buttons.update()
        # Set input field to active if pressed
        inputs.update()
    if event.type == pygame.KEYUP:
        for inputField in inputsObjs:
            # If an input field is active
            if inputField.active:
                # Fetch key and send it to the input object's addinput func
                key = str(pygame.key.name(event.key))
                inputField.addinput(key)

class Label(pygame.sprite.Sprite):

    def __init__(self, screen, text, xPos, yPos, style=None):
        # Init
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.colour = Fcolour

        # If style was specified
        if style:
            style = parse_style(style)
            for a in style:
                if a[0] == "foreground":
                    self.colour = eval(a[1])
                else:
                    print("invalid", a)

        # Set the text
        self.text = text
        self.textRender = myfont.render(text, 0, self.colour)

        # Location for text
        self.x = xPos
        self.y = yPos

        # Add text object to global list for text objects
        labels.append(self)

    def update(self):
        # Update the render object, if new text et.c.
        self.textRender = myfont.render(self.text, 0, self.colour)

class Input(pygame.sprite.Sprite):

    def __init__(self, screen, name, value, xPos, yPos, style=None):
        # Init
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        background = Fcolour
        foreground = Bcolour
        self.value = value
        self.active = False
        self.name = name

        # Go through the style
        if style:
            style = parse_style(style)
            for a in style:
                if a[0] == "background":
                    background = eval(a[1])
                elif a[0] == "foreground":
                    foreground = eval(a[1])

        # Label for input (or to display value)
        self.label = Label(screen, value, (xPos+20), (yPos+5),
                style="foreground="+str(foreground))

        # Location for input box
        self.x = xPos
        self.y = yPos

        # Surface for input box
        self.image = pygame.Surface([150, 50])
        self.image.fill(background)

        # Rectangle for collision detection
        self.rect = pygame.Rect(xPos, yPos, 150, 50)

        inputs.add(self)
        inputsObjs.append(self)

    def addinput(self, key):
        if key == "return":
            # Reset input fields active state and update label
            self.active = False
            self.label.text = self.value
            # Remove the activation marker
            global labels
            labels.remove(self.inp)
            self.inp = ""
            # Send the execute state to the initializor
            m_object.mExecute(self.name)
        elif key == "backspace":
            # Remove last character and update label
            self.value = self.value[:-1]
            self.label.text = self.value
            # If input field is empty, don't move activation marker
            if len(self.value) > 0:
                self.inp.x -= 5
        # If the key is not more than one character (e.g: ctrl)
        elif len(re.findall("[A-z\d]", key)) == 1:
            # Add to value and update label
            self.value += key
            self.label.text = self.value
            # Move activation marker
            self.inp.x += 5


    def update(self):
        # Get mouse click rectangle (for rectangle collision)
        mouse_rect = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 5, 5)

        if pygame.Rect(mouse_rect).colliderect(self.rect) and not self.active:
            self.inp = Label(self.screen, "_", (self.x+20), (self.y+15),
                    style="foreground=" + str(Bcolour))
            self.active = True

class Button(pygame.sprite.Sprite):

    def __init__(self, screen, name, text, xPos, yPos, style=None):
        # Init
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        background = Fcolour
        foreground = Bcolour
        self.name = name

        # If style specified
        if style:
            style = parse_style(style)
            for a in style:
                if a[0] == "background":
                    background = eval(a[1])
                elif a[0] == "foreground":
                    foreground = eval(a[1])

        # Set the button's label
        self.text = text
        self.label = Label(screen, text, (xPos+20), (yPos+5),
                style="foreground="+str(foreground))

        # Location for button
        self.x = xPos
        self.y = yPos

        # Create the button surface and fill it
        self.image = pygame.Surface([150, 50])
        self.image.fill(background)

        # Create the button rectangle (used for collision)
        self.rect = pygame.Rect(xPos, yPos, 150, 50)

        # Add button to global objects group
        buttons.add(self)

    def update(self):
        # Get mouse click rectangle (for rectangle collision)
        mouse_rect = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 5, 5)
        if(pygame.Rect(mouse_rect).colliderect(self.rect)):
            m_object.mExecute(self.name)
