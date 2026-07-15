"""
模块2：LoRA 轻量微调
=====================
作用：低成本适配垂直领域，节省显存和时间

文件格式: .safetensors (几MB~几百MB)
路径示例: models/lora/
"""

# ============ 2.1 学习路线 ============
print("=" * 60)
print("📚 LoRA 轻量微调 - 学习路线")
print("=" * 60)

LEARNING_ROADMAP = """
【前置知识】
  ├── 预训练模型 (Pre-training)
  ├── 微调概念 (Fine-tuning)
  └── 反向传播 + 梯度下降

【阶段1】PEFT 参数高效微调
  ├── Adapter (2019)
  │   └── 在Transformer层间插入小网络
  ├── Prefix Tuning (2021)
  │   └── 在输入前添加可训练向量
  ├── Prompt Tuning (2021)
  │   └── 只训练 soft prompt
  └── LoRA (2021) ← 主流选择
      └── 低秩分解：W' = W + BA

【阶段2】LoRA 深入
  ├── 原理：W ∈ R^{d×k}, B ∈ R^{d×r}, A ∈ R^{r×k}, r << d,k
  ├── rank选择：r=8/16/32/64
  ├── target_modules: q_proj, v_proj, k_proj, o_proj
  ├── lora_alpha: 缩放系数
  └── lora_dropout: 防止过拟合

【阶段3】LoRA 变体
  ├── QLoRA: LoRA + 4bit 量化
  │   └── 双重量化 + NF4 + 分页优化
  ├── DoRA: 权重分解 LoRA
  ├── VeRA: 共享低秩矩阵
  └── LoRA-FA: 只训练 A 不训练 B

【阶段4】实战流程
  ├── 数据准备 (Alpaca/ShareGPT格式)
  ├── 模型加载 (4bit量化)
  ├── LoRA配置 (PEFT)
  ├── 训练 (SFT/DPO)
  └── 导出与合并
"""
print(LEARNING_ROADMAP)

# ============ 2.2 从零实现 LoRA ============
print("\n" + "=" * 60)
print("🔧 Demo: 从零实现 LoRA")
print("=" * 60)

import torch
import torch.nn as nn
import math

class LoRALayer(nn.Module):
    """低秩适应层"""
    def __init__(self, in_dim, out_dim, rank=8, alpha=32, dropout=0.1):
        super().__init__()
        self.scaling = alpha / rank
        self.lora_A = nn.Parameter(torch.randn(in_dim, rank) * 0.01)
        self.lora_B = nn.Parameter(torch.zeros(rank, out_dim))
        self.dropout = nn.Dropout(dropout) if dropout > 0 else nn.Identity()

    def forward(self, x):
        # LoRA 前向: x @ (A @ B)
        return self.dropout(x) @ (self.lora_A @ self.lora_B) * self.scaling

class LinearWithLoRA(nn.Module):
    """带 LoRA 的线性层"""
    def __init__(self, linear: nn.Linear, rank=8, alpha=32):
        super().__init__()
        self.linear = linear  # 原始权重 (冻结)
        self.linear.weight.requires_grad = False
        self.lora = LoRALayer(
            linear.in_features, linear.out_features, rank, alpha
        )

    def forward(self, x):
        # Wx + BAx
        return self.linear(x) + self.lora(x)

    def merge_weights(self):
        """将 LoRA 权重合并到原始权重（用于部署）"""
        W = self.linear.weight.data
        BA = self.lora.lora_A.data @ self.lora.lora_B.data * self.lora.scaling
        self.linear.weight.data = W + BA.T
        self.lora.lora_A.data.zero_()
        self.lora.lora_B.data.zero_()

# ============ 测试 ============
print("\n🧪 测试 LoRA:")
orig = nn.Linear(4096, 4096, bias=False)
lora_layer = LinearWithLoRA(orig, rank=8, alpha=32)

x = torch.randn(2, 4096)
orig_out = orig(x)
lora_out = lora_layer(x)

print(f"  原始权重: {tuple(orig.weight.shape)} ({orig.weight.numel():,} 参数)")
print(f"  LoRA参数: {lora_layer.lora.lora_A.numel() + lora_layer.lora.lora_B.numel():,}")
print(f"  参数减少: {orig.weight.numel() / (lora_layer.lora.lora_A.numel() + lora_layer.lora.lora_B.numel()):.0f}x")
print(f"  输出一致: {torch.allclose(orig_out, lora_out, atol=1e-3)} (权重还没训练)")

# 合并测试
lora_layer.merge_weights()
merged_out = lora_layer.linear(x)
print(f"  合并后输出与原始一致: {torch.allclose(orig_out, merged_out, atol=1e-3)}")

# ============ 2.3 不同 rank 对比 ============
print("\n" + "=" * 60)
print("🔧 Demo: 不同 rank 的参数量对比")
print("=" * 60)

d_model = 4096  # 7B模型的维度
print(f"\n当 d_model={d_model} 时:")
print(f"{'rank':<8} {'LoRA参数量':<15} {'原始参数量':<15} {'减少比例'}")
print("-" * 55)
for r in [1, 2, 4, 8, 16, 32, 64, 128]:
    lora_params = (d_model * r + r * d_model)  # A + B
    orig_params = d_model * d_model
    ratio = orig_params / lora_params
    print(f"{r:<8} {lora_params:<15,} {orig_params:<15,} {ratio:.0f}x")

# ============ 2.4 使用 PEFT 库 ============
print("\n" + "=" * 60)
print("🔧 Demo: 使用 PEFT 库进行 LoRA 配置")
print("=" * 60)

PEFT_GUIDE = """
# 安装: pip install peft transformers

from peft import LoraConfig, get_peft_model, TaskType

# LoRA 配置
lora_config = LoraConfig(
    r=16,                    # 秩
    lora_alpha=64,           # 缩放系数
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
    lora_dropout=0.1,
    bias="none",
    task_type=TaskType.CAUSAL_LM,
)

# 加载基础模型
from transformers import AutoModelForCausalLM
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2-7B-Instruct")

# 应用 LoRA
model = get_peft_model(model, lora_config)

# 查看可训练参数
model.print_trainable_parameters()
# 输出: trainable params: 8,388,608 || all params: 7,000,000,000 || trainable%: 0.12%

# 训练后保存
model.save_pretrained("./my_lora_adapter")

# 推理时加载
from peft import PeftModel
model = PeftModel.from_pretrained(base_model, "./my_lora_adapter")
model = model.merge_and_unload()  # 合并权重加速推理

# 常用 target_modules:
#   Llama: q_proj, v_proj, k_proj, o_proj, gate_proj, up_proj, down_proj
#   ChatGLM: query_key_value, dense
#   Qwen: q_proj, v_proj, k_proj, o_proj

# LoRA 训练显存对比 (7B模型):
#   全量微调: ~140GB  (8×A100)
#   LoRA:     ~36GB   (1×A100)
#   QLoRA:    ~8GB    (1×RTX 4090)
"""
print(PEFT_GUIDE)

print("\n✅ LoRA模块完成！")
