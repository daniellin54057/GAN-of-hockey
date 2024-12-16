import pygame
import numpy as np
from paddle import Paddle
from ball_test_D import Ball
import config
from pygame.locals import *
import os
pygame.init()

class HockeyEnv:
    def __init__(self):
        self.rewardA = 0
        self.rewardB = 0 
        # 初始化 pygame
        pygame.init()

        # 環境參數
        self.screen_width = config.SCREEN_WIDTH
        self.screen_height = config.SCREEN_HEIGHT
        self.done = False

        # 初始化畫布
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Hockey Environment")

        # 初始化遊戲對象
        self.paddleA = Paddle(config.CYAN, config.PADDLE_WIDTH, config.PADDLE_HEIGHT_D)
        self.paddleA.rect.x = 20
        self.paddleA.rect.y = self.screen_height // 2 - config.PADDLE_HEIGHT_D // 2

        self.paddleB = Paddle(config.MAGENTA, config.PADDLE_WIDTH, config.PADDLE_HEIGHT_D)
        self.paddleB.rect.x = self.screen_width - 20 - config.PADDLE_WIDTH
        self.paddleB.rect.y = self.screen_height // 2 - config.PADDLE_HEIGHT_D // 2

        self.ball = Ball(config.WHITE, config.BALL_SIZE, config.BALL_SIZE)
        self.reset_ball()

        # 遊戲精靈
        self.all_sprites_list = pygame.sprite.Group()
        self.all_sprites_list.add(self.paddleA)
        self.all_sprites_list.add(self.paddleB)
        self.all_sprites_list.add(self.ball)

    def reset_ball(self):
        self.ball.rect.x = self.screen_width // 2 - config.BALL_SIZE // 2
        self.ball.rect.y = self.screen_height // 2 - config.BALL_SIZE // 2
        self.ball.velocity = [config.WAY * config.BALL_INITIAL_SPEED_D[0], 0]
        self.ball.BOUNCE = 0

    def reset(self, episode):
        self.rewardA = 0
        self.rewardB = 0
        self.ball.BOUNCE = 0
        # 重置遊戲狀態
        self.paddleA.rect.y = self.screen_height // 2 - self.paddleA.height//2
        self.paddleB.rect.y = self.screen_height // 2  - self.paddleB.height//2
        self.reset_ball()
        self.done = False
        self.paddleA.rect.x = 20
        self.paddleB.rect.x = self.screen_width - 20 - config.PADDLE_WIDTH
        if episode >= 100 and episode < config.PADDLE_DECREASE:    
            if config.PADDLE_HEIGHT_D - config.PADDLE_HEIGHT_D * episode /500 <= config.PADDLE_MIN:
                self.paddleA.changehight(config.PADDLE_MIN)
                self.paddleB.changehight(config.PADDLE_MIN)
            else:
                self.paddleA.changehight(config.PADDLE_HEIGHT_D - config.PADDLE_HEIGHT_D * episode / config.PADDLE_DECREASE)
                self.paddleB.changehight(config.PADDLE_HEIGHT_D - config.PADDLE_HEIGHT_D * episode / config.PADDLE_DECREASE)
            self.paddleA.rect.x = 20
            self.paddleB.rect.x = self.screen_width - 20 - config.PADDLE_WIDTH
        elif episode >= config.PADDLE_DECREASE:
            self.paddleA.changehight(config.PADDLE_MIN)
            self.paddleB.changehight(config.PADDLE_MIN)
            self.paddleA.rect.x = 20
            self.paddleB.rect.x = self.screen_width - 20 - config.PADDLE_WIDTH
        return self.get_state()

    def step(self, actionA, actionB):
        rewardA = 0
        rewardB = 0
        # 接收動作
        if actionA == 0:
            self.paddleA.moveUp(config.PADDLE_SPEED_D)
        elif actionA == 1:
            self.paddleA.moveDown(config.PADDLE_SPEED_D)

        if actionB == 0:
            self.paddleB.moveUp(config.PADDLE_SPEED_D)
        elif actionB == 1:
            self.paddleB.moveDown(config.PADDLE_SPEED_D)

        # 更新狀態
        self.all_sprites_list.update()

        # 邊界檢測
        if self.ball.rect.y < 0 or self.ball.rect.y > self.screen_height - config.BALL_SIZE:
            self.ball.velocity[1] = -self.ball.velocity[1]
        
        pygame.mixer.init()
        sound_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "boom.wav")
        self.collision_sound = pygame.mixer.Sound(sound_path)
        self.collision_sound.set_volume(100)

        # 球拍碰撞檢測 (使用 mask)
        if pygame.sprite.collide_mask(self.paddleA, self.ball):
            self.ball.bounce()
            rewardB = 1
            self.ball.velocity[0] *= config.BALL_BOUNCE_FACTOR
            self.ball.rect.x += config.PADDLE_WIDTH
            self.ball.BOUNCE += 1
            self.collision_sound.play()
        if pygame.sprite.collide_mask(self.paddleB, self.ball):
            self.ball.bounce()
            rewardA = 1
            self.ball.velocity[0] *= config.BALL_BOUNCE_FACTOR
            self.ball.rect.x -= config.PADDLE_WIDTH
            self.ball.BOUNCE += 1
            self.collision_sound.play()
        # 獎勳和結束條件
        if self.ball.rect.x < 0:
            rewardB = 1
            config.WAY *= -1
            self.done = True
        if self.ball.rect.x > self.screen_width:
            rewardA = 1
            config.WAY *= -1
            self.done = True

        # 更新球位置
        self.ball.rect.x += self.ball.velocity[0]
        self.ball.rect.y += self.ball.velocity[1]

        return self.get_state(), (rewardA, rewardB), self.done

    def get_state(self):
        # 返回狀態數據
        return np.array([
            self.paddleA.rect.y + self.paddleA.height//2,
            self.paddleB.rect.y + self.paddleB.height//2,
            self.ball.rect.x,
            self.ball.rect.y,
            self.ball.velocity[0],
            self.ball.velocity[1],
            self.ball.BOUNCE
        ], dtype=np.float32)
    

    def render(self):
        # 繪製畫面
        self.screen.fill(config.BLACK)
        pygame.draw.line(self.screen, config.WHITE, [self.screen_width // 2, 0], [self.screen_width // 2, self.screen_height], 5)
        self.all_sprites_list.draw(self.screen)
        pygame.display.flip()

