import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import random
import pickle
from collections import deque
import matplotlib.pyplot as plt
import pygame
import math
from hockey_env import HockeyEnv
import config
from train2 import HockeyAI

# 初始化 pygame
pygame.init()
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
pygame.display.set_caption("Hockey Training Visualization")
clock = pygame.time.Clock()


def normalize_state(state):
    """正規化狀態"""
    return state / np.linalg.norm(state)


def render_game():
    screen.fill((0, 0, 0))  # 清空螢幕為黑色
    env.render()  # 假設 HockeyEnv 中有 render 方法繪製畫面
    pygame.display.flip()

# 初始化模型
state_size = 7  # 根據環境的狀態維度設置
action_size = 3  # 根據行為空間維度設置
model1 = HockeyAI(state_size, action_size)
model2 = HockeyAI(state_size, action_size)

# 載入儲存的參數
model1_path = "model1_final_difficult.pth"
model2_path = "model2_final_difficult.pth"
model1.load_state_dict(torch.load(model1_path))
model2.load_state_dict(torch.load(model2_path))
model1.eval()  # 切換到推理模式
model2.eval()

env = HockeyEnv()
state1 , state2 = env.reset(1), env.reset(1)  # 重置環境並獲取初始狀態
state1, state2 = normalize_state(state1), normalize_state(state2)


episodes = config.EPISODES

for episode in range(500,episodes):
        total_total = []
        x = []
        bounce_per_episode = []
        state1, state2 = env.reset(episode), env.reset(episode)
        state1, state2 = normalize_state(state1), normalize_state(state2)
        total_reward1, total_reward2 = 0, 0


        while not env.done:
            # 模型1的行動
            action1 = model1(torch.tensor(state1, dtype=torch.float32)).argmax().item()

            # 模型2的行動
            action2 = model2(torch.tensor(state2, dtype=torch.float32)).argmax().item()

            next_state1, (reward1, reward2), done = env.step(action1, action2)
            next_state1, next_state2 = normalize_state(next_state1), normalize_state(next_state1)


            # 更新狀態與總分
            state1, state2 = next_state1, next_state2
            total_reward1 += reward1
            total_reward2 += reward2


            # 可視化更新
            render_game()
            clock.tick(30)  # 控制更新速度

            if done:
                break
 
        if episode == 0:
            pass
        else:
            t = total_reward1 + total_reward2
            total_total.append(t)
            x.append(math.log(episode))
            bounce_per_episode.append(env.ball.BOUNCE)

        print(f"Episode {episode }: Player A Reward: {total_reward1}, Player B Reward: {total_reward2}, BOUNCE: {env.ball.BOUNCE}")


        print(f"Episode {episode + 1}: Player A Reward: {total_reward1}, Player B Reward: {total_reward2}, BOUNCE: {env.ball.BOUNCE}")

        print(f"Episode {episode + 1}: Player A Reward: {total_reward1}, Player B Reward: {total_reward2}")
        if len(total_total) != 0 and total_total[len(total_total)-1] > 250:
            break
        # 儲存模型與數據

