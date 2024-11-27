import pygame
import random

class Ball(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()

        # 創建球的表面
        self.image = pygame.Surface([width, height], pygame.SRCALPHA)  # 使用透明背景
        self.image.fill((0, 0, 0, 0))  # 設置透明
        pygame.draw.ellipse(self.image, color, [0, 0, width, height])  # 繪製球
        self.rect = self.image.get_rect()

        # 創建mask，精確檢查碰撞
        self.mask = pygame.mask.from_surface(self.image)

        # 球的速度
        self.velocity = [5, 0]

    def update(self):
        # 更新球的位置
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def bounce(self):
        """
        當球與球拍碰撞時改變速度方向。
        """
        self.velocity[0] = -self.velocity[0]  # 反轉水平速度
        self.velocity[1] += random.randint(-3, 3)  # 給垂直速度增加隨機偏移量
        if abs(self.velocity[1]) > 8:  # 防止速度過快
            self.velocity[1] = 8 if self.velocity[1] > 0 else -8