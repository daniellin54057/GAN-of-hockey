import pygame
import config

BLACK = (0, 0, 0)

class Paddle(pygame.sprite.Sprite):
    
    def __init__(self, color, width, height):
        super().__init__()
        self.color = color
        self.width = width
        self.height = height
        
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
 
        pygame.draw.rect(self.image, color, [0, 0, width, height], border_radius=0)
        
        self.rect = self.image.get_rect()

        # 創建mask，精確檢查碰撞
        self.mask = pygame.mask.from_surface(self.image)
        
    def moveUp(self, pixels):
        self.rect.y -= pixels
        if self.rect.y < 0:
            self.rect.y = 0
          
    def moveDown(self, pixels):
        self.rect.y += pixels
        if self.rect.y > config.SCREEN_HEIGHT - self.height:
            self.rect.y = config.SCREEN_HEIGHT - self.height
    def changehight(self, pixels):
        self.height = pixels
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.rect(self.image, self.color, [0, 0, self.width, self.height], border_radius=0)        
        self.rect = self.image.get_rect()
        # 創建mask，精確檢查碰撞
        self.mask = pygame.mask.from_surface(self.image)
