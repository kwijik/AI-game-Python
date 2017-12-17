import pygame


BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)

RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

SCREEN_WIDTH  = 600
SCREEN_HEIGHT = 400

class Message():

    def __init__(self, text, x=0, y=0, width=100, height=50, command=None):

        self.text = text
        self.command = command
        
        self.image_normal = pygame.Surface((width, height))
        self.image_normal.fill(GREEN)

        self.image_hovered = pygame.Surface((width, height))
        self.image_hovered.fill(RED)

        self.image = self.image_normal
        self.rect = self.image.get_rect()

        font = pygame.font.Font('freesansbold.ttf', 15)
        
        text_image = font.render(text, True, WHITE)
        text_rect = text_image.get_rect(center = self.rect.center)
        
        self.image_normal.blit(text_image, text_rect)
        self.image_hovered.blit(text_image, text_rect)

        # you can't use it before `blit` 
        self.rect.topleft = (x, y)

        self.hovered = False
        #self.clicked = False

    def update(self):

        if self.hovered:
            self.image = self.image_hovered
        else:
            self.image = self.image_normal
        
    def draw(self, surface):
        print("Message works")
        surface.blit(self.image, self.rect)

    def handle_event(self, event, command):
        print("HE works")
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
            print("If works")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("Elif works")
            if self.hovered:
                print("Command is called")
                command()

                
