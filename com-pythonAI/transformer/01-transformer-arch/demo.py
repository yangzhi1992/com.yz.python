"""
模块1：Transformer 骨干架构
=============================
核心模块，负责语义理解和上下文建模

文件格式: 结构文件+权重 (GB级)
路径示例: models/transformer/
"""

# ============ 1.1 学习路线 ============
print("=" * 60)
print("📚 Transformer 骨干架构 - 学习路线")
print("=" * 60)

LEARNING_ROADMAP = """
【阶段1】前置基础
  ├── 词嵌入 Word Embedding
  │   ├── One-hot → Word2Vec → GloVe → BERT Embedding
  │   └── demo: 词向量相似度计算
  ├── RNN / LSTM / GRU
  │   ├── 循环神经网络原理
  │   ├── 梯度消失/梯度爆炸
  │   └── demo: 手写RNN文本生成
  └── Attention 机制起源
      ├── Bahdanau Attention (2014)
      ├── Luong Attention (2015)
      └── demo: 注意力权重可视化

【阶段2】Transformer 核心
  ├── Scaled Dot-Product Attention
  │   └── demo: QKV计算 + softmax
  ├── Multi-Head Attention
  │   └── demo: 8头注意力实现
  ├── Positional Encoding
  │   ├── Sinusoidal PE (原版)
  │   ├── RoPE (旋转位置编码)
  │   └── ALiBi (线性偏置)
  └── Feed-Forward Network
      └── demo: FFN + ReLU/SwiGLU

【阶段3】完整架构
  ├── Encoder (编码器)
  │   └── Self-Attention + FFN + Residual + LayerNorm
  ├── Decoder (解码器)
  │   ├── Masked Self-Attention
  │   ├── Cross-Attention
  │   └── demo: 自动回归生成
  └── Encoder-Decoder 完整流程
      └── demo: 机器翻译

【阶段4】主流变体
  ├── BERT: Encoder-Only
  │   └── MLM + NSP 预训练
  ├── GPT: Decoder-Only
  │   └── 自回归语言模型
  ├── T5: Encoder-Decoder
  │   └── Text-to-Text 统一框架
  └── MoE (混合专家)
      └── Mixtral 8×7B 架构

【阶段5】前沿优化
  ├── RMSNorm vs LayerNorm
  ├── GQA (Grouped Query Attention)
  ├── SwiGLU Activation
  ├── Flash Attention
  └── KV Cache 优化
"""
print(LEARNING_ROADMAP)

# ============ 1.2 从零实现完整 Transformer ============
print("\n" + "=" * 60)
print("🔧 Demo: 从零实现Transformer Encoder块")
print("=" * 60)

import torch
import torch.nn as nn
import torch.nn.functional as F
import math

class LayerNorm(nn.Module):
    """Layer Normalization"""
    def __init__(self, d_model, eps=1e-5):
        super().__init__()
        self.gamma = nn.Parameter(torch.ones(d_model))
        self.beta = nn.Parameter(torch.zeros(d_model))
        self.eps = eps

    def forward(self, x):
        mean = x.mean(-1, keepdim=True)
        std = x.std(-1, keepdim=True)
        return self.gamma * (x - mean) / (std + self.eps) + self.beta

class RMSNorm(nn.Module):
    """Root Mean Square Layer Normalization (Llama 使用的版本)"""
    def __init__(self, d_model, eps=1e-5):
        super().__init__()
        self.weight = nn.Parameter(torch.ones(d_model))
        self.eps = eps

    def forward(self, x):
        rms = torch.sqrt(x.pow(2).mean(-1, keepdim=True) + self.eps)
        return self.weight * x / rms

class RoPE(nn.Module):
    """旋转位置编码 Rotary Position Embedding"""
    def __init__(self, d_model, max_len=2048):
        super().__init__()
        inv_freq = 1.0 / (10000 ** (torch.arange(0, d_model, 2).float() / d_model))
        self.register_buffer("inv_freq", inv_freq)

    def forward(self, x, seq_len):
        t = torch.arange(seq_len, device=x.device).type_as(self.inv_freq)
        freqs = torch.einsum("i,j->ij", t, self.inv_freq)
        emb = torch.cat((freqs, freqs), dim=-1)
        return emb[:seq_len]

def apply_rope(x, pos_emb):
    """应用 RoPE 到 Q 和 K"""
    cos = pos_emb.cos()
    sin = pos_emb.sin()
    x2 = torch.stack([-x[..., 1::2], x[..., ::2]], dim=-1).reshape_as(x)
    return x * cos + x2 * sin

