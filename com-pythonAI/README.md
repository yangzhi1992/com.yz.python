# Python AI 大模型学习路线

## 📋 学习路线总览

```
阶段1  Python编程基础       ████████░░░░  基础
阶段2  算法基础              ████████░░░░  基础
阶段3  深度学习基础(PyTorch) ████████░░░░  基础
阶段4  Transformer核心原理   ██████████░░  模型架构
阶段5  提示词工程(Prompt)     ██████████░░  应用入门
阶段6  RAG检索增强生成       ██████████░░  RAG
阶段7  LangChain开发框架      ██████████░░  开发框架
阶段8  LangGraph工作流编排    ██████████░░  工作流
阶段9  Agent智能体开发        ██████████░░  智能体
阶段10 模型微调(LoRA/QLoRA)  ██████████░░  模型优化
阶段11 私有化本地部署         ██████████░░  部署
阶段12 模型量化推理优化       ██████████░░  推理优化
阶段13 多Agent多智能体系统    ██████████░░  进阶
阶段14 多模态大模型开发       ██████████░░  前沿
```

## 📁 目录结构

```
com-pythonAI/
├── README.md                    ← 本文件
├── docs/                        ← 学习文档
│   └── learning-plan.md         ← 详细学习计划
├── phase01-python-basics/       ← Python基础
├── phase02-algorithms/          ← 算法基础
├── phase03-pytorch/             ← PyTorch深度学习
├── phase04-transformer/         ← Transformer原理
├── phase05-prompt/              ← 提示词工程
├── phase06-rag/                 ← RAG检索增强
├── phase07-langchain/           ← LangChain框架
├── phase08-langgraph/           ← LangGraph工作流
├── phase09-agent/               ← Agent智能体
├── phase10-finetune/            ← 模型微调
├── phase11-deploy/              ← 本地部署
├── phase12-quantization/        ← 模型量化
├── phase13-multi-agent/         ← 多Agent系统
└── phase14-multimodal/          ← 多模态开发
```

## 🚀 快速开始

```bash
# 1. 创建虚拟环境
cd com-pythonAI
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. 安装依赖
pip install torch transformers datasets accelerate
pip install langchain langchain-community chromadb
pip install requests numpy pandas matplotlib
pip install openai ollama

# 3. 从阶段1开始逐步学习
cd phase01-python-basics && python hello.py
```
