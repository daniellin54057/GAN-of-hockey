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

def save_model(model_data, file_path="model.pkl"):
    """
    儲存模型到指定路徑
    """
    with open(file_path, "wb") as file:
        pickle.dump(model_data, file)
    print(f"模型已儲存至 {file_path}")
class HockeyAI(nn.Module):
    def __init__(self, input_size, output_size):
        super(HockeyAI, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_size, 256),  # 增加隱藏層單元數
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Linear(256, output_size)
        )

    def forward(self, x):
        return self.net(x)


class ReplayBuffer:
    def __init__(self, capacity=10000):
        self.buffer = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        return np.array(states), np.array(actions), np.array(rewards), np.array(next_states), np.array(dones)

    def __len__(self):
        return len(self.buffer)


def train():
    # 初始化環境與參數
    env = HockeyEnv()
    state_size = env.get_state().shape[0]
    action_size = config.ACTION_SPACE

    model1 = HockeyAI(state_size, action_size)
    model2 = HockeyAI(state_size, action_size)

    optimizer1 = optim.Adam(model1.parameters(), lr=0.001)
    optimizer2 = optim.Adam(model2.parameters(), lr=0.001)
    scheduler1 = optim.lr_scheduler.StepLR(optimizer1, step_size=100, gamma=0.9)
    scheduler2 = optim.lr_scheduler.StepLR(optimizer2, step_size=100, gamma=0.9)

    criterion = nn.MSELoss()
    buffer1 = ReplayBuffer()
    buffer2 = ReplayBuffer()
    scores1, scores2, bounce_per_episode = [], [], []
    episodes = config.EPISODES
    batch_size = 64
    # 初始化 pygame
    pygame.init()
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption("Hockey Training Visualization")
    clock = pygame.time.Clock()

    def render_game():
        screen.fill((0, 0, 0))  # 清空螢幕為黑色
        env.render()  # 假設 HockeyEnv 中有 render 方法繪製畫面
        pygame.display.flip()
    x = []
    total_total = []
    for episode in range(episodes):
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

            # 儲存到 Replay Buffer
            buffer1.push(state1, action1, reward1, next_state1, done)
            buffer2.push(state2, action2, reward2, next_state2, done)

            # 更新狀態與總分
            state1, state2 = next_state1, next_state2
            total_reward1 += reward1
            total_reward2 += reward2

            # Replay Buffer 訓練
            if len(buffer1) > batch_size:
                train_from_buffer(model1, optimizer1, criterion, buffer1, batch_size)
            if len(buffer2) > batch_size:
                train_from_buffer(model2, optimizer2, criterion, buffer2, batch_size)
            # 可視化更新
            render_game()
            clock.tick(30)  # 控制更新速度

            if done:
                break
        # 記錄分數與碰撞次數

        scores1.append(total_reward1)
        scores2.append(total_reward2)
 
        if episode == 0:
            pass
        else:
            t = total_reward1 + total_reward2
            total_total.append(t)
            x.append(math.log(episode))
            bounce_per_episode.append(env.ball.BOUNCE)

        print(f"Episode {episode }: Player A Reward: {total_reward1}, Player B Reward: {total_reward2}, BOUNCE: {env.ball.BOUNCE}")

        # 動態繪圖
        plt.clf()
        plt.xlim(0, math.log(config.EPISODES))
        #plt.plot(x, bounce_per_episode, label="Bounces per Episode(log)", color="blue", marker=".")
        plt.plot(x, total_total, label="total reward", color="red", marker="")
        plt.xlabel("Episode")
        plt.ylabel("Total Count")
        plt.title("Reward to Episode(log)")
        plt.grid(True)
        plt.legend()
        plt.pause(0.01)

        print(f"Episode {episode + 1}: Player A Reward: {total_reward1}, Player B Reward: {total_reward2}, BOUNCE: {env.ball.BOUNCE}")


        # 減少探索率
        scheduler1.step()
        scheduler2.step()

        print(f"Episode {episode + 1}: Player A Reward: {total_reward1}, Player B Reward: {total_reward2}")
        if len(total_total) != 0 and total_total[len(total_total)-1] > 100:
            break
        # 儲存模型與數據

    save_model(bounce_per_episode, "bounce_model.pkl")
    torch.save(model1.state_dict(), f"model1_final{config.EPISODES}.pth")
    torch.save(model2.state_dict(), f"model2_final{config.EPISODES}.pth")

    # 繪製最終圖表
    plt.figure(figsize=(10, 6))
    plt.plot(x, total_total, label="total reward", color="red", marker="")
    plt.xlabel("Episode")
    plt.ylabel("Total Reward")
    plt.title("Reward to Episode")
    plt.grid(True)
    plt.legend()
    plt.savefig("reward to ep (log).png")
    plt.show()
    print("訓練完成，圖表與模型已儲存。")
    pygame.quit()
    print("訓練完成！")


def normalize_state(state):
    """正規化狀態"""
    return state / np.linalg.norm(state)


def train_from_buffer(model, optimizer, criterion, buffer, batch_size):
    """從 Replay Buffer 中訓練"""
    states, actions, rewards, next_states, dones = buffer.sample(batch_size)

    states = torch.tensor(states, dtype=torch.float32)
    actions = torch.tensor(actions, dtype=torch.int64)
    rewards = torch.tensor(rewards, dtype=torch.float32)
    next_states = torch.tensor(next_states, dtype=torch.float32)
    dones = torch.tensor(dones, dtype=torch.float32)

    q_values = model(states)
    next_q_values = model(next_states).detach().max(dim=1)[0]
    target_q_values = rewards + (1 - dones) * 0.99 * next_q_values

    current_q_values = q_values.gather(1, actions.unsqueeze(1)).squeeze()

    loss = criterion(current_q_values, target_q_values)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()


if __name__ == "__main__":
    train()
