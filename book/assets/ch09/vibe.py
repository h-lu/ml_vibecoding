import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.datasets import make_moons
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# 1. 生成并准备数据
X, y = make_moons(n_samples=200, noise=0.4, random_state=42)
X = torch.FloatTensor(X)
y = torch.FloatTensor(y.reshape(-1, 1))

# 2. 定义网络架构
class MoonClassifier(nn.Module):
    def __init__(self):
        super(MoonClassifier, self).__init__()
        self.fc1 = nn.Linear(2, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc22 = nn.Linear(64, 64)
        self.fc23 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, 1)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.3)
        self.sigmoid = nn.Sigmoid()
    
    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.relu(self.fc2(x))
        x = self.dropout(x)
        x = self.relu(self.fc22(x))
        x = self.dropout(x)
        x = self.relu(self.fc23(x))
        x = self.dropout(x)
        x = self.sigmoid(self.fc3(x))
        return x

model = MoonClassifier()

# 3. 定义损失与优化器
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

# 4. 训练循环和可视化
def plot_decision_boundary(model, X, y, epoch):
    # 创建网格点
    h = 0.02  # 步长
    x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
    y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
    
    # 预测每个网格点的类别
    with torch.no_grad():
        Z = model(torch.FloatTensor(np.c_[xx.ravel(), yy.ravel()]))
        Z = Z.numpy().reshape(xx.shape)
    
    # 绘制决策边界和数据点
    plt.figure(figsize=(10, 6))
    plt.contourf(xx, yy, Z, cmap=plt.cm.RdBu, alpha=0.8)
    plt.scatter(X[:, 0], X[:, 1], c=y.numpy().ravel(), cmap=ListedColormap(['#FF0000', '#0000FF']), edgecolors='k')
    plt.title(f'Epoch {epoch}')
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.pause(0.1)
    plt.close()

# 训练过程
plt.ion()  # 开启交互模式
for epoch in range(1001):
    # 前向传播
    outputs = model(X)
    loss = criterion(outputs, y)
    
    # 反向传播和优化
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    # 每100次迭代可视化一次
    if epoch % 100 == 0:
        print(f'Epoch [{epoch}/1000], Loss: {loss.item():.4f}')
        plot_decision_boundary(model, X, y, epoch)

plt.ioff()  # 关闭交互模式
plt.show()