class MultiHeadAttention(nn.Module):
    """多头注意力（支持 GQA 可选）"""
    def __init__(self, d_model, n_heads, n_kv_heads=None, use_rope=False):
        super().__init__()
        self.n_heads = n_heads
        self.n_kv_heads = n_kv_heads or n_heads
        self.d_k = d_model // n_heads
        self.use_rope = use_rope

        self.W_Q = nn.Linear(d_model, d_model, bias=False)
        self.W_K = nn.Linear(d_model, self.n_kv_heads * self.d_k, bias=False)
        self.W_V = nn.Linear(d_model, self.n_kv_heads * self.d_k, bias=False)
        self.W_O = nn.Linear(d_model, d_model, bias=False)

        if use_rope:
            self.rope = RoPE(self.d_k)

    def forward(self, x, mask=None):
        batch, seq_len, _ = x.shape

        Q = self.W_Q(x).view(batch, seq_len, self.n_heads, self.d_k).transpose(1, 2)
        K = self.W_K(x).view(batch, seq_len, self.n_kv_heads, self.d_k).transpose(1, 2)
        V = self.W_V(x).view(batch, seq_len, self.n_kv_heads, self.d_k).transpose(1, 2)

        # RoPE (GQA: 对K做repeat)
        if self.use_rope:
            pos_emb = self.rope(x, seq_len)
            Q = apply_rope(Q, pos_emb)
            K = apply_rope(K, pos_emb)

        # GQA: 扩展 K, V 头数匹配 Q
        if self.n_kv_heads != self.n_heads:
            repeat = self.n_heads // self.n_kv_heads
            K = K.repeat_interleave(repeat, dim=1)
            V = V.repeat_interleave(repeat, dim=1)

        # 注意力
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)
        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)
        attn = F.softmax(scores, dim=-1)
        output = torch.matmul(attn, V)
        output = output.transpose(1, 2).contiguous().view(batch, seq_len, -1)
        return self.W_O(output)

class SwiGLU(nn.Module):
    """SwiGLU 激活函数 (Llama 使用)"""
    def __init__(self, d_model, d_ff):
        super().__init__()
        self.W1 = nn.Linear(d_model, d_ff, bias=False)
        self.W2 = nn.Linear(d_model, d_ff, bias=False)
        self.W3 = nn.Linear(d_ff, d_model, bias=False)

    def forward(self, x):
        return self.W3(F.silu(self.W1(x)) * self.W2(x))

class TransformerBlock(nn.Module):
    """完整 Transformer 块"""
    def __init__(self, d_model=512, n_heads=8, d_ff=2048, use_rope=True, use_swiglu=True):
        super().__init__()
        self.attention = MultiHeadAttention(d_model, n_heads, use_rope=use_rope)
        self.norm1 = RMSNorm(d_model)
        self.ffn = SwiGLU(d_model, d_ff) if use_swiglu else nn.Sequential(
            nn.Linear(d_model, d_ff), nn.ReLU(), nn.Linear(d_ff, d_model))
        self.norm2 = RMSNorm(d_model)

    def forward(self, x):
        x = x + self.attention(self.norm1(x))
        x = x + self.ffn(self.norm2(x))
        return x

# ============ 测试 ============
print("\n🧪 测试 Transformer 块:")
d_model, n_heads, seq_len, batch = 64, 4, 10, 2
block = TransformerBlock(d_model, n_heads, d_ff=256, use_rope=True, use_swiglu=True)
x = torch.randn(batch, seq_len, d_model)
out = block(x)
print(f"  输入: ({batch}, {seq_len}, {d_model})")
print(f"  输出: {tuple(out.shape)}")
print(f"  参数量: {sum(p.numel() for p in block.parameters()):,}")

# ============ 1.3 预训练模型加载 ============
print("\n" + "=" * 60)
print("🔧 Demo: 加载预训练Transformer (HuggingFace)")
print("=" * 60)

HF_GUIDE = """
# 使用 HuggingFace Transformers 加载预训练模型

## 1. BERT (编码器)
from transformers import BertModel, BertTokenizer
model = BertModel.from_pretrained("bert-base-chinese")
tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
# 输出: [batch, seq_len, 768]

## 2. GPT (解码器)
from transformers import GPT2Model, GPT2Tokenizer
model = GPT2Model.from_pretrained("gpt2")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
# 输出: [batch, seq_len, 768]

## 3. Llama (现代架构)
from transformers import LlamaModel, LlamaTokenizer
model = LlamaModel.from_pretrained("meta-llama/Llama-2-7b-hf")
# 输出: [batch, seq_len, 4096]
# 特点: RMSNorm + RoPE + SwiGLU + GQA

## 4. Qwen2 (国产)
from transformers import AutoModel, AutoTokenizer
model = AutoModel.from_pretrained("Qwen/Qwen2-7B-Instruct", trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2-7B-Instruct")

## 架构对比
# 模型     | 参数   | 层数 | 头数 | d_model | 特色
# BERT     | 110M   | 12   | 12   | 768     | Encoder, MLM
# GPT2     | 124M   | 12   | 12   | 768     | Decoder, 自回归
# Llama2   | 7B     | 32   | 32   | 4096    | RoPE+GQA+SwiGLU
# Qwen2    | 7B     | 28   | 28   | 3584    | 中文优化
# Mistral  | 7B     | 32   | 8GQA | 4096    | Sliding Window
"""
print(HF_GUIDE)

print("\n✅ Transformer模块完成！")
