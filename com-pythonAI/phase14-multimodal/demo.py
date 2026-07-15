"""
阶段14：多模态大模型开发
=========================
学习内容:
  1. 多模态概念：文本+图像+音频+视频
  2. CLIP 图文对齐
  3. LLaVA 视觉语言模型
  4. Stable Diffusion 文生图
  5. Whisper 语音识别
  6. 多模态应用场景
"""

# ============ 14.1 多模态概念 ============
print("=== 14.1 多模态概念 ===")

MULTIMODAL_CONCEPTS = """
🖼️ 多模态大模型

模态 = 信息的表现形式

单模态：                   多模态：
  文本模型(GPT)              图文理解(LLaVA)
  图像模型(Stable Diffusion)  文生图(SD/DALL-E)
  语音模型(Whisper)          语音转文字(Whisper)
  视频模型                   视频理解

主流多模态模型:
  模型          输入         输出
  ──────────────────────────────
  GPT-4V        文本+图片      文本
  LLaVA         文本+图片      文本
  Qwen-VL       文本+图片      文本
  Stable Diff.  文本           图片
  DALL-E 3      文本           图片
  Whisper       音频           文本
  Sora          文本           视频
"""
print(MULTIMODAL_CONCEPTS)

# ============ 14.2 CLIP 图文对齐 ============
print("\n=== 14.2 CLIP 图文对齐 ===")

CLIP_EXAMPLE = """
📸 CLIP (Contrastive Language-Image Pre-training)

核心思想：
  将图像和文本映射到同一向量空间
  图片 → Image Encoder → [0.1, 0.2, ...]
  文本 → Text Encoder  → [0.1, 0.2, ...]
  匹配的图文对 → 向量距离近

应用场景：
  • 图文检索（搜图、搜文）
  • 零样本分类（不用训练就能分类新类别）
  • 多模态相似度计算

# 使用 OpenCLIP
# pip install open-clip-torch

import torch
import clip

model, preprocess = clip.load("ViT-B/32")

# 编码图片
image = preprocess(image).unsqueeze(0)
image_features = model.encode_image(image)

# 编码文本
text = clip.tokenize(["一只猫", "一条狗"])
text_features = model.encode_text(text)

# 计算相似度
similarity = (image_features @ text_features.T).softmax(dim=-1)
"""
print(CLIP_EXAMPLE)

# ============ 14.3 LLaVA 视觉语言模型 ============
print("\n=== 14.3 LLaVA (Large Language and Vision Assistant) ===")

LLAVA_GUIDE = """
👁️ LLaVA 架构

LLaVA = 视觉编码器 + 投影层 + LLM

流程：
  图片 → CLIP ViT → 视觉特征 → 投影层 → LLM → 回答
                                            ↑
                                       用户提问

# Ollama 运行 LLaVA
ollama pull llava     # 或 bakllava

# API 调用
curl http://localhost:11434/api/chat -d '{
    "model": "llava",
    "messages": [
        {
            "role": "user",
            "content": "描述这张图片",
            "images": ["base64_encoded_image"]
        }
    ]
}'

# 功能：
# ✓ 图片内容描述
# ✓ 图表解读
# ✓ 文档 OCR
# ✓ 视觉问答
"""
print(LLAVA_GUIDE)

# ============ 14.4 Stable Diffusion 文生图 ============
print("\n=== 14.4 Stable Diffusion 文生图 ===")

SD_GUIDE = """
🎨 Stable Diffusion 文生图

# 安装: pip install diffusers transformers accelerate

from diffusers import StableDiffusionPipeline
import torch

# 加载模型
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16,
)
pipe = pipe.to("cuda")

# 生成图片
prompt = "一只橘猫坐在太空飞船里，数字艺术风格"
image = pipe(
    prompt,
    negative_prompt="模糊, 低质量",  # 负向提示
    num_inference_steps=30,           # 步数（越高质量越好）
    guidance_scale=7.5,               # 文本相关性（越高越贴合prompt）
).images[0]

image.save("output.png")

# 高级应用：
# • ControlNet: 姿势控制、边缘控制、深度控制
# • LoRA: 特定风格/角色的微调
# • IP-Adapter: 图生图（以图生图）
# • T2I-Adapter: 条件控制

# 在线体验: https://huggingface.co/spaces/stabilityai/stable-diffusion
"""
print(SD_GUIDE)

# ============ 14.5 Whisper 语音识别 ============
print("\n=== 14.5 Whisper 语音识别 ===")

WHISPER_GUIDE = """
🎤 Whisper 语音转文字

# 安装: pip install openai-whisper

import whisper

# 加载模型
model = whisper.load_model("base")  # tiny/base/small/medium/large

# 语音转文字
result = model.transcribe("audio.mp3")
print(result["text"])       # 识别文本
print(result["language"])   # 检测语言

# 模型大小对比
# tiny:    39M   ~1GB显存
# base:    74M   ~1GB显存
# small:   244M  ~2GB显存
# medium:  769M  ~5GB显存
# large:   1550M ~10GB显存

# Ollama 集成
# ollama pull whisper
# curl http://localhost:11434/api/chat -d '{
#     "model": "whisper",
#     "messages": [{"role":"user","content":"识别音频"}]
# }'
"""
print(WHISPER_GUIDE)

# ============ 14.6 多模态应用Demo ============
print("\n=== 14.6 多模态应用场景 ===")

def multimodal_demo():
    """模拟多模态应用"""

    scenarios = {
        "智能客服": [
            "📷 用户发了一张产品照片",
            "🎤 用户语音描述问题",
            "🤖 AI 理解图片+语音，回复处理方案",
        ],
        "内容创作": [
            "📝 输入文案: '一只在太空漫步的猫'",
            "🎨 Stable Diffusion 生成图片",
            "🎵 MusicGen 生成背景音乐",
            "📹 组合成短视频",
        ],
        "教育辅助": [
            "📷 拍下数学题照片",
            "🤖 LLaVA 识别题目",
            "📝 GPT 生成解题步骤",
            "🎤 TTS 语音讲解",
        ],
    }

    for app_name, steps in scenarios.items():
        print(f"\n📱 {app_name}:")
        for step in steps:
            print(f"  {step}")

multimodal_demo()

# ============ 14.7 多模态开发工具 ============
print("\n=== 14.7 多模态开发工具 ===")

TOOLS = """
🛠️ 多模态开发工具栈

视觉理解:
  • LLaVA / Qwen-VL / InternVL — 图文理解
  • CLIP / SigLIP — 图文向量对齐
  • YOLO / DETR — 目标检测

图像生成:
  • Stable Diffusion — 主流文生图
  • ControlNet — 生成控制
  • ComfyUI — 工作流编辑器

语音处理:
  • Whisper — 语音识别
  • CosyVoice / FishSpeech — 语音合成
  • VoiceCraft — 语音克隆

视频处理:
  • Sora (OpenAI) — 文生视频
  • CogVideo / AnimateDiff — 视频生成
  • VideoRetalking — 数字人口型同步

向量数据库:
  • Milvus — 多模态向量检索
  • CLIP 作为多模态特征提取器
"""
print(TOOLS)

print("\n✅ 阶段14完成！")
print("=" * 50)
print("🎉 恭喜！你已完成整个大模型学习路线！")
print("=" * 50)
