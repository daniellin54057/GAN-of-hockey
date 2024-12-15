import pygame
import random
import config

class Ball(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()

        # 創建球的表面
        self.image = pygame.Surface([width, height], pygame.SRCALPHA)  # 使用透明背景
        self.image.fill((0, 0, 0, 0))  # 設置透明
        pygame.draw.ellipse(self.image, color, [0, 0, width, height])  # 繪製球
        self.rect = self.image.get_rect()
        self.BOUNCE = 0

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
         # 增加反彈次數並更新顏色
        self.BOUNCE += 1
        self.update_color()

    def update_color(self):
        """
        根據反彈次數調整球的顏色。
        """
        mode = (self.BOUNCE // 3) % 6
        if mode == 0 : color = config.RED
        elif mode == 1 : color = config.ORANGE
        elif mode == 2 : color = config.YELLOW
        elif mode == 3 : color = config.GREEN
        elif mode == 4 : color = config.BLUE
        elif mode == 5 : color = config.PURPLE
        self.color = color
        self.image.fill((0, 0, 0, 0))  # 清除舊顏色
        pygame.draw.ellipse(self.image, self.color, [0, 0, self.rect.width, self.rect.height])

    def reset_color(self):
        """
        在失分後重置顏色和反彈次數。
        """
        self.BOUNCE = 0
        self.color = (255, 255, 255)  # 重置為白色
        self.image.fill((0, 0, 0, 0))  # 清除舊顏色
        pygame.draw.ellipse(self.image, self.color, [0, 0, self.rect.width, self.rect.height])
