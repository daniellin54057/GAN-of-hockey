import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import pygame
import pickle
from hockey_env import HockeyEnv
import config


# 定義簡單的神經網路
class HockeyAI(nn.Module):
    def __init__(self, input_size, output_size):
        super(HockeyAI, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_size, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, output_size)
        )

    def forward(self, x):
        return self.net(x)


def save_model(model_data, file_path="model.pkl"):
    """
    儲存模型到指定路徑
    """
    with open(file_path, "wb") as file:
        pickle.dump(model_data, file)
    print(f"模型已儲存至 {file_path}")


def train():
    # 初始化環境
    env = HockeyEnv()
    state_size = env.get_state().shape[0]  # 假設 get_state 回傳狀態空間大小
    action_size = config.ACTION_SPACE  # 假設 config.ACTION_SPACE 定義動作空間

    # 初始化模型
    model1 = HockeyAI(state_size, action_size)
    model2 = HockeyAI(state_size, action_size)

    optimizer1 = optim.Adam(model1.parameters(), lr=0.001)
    optimizer2 = optim.Adam(model2.parameters(), lr=0.001)
    criterion = nn.MSELoss()

    episodes = config.EPISODES
    scores1, scores2, bounce_per_episode = [], [], []

    # 初始化 pygame
    pygame.init()
    screen = pygame.display.set_mode((700, 600))
    pygame.display.set_caption("Hockey Training Visualization")
    clock = pygame.time.Clock()

    def render_game():
        screen.fill((0, 0, 0))  # 清空螢幕為黑色
        env.render()  # 假設 HockeyEnv 中有 render 方法繪製畫面
        pygame.display.flip()

    for episode in range(episodes):
        state1, state2 = env.reset(), env.reset()
        config.BOUNCE = 0
        total_reward1, total_reward2 = 0, 0

        while not env.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            # 模型1的行動
            state1 , state2 = env.get_state(), env.get_state()
            state_tensor1 = torch.tensor(state1, dtype=torch.float32)
            action1 = model1(state_tensor1).detach().argmax().item()
 
            # 模型2的行動
            state_tensor2 = torch.tensor(state2, dtype=torch.float32)
            action2 = model2(state_tensor2).detach().argmax().item()

            # 執行環境中的一步
            next_state1, (reward1, reward2), done = env.step(action1, action2)

            # 儲存經驗並訓練模型1
            target1 = reward1 + 0.99 * model1(torch.tensor(next_state1, dtype=torch.float32)).max().detach()
            loss1 = criterion(model1(state_tensor1), target1)
            optimizer1.zero_grad()
            loss1.backward()
            optimizer1.step()

            # 儲存經驗並訓練模型2
            target2 = reward2 + 0.99* model2(torch.tensor(next_state1, dtype=torch.float32)).max().detach()
            loss2 = criterion(model2(state_tensor2), target2)
            optimizer2.zero_grad()
            loss2.backward()
            optimizer2.step()

            # 累積分數
            total_reward1 += reward1
            total_reward2 += reward2


            # 可視化更新
            render_game()
            clock.tick(30)  # 控制更新速度

            if done:
                break

        # 記錄分數與碰撞次數
        scores1.append(total_reward1)
        scores2.append(total_reward2)
        bounce_per_episode.append(config.BOUNCE)

        print(f"Episode {episode + 1}: Player A Reward: {total_reward1}, Player B Reward: {total_reward2}, BOUNCE: {config.BOUNCE}")

        # 動態繪圖
        plt.clf()
        plt.plot(range(len(bounce_per_episode)), bounce_per_episode, label="Bounces per Episode", color="blue", marker="o")
        plt.xlabel("Episode")
        plt.ylabel("BOUNCE Count")
        plt.title("BOUNCE Count per Episode")
        plt.grid(True)
        plt.legend()
        plt.pause(0.01)
        


    # 儲存模型與數據
    save_model(bounce_per_episode, "bounce_model.pkl")
    torch.save(model1.state_dict(), "model1_final.pth")
    torch.save(model2.state_dict(), "model2_final.pth")

    # 繪製最終圖表
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(bounce_per_episode)), bounce_per_episode, label="Bounces per Episode", color="blue", marker="o")
    plt.xlabel("Episode")
    plt.ylabel("BOUNCE Count")
    plt.title("BOUNCE Count per Episode")
    plt.grid(True)
    plt.legend()
    plt.savefig("bounce_plot.png")
    plt.show()
    print("訓練完成，圖表與模型已儲存。")
    pygame.quit()


if __name__ == "__main__":
    train()