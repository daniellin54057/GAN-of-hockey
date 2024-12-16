import pygame
from paddle import Paddle
from ball_test import Ball
import config
import random

class playhockey2:
    def __init__(self):
        pygame.init()

        self.screen_width = config.SCREEN_WIDTH
        self.screen_height = config.SCREEN_HEIGHT
        self.gg = False
        self.leftcol = False
        self.rightcol = False
        self.regard = {
            'q' : pygame.K_q ,
            'w' : pygame.K_w , 
            'e' : pygame.K_e , 
            'a' : pygame.K_a , 
            's' : pygame.K_s , 
            'd' : pygame.K_d , 
            'u' : pygame.K_u , 
            'i' : pygame.K_i , 
            'o' : pygame.K_o , 
            'j' : pygame.K_j , 
            'k' : pygame.K_k ,
            'l' : pygame.K_l}

        #canvas

        self.screen = pygame.display.set_mode((self.screen_width , self.screen_height))
        pygame.display.set_caption('hockey env')

        #items
        self.paddleA = Paddle(config.CYAN , config.PADDLE_WIDTH , config.PADDLE_HEIGHT_FOR_PLAY2)
        self.paddleA.rect.x = 20 + config.PADDLE_WIDTH // 2
        self.paddleA.rect.y = self.screen_height // 2 - config.PADDLE_HEIGHT_FOR_PLAY2// 2
        
        self.paddleB = Paddle(config.MAGENTA , config.PADDLE_WIDTH , config.PADDLE_HEIGHT_FOR_PLAY2)
        self.paddleB.rect.x = self.screen_width - 20 - config.PADDLE_WIDTH//2 
        self.paddleB.rect.y = self.screen_height // 2 - config.PADDLE_HEIGHT_FOR_PLAY2 // 2

        self.ball = Ball(config.WHITE , config.BALL_SIZE, config.BALL_SIZE)
        self.reset_ball()

        self.all_sprites_list = pygame.sprite.Group()
        self.all_sprites_list.add(self.paddleA)
        self.all_sprites_list.add(self.paddleB)
        self.all_sprites_list.add(self.ball)

        self.scoreA = 0
        self.scoreB = 0

        self.font = pygame.font.Font(None, 74)
    
    def reset_letters_p1(self):

        global p1_list
        p1_list = ['q' , 'w' , 'e' , 'a' , 's' , 'd']
        
        random.shuffle(p1_list)


         
    
    def reset_letters_p2(self):
        global p2_list

        p2_list = ['u' , 'i' , 'o' , 'j' , 'k' , 'l']

        random.shuffle(p2_list)


        for i in range(6):
            font = pygame.font.Font(None , 74)
            text_color = (255 , 255 , 255)
            text_surface = font.render(f'{p1_list[i]}' , True , text_color)
            self.screen.blit(text_surface , (680 , 100 * i+50))

    def reset_ball(self):
        self.ball.rect.x = self.screen_width // 2 - config.BALL_SIZE // 2
        self.ball.rect.y = self.screen_height // 2 - config.BALL_SIZE // 2
        self.ball.velocity = [config.WAY * 5, 0]

    def reset(self):
        self.paddleA.rect.y = self.screen_height // 2 - config.PADDLE_HEIGHT_FOR_PLAY2 // 2
        self.paddleB.rect.y = self.screen_height // 2 - config.PADDLE_HEIGHT_FOR_PLAY2 // 2
        self.reset_ball()
        self.gg = False
        
    def move(self):
        
        keys = pygame.key.get_pressed()
        for i in range(6):
            if keys[self.regard[p1_list[i]]]:
                self.paddleA.rect.y = 100*i
    
        for i in range(6):
            if keys[self.regard[p2_list[i]]]:
                self.paddleB.rect.y = 100*i
    
        self.all_sprites_list.update()

        if self.ball.rect.y <= 0 or self.ball.rect.y >= self.screen_height - config.BALL_SIZE:
            self.ball.velocity[1] = -self.ball.velocity[1]
        
        if pygame.sprite.collide_mask(self.paddleA, self.ball):
            self.ball.bounce()
            self.ball.velocity[0] *= (config.BALL_BOUNCE_FACTOR + 0.01)
            self.ball.rect.x += config.PADDLE_WIDTH
            self.reset_letters_p1()

        if pygame.sprite.collide_mask(self.paddleB, self.ball):
            self.ball.bounce()
            self.ball.velocity[0] *= (config.BALL_BOUNCE_FACTOR + 0.01)
            self.ball.rect.x -= config.PADDLE_WIDTH
            self.reset_letters_p2()
        
        if self.ball.rect.x < 0 or self.ball.rect.x > self.screen_width: 
            if self.ball.rect.x < 0:
                self.scoreB += 1
            elif self.ball.rect.x > self.screen_width:
                self.scoreA += 1
            config.WAY *= -1
            self.gg = True
    def render(self):
        self.screen.fill(config.BLACK)
        pygame.draw.line(self.screen, config.WHITE, [self.screen_width // 2, 0], [self.screen_width // 2, self.screen_height], 5)
        self.all_sprites_list.draw(self.screen)
        pygame.display.flip()
        score_textA = self.font.render(str(self.scoreA), True, config.WHITE)
        score_textB = self.font.render(str(self.scoreB), True, config.WHITE)
        
        for i in range(6):
            font = pygame.font.Font(None , 74)
            text_color = (255 , 255 , 255)
            text_surface = font.render(f'{p1_list[i]}' , True , text_color)
            self.screen.blit(text_surface , (20 , 100 * i+25)) 

        for i in range(6):
            font = pygame.font.Font(None , 74)
            text_color = (255 , 255 , 255)
            text_surface = font.render(f'{p2_list[i]}' , True , text_color)
            self.screen.blit(text_surface , (650 , 100 * i+25))

        self.screen.blit(score_textA, (self.screen_width // 4, 20))
        self.screen.blit(score_textB, (self.screen_width * 3 // 4, 20))
