"""
阶段3：深度学习基础（PyTorch）
==============================
学习内容:
  1. PyTorch 张量操作
  2. 自动求导 Autograd
  3. 线性回归（全连接网络）
  4. 多层感知机 MLP
  5. CNN 卷积神经网络
  6. 训练流程：数据→模型→损失→优化
"""

# ============ 3.1 张量操作 ============
print("=== 3.1 张量操作 ===")
import torch

# 创建张量
x = torch.tensor([[1, 2], [3, 4]], dtype=torch.float32)
y = torch.ones(2, 2)
print(f"x:\n{x}")
print(f"x + y:\n{x + y}")
print(f"x * y:\n{x * y}")
print(f"矩阵乘法 x @ y:\n{x @ y}")
print(f"x.shape: {x.shape}, x.device: {x.device}")

# GPU检查
print(f"CUDA可用: {torch.cuda.is_available()}")

# ============ 3.2 自动求导 ============
print("\n=== 3.2 自动求导 Autograd ===")

x = torch.tensor([2.0], requires_grad=True)
y = x ** 3 + 2 * x ** 2 + 3 * x + 1  # y = x³ + 2x² + 3x + 1
y.backward()
print(f"x=2时 dy/dx = {x.grad.item()}")  # 3x²+4x+3 = 12+8+3=23

# ============ 3.3 线性回归 ============
print("\n=== 3.3 线性回归 ===")

# 生成数据: y = 2x + 1 + noise
torch.manual_seed(42)
X = torch.rand(100, 1) * 10
y_true = 2 * X + 1 + torch.randn(100, 1) * 0.5

# 模型
model = torch.nn.Linear(1, 1)
loss_fn = torch.nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

# 训练
for epoch in range(500):
    pred = model(X)
    loss = loss_fn(pred, y_true)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

w, b = model.weight.item(), model.bias.item()
print(f"训练结果: y = {w:.4f}x + {b:.4f} (期望: y=2x+1)")
print(f"最终Loss: {loss.item():.6f}")

# ============ 3.4 多层感知机 MLP ============
print("\n=== 3.4 多层感知机 MLP ===")

class MLP(torch.nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super().__init__()
        self.net = torch.nn.Sequential(
            torch.nn.Linear(input_dim, hidden_dim),
            torch.nn.ReLU(),
            torch.nn.Linear(hidden_dim, hidden_dim),
            torch.nn.ReLU(),
            torch.nn.Linear(hidden_dim, output_dim),
        )

    def forward(self, x):
        return self.net(x)

model = MLP(10, 64, 1)
dummy = torch.randn(32, 10)  # batch=32, input=10
output = model(dummy)
print(f"MLP 输入 (32,10) → 输出 {output.shape}")
print(f"参数量: {sum(p.numel() for p in model.parameters())}")

# ============ 3.5 CNN 卷积网络 ============
print("\n=== 3.5 CNN 卷积网络 ===")

class SimpleCNN(torch.nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()
        self.conv = torch.nn.Sequential(
            torch.nn.Conv2d(1, 32, kernel_size=3, padding=1),  # 1→32通道
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(2),                               # 28→14
            torch.nn.Conv2d(32, 64, kernel_size=3, padding=1),  # 32→64
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(2),                               # 14→7
        )
        self.fc = torch.nn.Linear(64 * 7 * 7, num_classes)

    def forward(self, x):
        x = self.conv(x)
        x = x.view(x.size(0), -1)  # flatten
        return self.fc(x)

cnn = SimpleCNN()
dummy_img = torch.randn(16, 1, 28, 28)  # batch=16, 灰度28x28
out = cnn(dummy_img)
print(f"CNN 输入 (16,1,28,28) → 输出 {out.shape} (16,10)")
print(f"CNN参数量: {sum(p.numel() for p in cnn.parameters())}")

# ============ 3.6 完整训练流程 ============
print("\n=== 3.6 完整训练流程 ===")

def train_epoch(model, X, y, loss_fn, optimizer):
    model.train()
    pred = model(X)
    loss = loss_fn(pred, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    return loss.item()

# 用 MLP 做分类（模拟数据）
torch.manual_seed(42)
X_cls = torch.randn(200, 2)  # 二维输入
y_cls = (X_cls[:, 0]**2 + X_cls[:, 1]**2 > 1).float().unsqueeze(1)

class Classifier(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.net = torch.nn.Sequential(
            torch.nn.Linear(2, 16),
            torch.nn.ReLU(),
            torch.nn.Linear(16, 16),
            torch.nn.ReLU(),
            torch.nn.Linear(16, 1),
            torch.nn.Sigmoid(),
        )
    def forward(self, x):
        return self.net(x)

model = Classifier()
loss_fn = torch.nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

print("训练分类器...")
for epoch in range(500):
    loss = train_epoch(model, X_cls, y_cls, loss_fn, optimizer)
    if epoch % 100 == 0:
        acc = ((model(X_cls) > 0.5).float() == y_cls).float().mean()
        print(f"  Epoch {epoch:3d} | Loss: {loss:.4f} | Acc: {acc:.4f}")

print("\n✅ 阶段3完成！")
