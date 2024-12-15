import pygame
import numpy as np
from paddle import Paddle
from ball_test_D import Ball
import config

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
        

        #字體
        self.font = pygame.font.Font(None, 74)

        #分數
        self.scoreA = 0
        self.scoreB = 0

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

        # 球拍碰撞檢測 (使用 mask)
        if pygame.sprite.collide_mask(self.paddleA, self.ball):
            self.ball.bounce()
            sound = pygame.mixer.Sound('path/to/your/soundfile.wav')
            # 设置音量和循环次数
            sound.set_volume(50)  # 设置音量为50%
            sound.play(1)  # 播放1次
            rewardB = 1
            self.ball.velocity[0] *= config.BALL_BOUNCE_FACTOR
            self.ball.rect.x += config.PADDLE_WIDTH
            self.ball.BOUNCE += 1
        if pygame.sprite.collide_mask(self.paddleB, self.ball):
            self.ball.bounce()
            sound = pygame.mixer.Sound('path/to/your/soundfile.wav')
            # 设置音量和循环次数
            sound.set_volume(50)  # 设置音量为50%
            sound.play(1)  # 播放1次
            rewardA = 1
            self.ball.velocity[0] *= config.BALL_BOUNCE_FACTOR
            self.ball.rect.x -= config.PADDLE_WIDTH
            self.ball.BOUNCE += 1

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
        # 填充背景
        self.screen.fill(config.BLACK)
        
        # 繪製中線
        pygame.draw.line(self.screen, config.WHITE, [self.screen_width // 2, 0], [self.screen_width // 2, self.screen_height], 5)
        
        # 繪製遊戲精靈
        self.all_sprites_list.draw(self.screen)
        
        # 繪製分數
        score_textA = self.font.render(str(self.scoreA), True, config.WHITE)
        score_textB = self.font.render(str(self.scoreB), True, config.WHITE)
        self.screen.blit(score_textA, (self.screen_width // 4 - score_textA.get_width() // 2, 20))
        self.screen.blit(score_textB, (self.screen_width * 3 // 4 - score_textB.get_width() // 2, 20))
        
        # 更新屏幕
        pygame.display.flip()

