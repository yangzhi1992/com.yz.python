"""
阶段10：模型微调（LoRA / QLoRA）
=================================
学习内容:
  1. 微调概念：全量微调 vs 参数高效微调
  2. LoRA 原理（低秩适应）
  3. QLoRA（量化 LoRA）
  4. 使用 HuggingFace 进行微调
  5. 微调后的模型推理
"""

# ============ 10.1 微调概念 ============
print("=== 10.1 微调概念 ===")

CONCEPTS = """
🎯 微调概念对比

全量微调 (Full Fine-tuning):
  更新所有参数
  ✅ 效果好
  ❌ 需要 8×A100 80GB
  ❌ 显存需求: 7B模型约140GB

LoRA (Low-Rank Adaptation):
  冻结原始权重，注入低秩矩阵
  ✅ 显存需求: 7B模型约16GB
  ✅ 训练速度提升 3-5 倍
  ❌ 效果稍逊于全量微调

QLoRA (Quantized LoRA):
  LoRA + 4bit 量化
  ✅ 显存需求: 7B模型约6GB
  ✅ 单张 RTX 4090 可训练 7B 模型
  ✅ 效果接近 LoRA

P-Tuning / Prefix Tuning:
  只训练 prompt 嵌入
  适合超大规模模型（100B+）
"""
print(CONCEPTS)

# ============ 10.2 LoRA 原理 ============
print("\n=== 10.2 LoRA 原理 ===")

class LoRALayer:
    """
    LoRA: W' = W + BA
    W: 原始权重矩阵 (d×k) — 冻结
    B: 低秩矩阵 (d×r)
    A: 低秩矩阵 (r×k)
    r << min(d, k) — 通常 r=8 或 16
    """
    def __init__(self, orig_weight, rank=8):
        d, k = orig_weight.shape
        # B: (d, r), A: (r, k)
        import numpy as np
        self.B = np.random.randn(d, rank) * 0.01
        self.A = np.random.randn(rank, k) * 0.01
        self.orig_weight = orig_weight  # 冻结

    def forward(self, x):
        # y = x @ W + x @ (B@A)
        original = x @ self.orig_weight
        adaptation = x @ (self.B @ self.A)
        return original + adaptation * 0.1  # scaling

    def trainable_params(self):
        return self.B.size + self.A.size

import numpy as np
orig_w = np.random.randn(4096, 4096)  # 模拟 LLM 权重
lora = LoRALayer(orig_w, rank=8)

print(f"原始权重: {orig_w.shape}, 参数量: {orig_w.size:,}")
print(f"LoRA可训练: {lora.trainable_params():,}")
print(f"参数减少: {orig_w.size / lora.trainable_params():.0f}x")

# ============ 10.3 使用 transformers 微调 ============
print("\n=== 10.3 使用 HuggingFace 微调 ===")

FINETUNE_CODE = """
📝 使用 HuggingFace 完整微调流程

# 1. 安装依赖
pip install transformers datasets accelerate peft bitsandbytes

# 2. 加载预训练模型 + Tokenizer
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments
from peft import LoraConfig, get_peft_model, TaskType
from datasets import Dataset

model_name = "Qwen/Qwen2-0.5B-Instruct"  # 测试用小模型

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto",
)

# 3. 配置 LoRA
lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=8,              # 秩
    lora_alpha=32,    # 缩放系数
    lora_dropout=0.1,
    target_modules=["q_proj", "v_proj"],  # 只微调 Q 和 V
)

model = get_peft_model(model, lora_config)
print(f"可训练参数: {model.print_trainable_parameters()}")

# 4. 准备数据
dataset = Dataset.from_dict({
    "instruction": ["介绍一下你自己", "1+1等于几"],
    "output": ["我是一个AI助手", "1+1=2"],
})

def format_func(example):
    text = f"问：{example['instruction']}\\n答：{example['output']}"
    return tokenizer(text, truncation=True, padding="max_length", max_length=128)

dataset = dataset.map(format_func)

# 5. 配置训练参数
training_args = TrainingArguments(
    output_dir="./lora_output",
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    num_train_epochs=3,
    save_steps=500,
    logging_steps=10,
    learning_rate=2e-4,
    fp16=True,
)

# 6. 开始训练
# from transformers import Trainer
# trainer = Trainer(
#     model=model,
#     args=training_args,
#     train_dataset=dataset,
# )
# trainer.train()

# 7. 保存 LoRA 权重
# model.save_pretrained("./my_lora_adapter")

# 8. 加载 LoRA 进行推理
# from peft import PeftModel
# model = PeftModel.from_pretrained(base_model, "./my_lora_adapter")
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# inputs = tokenizer("问：你好\\n答：", return_tensors="pt")
# outputs = model.generate(**inputs, max_new_tokens=50)
# print(tokenizer.decode(outputs[0]))
"""

print(FINETUNE_CODE)

# ============ 10.4 模拟微调效果 ============
print("\n=== 10.4 模拟微调效果 ===")

class MockFineTune:
    """模拟微调前后的效果对比"""

    def __init__(self):
        self.base_knowledge = [
            "Transformer是2017年提出的模型架构",
            "BERT使用MLM进行预训练",
        ]
        self.finetuned_knowledge = [
            "Transformer是2017年提出的模型架构",
            "BERT使用MLM进行预训练",
            "本公司2024年Q3营收50亿元，同比增长20%",
            "我们的产品支持100+国家的支付方式",
        ]

    def before_finetune(self, question):
        base = "\n".join(self.base_knowledge)
        if "公司" in question or "产品" in question:
            return "抱歉，我无法回答关于特定公司的问题"
        return f"基于通用知识:\n{base}"

    def after_finetune(self, question):
        all_knowledge = "\n".join(self.finetuned_knowledge)
        return f"基于领域知识:\n{all_knowledge}"

mt = MockFineTune()
print("微调前:")
print(f"  Q: 介绍一下贵公司的业绩")
print(f"  A: {mt.before_finetune('贵公司业绩')}")

print("\n微调后（注入领域知识）:")
print(f"  Q: 介绍一下贵公司的业绩")
print(f"  A: {mt.after_finetune('业绩')}")

print("\n✅ 阶段10完成！")
