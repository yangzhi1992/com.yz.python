"""
阶段4：Transformer 核心原理
===========================
学习内容:
  1. 自注意力机制 Self-Attention
  2. 多头注意力 Multi-Head Attention
  3. 位置编码 Positional Encoding
  4. Transformer Encoder 完整实现
  5. 使用预训练模型（BERT/GPT）
"""

import torch
import torch.nn.functional as F
import math

# ============ 4.1 缩放点积注意力 ============
print("=== 4.1 缩放点积注意力 Scaled Dot-Product Attention ===")

def scaled_dot_product_attention(Q, K, V, mask=None):
    """
    Attention(Q,K,V) = softmax(QK^T/√d_k) * V
    Q, K, V: [batch, heads, seq_len, d_k]
    """
    d_k = Q.size(-1)
    scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d_k)
    if mask is not None:
        scores = scores.masked_fill(mask == 0, -1e9)
    attn_weights = F.softmax(scores, dim=-1)
    output = torch.matmul(attn_weights, V)
    return output, attn_weights

# 测试：序列长度4，每个词关注哪些词
batch, heads, seq_len, d_k = 1, 1, 4, 8
Q = torch.randn(batch, heads, seq_len, d_k)
K = torch.randn(batch, heads, seq_len, d_k)
V = torch.randn(batch, heads, seq_len, d_k)

output, weights = scaled_dot_product_attention(Q, K, V)
print(f"注意力输出形状: {output.shape}")
print(f"注意力权重 (关注关系):\n{weights[0,0].detach().numpy().round(2)}")

# ============ 4.2 多头注意力 ============
print("\n=== 4.2 多头注意力 Multi-Head Attention ===")

class MultiHeadAttention(torch.nn.Module):
    def __init__(self, d_model=512, num_heads=8):
        super().__init__()
        assert d_model % num_heads == 0
        self.num_heads = num_heads
        self.d_k = d_model // num_heads

        self.W_Q = torch.nn.Linear(d_model, d_model)
        self.W_K = torch.nn.Linear(d_model, d_model)
        self.W_V = torch.nn.Linear(d_model, d_model)
        self.W_O = torch.nn.Linear(d_model, d_model)

    def forward(self, x, mask=None):
        batch, seq_len, d_model = x.shape

        # 1. 线性变换 + 拆分为多头
        Q = self.W_Q(x).view(batch, seq_len, self.num_heads, self.d_k).transpose(1, 2)
        K = self.W_K(x).view(batch, seq_len, self.num_heads, self.d_k).transpose(1, 2)
        V = self.W_V(x).view(batch, seq_len, self.num_heads, self.d_k).transpose(1, 2)

        # 2. 注意力计算
        attn_output, _ = scaled_dot_product_attention(Q, K, V, mask)

        # 3. 合并多头
        attn_output = attn_output.transpose(1, 2).contiguous().view(batch, seq_len, d_model)

        # 4. 输出投影
        return self.W_O(attn_output)

mha = MultiHeadAttention(d_model=64, num_heads=8)
dummy = torch.randn(2, 10, 64)  # batch=2, seq=10, d_model=64
out = mha(dummy)
print(f"多头注意力: 输入(2,10,64) → 输出{out.shape}")

# ============ 4.3 位置编码 ============
print("\n=== 4.3 位置编码 Positional Encoding ===")

class PositionalEncoding(torch.nn.Module):
    """Transformer 原版位置编码（正弦+余弦）"""
    def __init__(self, d_model, max_seq_len=5000):
        super().__init__()
        pe = torch.zeros(max_seq_len, d_model)
        position = torch.arange(0, max_seq_len).unsqueeze(1).float()
        div_term = torch.exp(torch.arange(0, d_model, 2).float() *
                             -(math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)  # 偶数维度 sin
        pe[:, 1::2] = torch.cos(position * div_term)  # 奇数维度 cos
        self.register_buffer('pe', pe.unsqueeze(0))

    def forward(self, x):
        return x + self.pe[:, :x.size(1)]

pe = PositionalEncoding(d_model=64)
dummy = torch.zeros(1, 10, 64)
out = pe(dummy)
print(f"位置编码: pos_enc形状={pe.pe.shape}, 输出={out.shape}")

# ============ 4.4 Transformer Encoder ============
print("\n=== 4.4 Transformer Encoder（完整层）===")

class TransformerEncoderLayer(torch.nn.Module):
    """单层 Transformer Encoder"""
    def __init__(self, d_model=512, num_heads=8, d_ff=2048, dropout=0.1):
        super().__init__()
        self.self_attn = MultiHeadAttention(d_model, num_heads)
        self.ffn = torch.nn.Sequential(
            torch.nn.Linear(d_model, d_ff),
            torch.nn.ReLU(),
            torch.nn.Linear(d_ff, d_model),
        )
        self.norm1 = torch.nn.LayerNorm(d_model)
        self.norm2 = torch.nn.LayerNorm(d_model)
        self.dropout = torch.nn.Dropout(dropout)

    def forward(self, x):
        # 自注意力 + 残差连接 + LayerNorm
        attn_out = self.self_attn(x)
        x = self.norm1(x + self.dropout(attn_out))
        # FFN + 残差连接 + LayerNorm
        ffn_out = self.ffn(x)
        x = self.norm2(x + self.dropout(ffn_out))
        return x

layer = TransformerEncoderLayer(d_model=64, num_heads=4, d_ff=256)
dummy = torch.randn(2, 10, 64)
out = layer(dummy)
print(f"Encoder层: 输入(2,10,64) → 输出{out.shape}")

# ============ 4.5 使用预训练模型 ============
print("\n=== 4.5 使用预训练模型 ===")

# 这里展示 API 调用方式（不需要实际下载模型）
# 实际使用时取消注释：
#
# from transformers import AutoTokenizer, AutoModel
#
# tokenizer = AutoTokenizer.from_pretrained("bert-base-chinese")
# model = AutoModel.from_pretrained("bert-base-chinese")
#
# text = "Transformer 是大模型的骨干结构"
# inputs = tokenizer(text, return_tensors="pt")
# outputs = model(**inputs)
# print(f"BERT输出形状: {outputs.last_hidden_state.shape}")
# print(f"文本向量: {outputs.pooler_output[0][:10]}...")

print("""
预训练模型使用流程:
  1. from transformers import AutoTokenizer, AutoModel
  2. tokenizer = AutoTokenizer.from_pretrained("模型名")
  3. model = AutoModel.from_pretrained("模型名")
  4. inputs = tokenizer("文本", return_tensors="pt")
  5. outputs = model(**inputs)
  6. 取 outputs.last_hidden_state 或 outputs.pooler_output

常用中文模型:
  - BERT:       bert-base-chinese
  - RoBERTa:    hfl/rbt3
  - GPT:        GPT2-chinese
  - LLM:        Qwen/Qwen2-7B-Instruct
""")

print("\n✅ 阶段4完成！")
