"""
模块5：VAE/解码模块
====================
作用：多模态中还原图像/音频/特征

文件格式: .ckpt / .safetensors
路径示例: models/VAE/
"""

# ============ 5.1 学习路线 ============
print("=" * 60)
print("📚 VAE/解码模块 - 学习路线")
print("=" * 60)

LEARNING_ROADMAP = """
【前置基础】
  ├── 自编码器 (Autoencoder)
  │   ├── Encoder: 高维→低维 (压缩)
  │   └── Decoder: 低维→高维 (还原)
  ├── 变分推断
  └── 重参数化技巧 (Reparameterization Trick)

【阶段1】VAE (Variational Autoencoder)
  ├── 原理: 学习数据的分布而非确定性映射
  │   └── 编码器输出 μ 和 σ，从中采样
  ├── KL 散度损失
  │   └── 让后验分布接近标准正态分布
  ├── 重构损失
  │   └── MSE / BCE 重建误差
  └── VAE 公式: L = E[log p(x|z)] - KL(q(z|x)||p(z))

【阶段2】Stable Diffusion 中的 VAE
  ├── 将图片压缩到潜在空间 (8×压缩)
  │   └── 512×512 的图 → 64×64 的潜在表示
  ├── 为什么需要 VAE？
  │   └── 在潜在空间做扩散，计算量大幅减少
  ├── KL-F8 VAE (SD 1.x/2.x)
  └── VQ-GAN / VQ-VAE (SDXL)

【阶段3】图像解码 (Image Decoding)
  ├── 文生图: VAE Decoder (Latent → Pixel)
  ├── 图生图: VAE Encoder (Pixel → Latent)
  ├── ControlNet: 条件控制 (Canny/Depth/Pose)
  └── Upscaler: 超分辨率 (4×/8×放大)

【阶段4】音频解码 (Audio Decoding)
  ├── Vocoder: mel频谱 → 波形
  │   └── HiFi-GAN, MelGAN
  ├── Audio VAE: 音频压缩与重建
  └── 语音合成: Tacotron → Vocoder

【阶段5】视频解码 (Video Decoding)
  ├── 帧间压缩 (H.264/H.265)
  ├── 3D VAE (视频潜在空间)
  └── Sora: 时空压缩 + Diffusion
"""
print(LEARNING_ROADMAP)

# ============ 5.2 从零实现 VAE ============
print("\n" + "=" * 60)
print("🔧 Demo: 从零实现 VAE")
print("=" * 60)

import torch
import torch.nn as nn
import torch.nn.functional as F

class VAE(nn.Module):
    """变分自编码器 (从零实现)"""
    def __init__(self, input_dim=784, latent_dim=20, hidden_dim=256):
        super().__init__()
        # Encoder
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
        )
        self.mu_layer = nn.Linear(hidden_dim, latent_dim)
        self.logvar_layer = nn.Linear(hidden_dim, latent_dim)

        # Decoder
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, input_dim),
            nn.Sigmoid(),
        )

    def encode(self, x):
        h = self.encoder(x)
        return self.mu_layer(h), self.logvar_layer(h)

    def reparameterize(self, mu, logvar):
        """重参数化技巧: z = μ + σ * ε"""
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return mu + eps * std

    def decode(self, z):
        return self.decoder(z)

    def forward(self, x):
        mu, logvar = self.encode(x)
        z = self.reparameterize(mu, logvar)
        recon = self.decode(z)
        return recon, mu, logvar

def vae_loss(recon_x, x, mu, logvar):
    """VAE 损失 = 重构损失 + KL 散度"""
    # 1. 重构损失 (BCE)
    recon_loss = F.binary_cross_entropy(recon_x, x, reduction='sum')
    # 2. KL 散度
    kl_loss = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
    return recon_loss + kl_loss, recon_loss, kl_loss

# 测试 VAE
print("\n🧪 测试 VAE (模拟MNIST):")
vae = VAE(input_dim=784, latent_dim=20)
dummy_img = torch.randn(4, 784)  # batch=4, 28×28=784
recon, mu, logvar = vae(dummy_img)
loss, recon_loss, kl_loss = vae_loss(recon, dummy_img, mu, logvar)

