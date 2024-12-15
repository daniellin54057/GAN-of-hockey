檔名意思：pds:paddlespeed  bs:ballspeed  t:train episode
----------

開啟＆輸入模型：

from hockey_env import HockeyEnv  # 確保 `HockeyEnv` 已經正確引入

# 初始化模型
state_size = 7  # 根據環境的狀態維度設置
action_size = 3  # 根據行為空間維度設置
model = HockeyAI(state_size, action_size)

# 載入儲存的參數
model_path = "model1_final.pth"
model.load_state_dict(torch.load(model_path))
model.eval()  # 切換到推理模式

-----------

與環境交互：
env = HockeyEnv()
state = env.reset()  # 重置環境並獲取初始狀態
state = normalize_state(state)  # 正規化狀態

# 將狀態轉為 Tensor 並推斷動作
state_tensor = torch.tensor(state, dtype=torch.float32)
action = model(state_tensor).argmax().item()  # 選擇機率最大的行動

# 執行該行動並查看結果
next_state, reward, done = env.step(action)

------------

繼續訓練：

model.train()  # 切換回訓練模式
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
criterion = nn.MSELoss()
------------
範例：

for episode in range(100):  # 假設繼續訓練 100 回合
    state = env.reset()
    state = normalize_state(state)
    total_loss = 0
    while not env.done:
        state_tensor = torch.tensor(state, dtype=torch.float32)
        action = model(state_tensor).argmax().item()
        next_state, reward, done = env.step(action)
        next_state = normalize_state(next_state)

        # 構建目標值
        next_state_tensor = torch.tensor(next_state, dtype=torch.float32)
        q_next = model(next_state_tensor).detach().max().item()
        target = reward + (0.99 * q_next * (1 - done))  # TD 目標值

        # 計算損失
        q_value = model(state_tensor)[action]
        loss = criterion(q_value, torch.tensor(target, dtype=torch.float32))

        # 更新模型
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        state = next_state
        total_loss += loss.item()
