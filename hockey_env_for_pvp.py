import pygame
from paddle import Paddle
from ball_test import Ball
import config

class playhockey:
    def __init__(self):
        pygame.init()

        self.screen_width = config.SCREEN_WIDTH
        self.screen_height = config.SCREEN_HEIGHT
        self.gg = False

        #canvas

        self.screen = pygame.display.set_mode((self.screen_width , self.screen_height))
        pygame.display.set_caption('hockey env')

        #items
        self.paddleA = Paddle(config.CYAN , config.PADDLE_WIDTH , config.PADDLE_HEIGHT)
        self.paddleA.rect.x = 20 + config.PADDLE_WIDTH // 2
        self.paddleA.rect.y = self.screen_height // 2 - config.PADDLE_HEIGHT // 2
        
        self.paddleB = Paddle(config.CYAN , config.PADDLE_WIDTH , config.PADDLE_HEIGHT)
        self.paddleB.rect.x = self.screen_width - 20 - config.PADDLE_WIDTH//2 
        self.paddleB.rect.y = self.screen_height // 2 - config.PADDLE_HEIGHT // 2

        self.ball = Ball(config.WHITE , config.BALL_SIZE, config.BALL_SIZE)
        self.reset_ball()

        self.all_sprites_list = pygame.sprite.Group()
        self.all_sprites_list.add(self.paddleA)
        self.all_sprites_list.add(self.paddleB)
        self.all_sprites_list.add(self.ball)
    
    def reset_ball(self):
        self.ball.rect.x = self.screen_width // 2 - config.BALL_SIZE // 2
        self.ball.rect.y = self.screen_height // 2 - config.BALL_SIZE // 2
        self.ball.velocity = [config.WAY * 5, 0]

    def reset(self):
        self.paddleA.rect.y = self.screen_height // 2 - config.PADDLE_HEIGHT // 2
        self.paddleB.rect.y = self.screen_height // 2 - config.PADDLE_HEIGHT // 2
        self.reset_ball()
        self.gg = False
        
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.paddleA.moveUp(config.PADDLE_SPEED)
        if keys[pygame.K_s]:
            self.paddleA.moveDown(config.PADDLE_SPEED)
        
        if keys[pygame.K_UP]:
            self.paddleB.moveUp(config.PADDLE_SPEED)
        if keys[pygame.K_DOWN]:
            self.paddleB.moveDown(config.PADDLE_SPEED)
    
        self.all_sprites_list.update()

        if self.ball.rect.y <= 0 or self.ball.rect.y >= self.screen_height - config.BALL_SIZE:
            self.ball.velocity[1] = -self.ball.velocity[1]
        
        if pygame.sprite.collide_mask(self.paddleA, self.ball):
            self.ball.bounce()
            self.ball.velocity[0] *= config.BALL_BOUNCE_FACTOR
            self.ball.rect.x += config.PADDLE_WIDTH
        if pygame.sprite.collide_mask(self.paddleB, self.ball):
            self.ball.bounce()
            self.ball.velocity[0] *= config.BALL_BOUNCE_FACTOR
            self.ball.rect.x -= config.PADDLE_WIDTH
        
        if self.ball.rect.x < 0 or self.ball.rect.x > self.screen_width: 
            config.WAY *= -1
            self.gg = True
    def render(self):
        self.screen.fill(config.BLACK)
        pygame.draw.line(self.screen, config.WHITE, [self.screen_width // 2, 0], [self.screen_width // 2, self.screen_height], 5)
        self.all_sprites_list.draw(self.screen)
        pygame.display.flip()