print(f"  输入: {tuple(dummy_img.shape)}")
print(f"  重建: {tuple(recon.shape)}")
print(f"  潜在空间均值: {mu.shape}")
print(f"  总损失: {loss.item():.2f}")
print(f"  重构损失: {recon_loss.item():.2f}")
print(f"  KL散度: {kl_loss.item():.2f}")

# 从潜在空间生成
print("\n  从潜在空间采样生成:")
z = torch.randn(2, 20)
gen = vae.decode(z)
print(f"  随机噪声 (2,20) → 生成 (2,784)")

# ============ 5.3 SD VAE 压缩比 ============
print("\n" + "=" * 60)
print("🔧 Demo: Stable Diffusion VAE 压缩")
print("=" * 60)

SD_VAE_GUIDE = """
Stable Diffusion VAE 压缩流程:

原始图像 (512×512×3 = 786,432)
        │
        ▼ VAE Encoder (8× 压缩)
        │
潜在表示 (64×64×4 = 16,384) → 压缩比: 48×
        │
        ▼ UNet + Diffusion (在潜在空间做)
        │
        ▼ VAE Decoder (8× 放大)
        │
生成图像 (512×512×3 = 786,432)

┌─────────────────────────────────────────────┐
│  为什么需要在潜在空间做扩散？                 │
│                                              │
│  像素空间(512²):    每一步处理 786K 数据      │
│  潜在空间(64²):     每一步处理 16K 数据       │
│  速度提升: ~48×                               │
│                                              │
│  SD 1.x:  KL-F8 VAE, 8×压缩                  │
│  SDXL:   更大的 VAE, 更精细                   │
│  SD3:     16通道 VAE, 16×压缩                │
└─────────────────────────────────────────────┘
"""
print(SD_VAE_GUIDE)

# ============ 5.4 不同 VAE 模型 ============
print("\n" + "=" * 60)
print("🔧 Demo: VAE 模型对比")
print("=" * 60)

VAE_COMPARISON = """
📊 VAE 模型对比

模型                   应用            压缩比   参数    特点
───────────────────────────────────────────────────────────
VAE (基础)             MNIST生成       1×       2M    简单
VQ-VAE                图像生成         8×      30M    离散编码
KL-F8 VAE             SD 1.x/2.x      8×      84M    稳定扩散标配
VQ-GAN                图像生成         8×      50M    感知损失
SDXL VAE              SDXL            8×      134M   高保真
Consistency VAE       实时生成         8×      67M    单步解码
TAE (Temporal AE)     视频生成         4×     120M    时序感知

SD VAE 使用方式:
    from diffusers import AutoencoderKL

    vae = AutoencoderKL.from_pretrained(
        "stabilityai/sd-vae-ft-mse"
    )

    # 编码: 图像 → 潜在空间
    with torch.no_grad():
        latents = vae.encode(pixel_values).latent_dist.sample()

    # 解码: 潜在空间 → 图像
    with torch.no_grad():
        images = vae.decode(latents).sample

    # 检查点文件: .ckpt / .safetensors
    # 路径: models/VAE/
"""
print(VAE_COMPARISON)

# ============ 5.5 音频 VAE 概念 ============
print("\n" + "=" * 60)
print("🔧 Demo: 音频编解码概念")
print("=" * 60)

AUDIO_VAE = """
🎵 音频编解码流程

┌─────────────────────────────────────────────────────┐
│  音频编解码器 (如 EnCodec / DAC)                    │
│                                                     │
│  原始音频 (24kHz, 16bit)                            │
│        │                                            │
│        ▼ Encoder                                   │
│        │                                            │
│  潜在表示 (低帧率, 如 50fps)                       │
│        │                                            │
│        ▼ Decoder + Vocoder                         │
│        │                                            │
│  重建音频                                           │
└─────────────────────────────────────────────────────┘

常用模型:
  • EnCodec (Meta):   1.5kbps~24kbps, 高质量音频压缩
  • DAC (Descript):   更高质量的开源替代
  • HiFi-GAN:         mel频谱→波形 (Vocoder)

应用场景:
  • 音频压缩传输
  • 语音合成(TTS)的后端
  • 音乐生成(MusicGen)的编解码
  • 实时语音通信
"""
print(AUDIO_VAE)

print("\n✅ VAE/解码模块完成！")
