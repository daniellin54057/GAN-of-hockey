import pygame
import torch
import numpy as np
from paddle import Paddle
from ball_test import Ball
import config
from train2 import HockeyAI  # 假設訓練代碼中定義了模型結構

class playhockey:
    def __init__(self):
        pygame.init()

        self.screen_width = config.SCREEN_WIDTH
        self.screen_height = config.SCREEN_HEIGHT
        self.gg = False

        # canvas
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Hockey Environment')

        # items
        self.paddleA = Paddle(config.CYAN, config.PADDLE_WIDTH, config.PADDLE_HEIGHT)
        self.paddleA.rect.x = 20 + config.PADDLE_WIDTH // 2
        self.paddleA.rect.y = self.screen_height // 2 - config.PADDLE_HEIGHT // 2

        self.paddleB = Paddle(config.CYAN, config.PADDLE_WIDTH, config.PADDLE_HEIGHT)
        self.paddleB.rect.x = self.screen_width - 20 - config.PADDLE_WIDTH // 2
        self.paddleB.rect.y = self.screen_height // 2 - config.PADDLE_HEIGHT // 2

        self.ball = Ball(config.WHITE, config.BALL_SIZE, config.BALL_SIZE)
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

    def render(self):
        self.screen.fill(config.BLACK)
        pygame.draw.line(self.screen, config.WHITE, [self.screen_width // 2, 0], [self.screen_width // 2, self.screen_height], 5)
        self.all_sprites_list.draw(self.screen)
        pygame.display.flip()

    def get_state(self):
        """
        返回遊戲的完整狀態：
        - 球拍位置
        - 球的位置和速度
        - 遊戲方向
        """
        return np.array([
            self.paddleA.rect.y,
            self.paddleB.rect.y,
            self.ball.rect.x,
            self.ball.rect.y,
            self.ball.velocity[0],
            self.ball.velocity[1],
            self.ball.BOUNCE
        ], dtype=np.float32)

def normalize_state(state):
    """
    將狀態數據正規化為 [0, 1] 範圍
    """
    norm = np.linalg.norm(state)
    return state / norm if norm != 0 else state

def player_vs_ai():
    pygame.init()
    game = playhockey()
    clock = pygame.time.Clock()

    # 加載 AI 模型
    model_path = r"/home/project/model2_final_difficult.pth"
    state_size = 7  # 確保與 get_state 返回的狀態數量一致
    action_size = 3
    ai_model = HockeyAI(state_size, action_size)
    ai_model.load_state_dict(torch.load(model_path))
    ai_model.eval()  # 設置為評估模式

    running = True
    player_score = 0
    ai_score = 0
    max_score = 10  # 結束條件

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 玩家控制左側球拍
        game.move()

        # AI 決策
        state = game.get_state()  # 獲取遊戲狀態
        normalized_state = normalize_state(state)  # 正規化狀態
        ai_action = ai_model(torch.tensor(normalized_state, dtype=torch.float32)).argmax().item()

        # 應用 AI 動作到右側球拍
        if ai_action == 0:  # 向上移動
            game.paddleB.moveUp(config.PADDLE_SPEED)
        elif ai_action == 1:  # 向下移動
            game.paddleB.moveDown(config.PADDLE_SPEED)

        # 更新遊戲環境
        game.all_sprites_list.update()

        # 確認是否得分
        if game.ball.rect.x < 0:  # AI 得分
            ai_score += 1
            game.reset()
        elif game.ball.rect.x > game.screen_width:  # 玩家得分
            player_score += 1
            game.reset()

        # 檢查遊戲結束條件
        if player_score >= max_score or ai_score >= max_score:
            print(f"遊戲結束！玩家: {player_score}, AI: {ai_score}")
            running = False

        # 渲染遊戲
        game.render()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    player_vs_ai()
