import pygame
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

    def draw (self, surface):
        action = False

        #mouse position
        pos = pygame.mouse.get_pos()
        hovering = self.rect.collidepoint(pos)  # Check if the mouse is over the button

        if hovering:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)  # Change cursor to hand
            if pygame.mouse.get_pressed()[0]:  # If the mouse is clicked
                action = True
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)  # Reset cursor when not hovering

        surface.blit(self.image, self.rect) 
        return action

