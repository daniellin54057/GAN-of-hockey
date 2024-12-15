import pygame
import torch
import numpy as np
from train2 import HockeyAI  # 假設已定義的 AI 模型結構
from hockeyEnvForPAI_D import HockeyEnv
import config
from paddle import Paddle
from ball_test_D import Ball




def normalize_state(state):
    """
    將狀態數據正規化為 [0, 1] 範圍。
    """
    norm = np.linalg.norm(state)
    return state / norm if norm != 0 else state

def player_vs_ai():
    # 初始化遊戲環境
    pygame.init()
    env = HockeyEnv()
    clock = pygame.time.Clock()

    # 加載 AI 模型
    model_path = r"model2_final_difficult.pth"
    state_size = 7  # 確保與 get_state 返回的狀態數量一致
    action_size = 3
    ai_model = HockeyAI(state_size, action_size)
    ai_model.load_state_dict(torch.load(model_path))
    ai_model.eval()  # 設置為評估模式

    # 遊戲變量
    running = True
    player_score = 0
    ai_score = 0
    max_score = config.MAXSCORE  # 比賽結束條件

    # 遊戲主循環
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

 

        # 獲取環境狀態
        state = env.get_state()
        normalized_state = normalize_state(state)

        # AI 行為
        ai_action = ai_model(torch.tensor(normalized_state, dtype=torch.float32)).argmax().item()

        # 玩家輸入
        keys = pygame.key.get_pressed()
        action1 = 2  # 預設為不動
        if keys[pygame.K_w]:
            action1 = 0  # 向上移動
        elif keys[pygame.K_s]:
            action1 = 1  # 向下移動

        # 更新環境
        _, rewards, done = env.step(action1, ai_action)

        # 更新分數
        if done:
            if rewards[0] > rewards[1]:
                player_score += 1
            else:
                ai_score += 1
            env.reset(episode=player_score + ai_score)  # 重置環境
        env.scoreA = player_score
        env.scoreB = ai_score
        # 檢查結束條件
        if player_score >= max_score or ai_score >= max_score:
            print(f"遊戲結束！玩家: {player_score}, AI: {ai_score}")
            running = False
        
        

        # 繪製畫面
        env.render()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    player_vs_ai()    

