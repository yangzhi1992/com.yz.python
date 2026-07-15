# Python AI 大模型学习 - 详细学习计划

> 14 个阶段，从零基础到大模型应用开发全栈

---

## 📅 学习时间规划（建议）

| 阶段 | 内容 | 建议时间 | 前置要求 |
|------|------|---------|---------|
| 1 | Python编程基础 | 1-2周 | 无 |
| 2 | 算法基础 | 1-2周 | 阶段1 |
| 3 | PyTorch深度学习 | 2-3周 | 阶段1-2 |
| 4 | Transformer原理 | 2周 | 阶段3 |
| 5 | 提示词工程 | 1周 | 无 |
| 6 | RAG检索增强 | 1-2周 | 阶段4-5 |
| 7 | LangChain框架 | 2周 | 阶段5-6 |
| 8 | LangGraph工作流 | 1周 | 阶段7 |
| 9 | Agent智能体 | 2周 | 阶段7-8 |
| 10 | 模型微调 | 2-3周 | 阶段3-4 |
| 11 | 本地部署 | 1周 | 阶段10 |
| 12 | 量化推理 | 1周 | 阶段11 |
| 13 | 多Agent系统 | 1-2周 | 阶段9 |
| 14 | 多模态 | 2周 | 阶段3-4 |

**总耗时：约 20-26 周（5-6个月）**

---

## 📚 每个阶段具体学习内容

### 阶段1：Python 编程基础

**目标：** 掌握 Python 语法、面向对象、函数式编程

| 学习项 | 具体内容 | 练习 |
|--------|---------|------|
| 基础语法 | 变量、类型、运算符、控制流 | 写计算器、猜数字 |
| 数据结构 | list/dict/set/tuple | 通讯录管理 |
| 函数 | 参数、作用域、lambda、装饰器 | 计时装饰器 |
| 面向对象 | 类、继承、多态、魔法方法 | 实现 Stack 类 |
| 文件IO | 读写文件、with 语句 | 日志分析器 |
| 模块 | import、包管理、pip | 发布自己的包 |
| 进阶 | 生成器、上下文管理器、闭包 | 实现迭代器 |

**参考书：** 《Python编程：从入门到实践》《流畅的Python》

---

### 阶段2：算法基础

**目标：** 掌握常用数据结构和算法，能通过算法面试

| 学习项 | 具体内容 | LeetCode 题 |
|--------|---------|-----------|
| 复杂度 | 大O表示法、时间/空间 | - |
| 排序 | 快排、归并、堆排 | 912 |
| 二分 | 二分查找、二分答案 | 704, 34 |
| 哈希表 | 两数之和、三数之和 | 1, 15, 49 |
| 链表 | 反转、合并、环形 | 206, 21, 141 |
| 栈/队列 | 最小栈、单调栈 | 155, 739 |
| 树 | 遍历、二叉搜索树 | 94, 230, 102 |
| 图 | BFS、DFS、拓扑排序 | 200, 207, 994 |
| 动态规划 | 背包、最长子序列 | 300, 1143, 322 |
| 贪心 | 区间调度 | 435, 452 |

**重点：** 哈希表、二叉树遍历、BFS/DFS、基础DP

---

### 阶段3：深度学习基础（PyTorch）

**目标：** 掌握 PyTorch 框架，理解深度学习基础

| 学习项 | 具体内容 | 代码练习 |
|--------|---------|---------|
| 张量 | 创建、索引、广播、设备 | 各种张量操作 |
| Autograd | 计算图、backward() | 手动求导验证 |
| 线性回归 | nn.Linear + MSELoss + SGD | 拟合 y=2x+1 |
| 逻辑回归 | nn.Sigmoid + BCELoss | 二分类 |
| MLP | 激活函数、Dropout | MNIST 手写识别 |
| CNN | Conv2d、Pooling、Flatten | CIFAR-10 分类 |
| 训练流程 | DataLoader、优化器、评估 | 完整训练脚本 |
| GPU训练 | .cuda()、AMP混合精度 | 提速对比 |

---

### 阶段4：Transformer 原理

**目标：** 理解 Transformer 架构核心，能手动实现

| 学习项 | 具体内容 |
|--------|---------|
| 自注意力 | QKV 计算、缩放点积、softmax |
| 多头注意力 | 8头并行、拼接、投影 |
| 位置编码 | 正余弦 PE、RoPE |
| Encoder块 | Self-Attn + FFN + LayerNorm + 残差 |
| Decoder块 | Masked Self-Attn + Cross-Attn |
| BERT | Encoder-only、MLM、NSP |
| GPT | Decoder-only、自回归生成 |
| 最新架构 | RMSNorm、GQA、SwiGLU、RoPE |

---

### 阶段5：提示词工程

**目标：** 掌握与大模型高效交互的技能

| 学习项 | 具体内容 |
|--------|---------|
| 角色设定 | system prompt 设计 |
| Few-Shot | 示例引导（1-shot/3-shot/5-shot） |
| CoT思维链 | 一步一步思考、数学推理 |
| Prompt模板 | 结构化模板设计 |
| 参数调优 | temperature、top_p、max_tokens |
| 约束控制 | 输出格式、长度、风格 |
| 安全防护 | 提示注入防护、边界设定 |
| API调用 | Ollama / OpenAI / 流式输出 |

---

### 阶段6：RAG 检索增强生成

**目标：** 独立搭建 RAG 问答系统

| 学习项 | 具体内容 |
|--------|---------|
| 文档加载 | TextLoader、PDFLoader、WebLoader |
| 文本分割 | RecursiveCharacter、按语义分割 |
| Embedding | BGE、text2vec-large-chinese |
| 向量库 | ChromaDB、FAISS、PGVector |
| 相似度搜索 | 余弦相似度、L2距离 |
| 检索策略 | Top-K、MMR、混合检索 |
| 增强生成 | Context注入、Prompt模板 |
| 引用溯源 | 标注来源、相似度分数 |
| 高级RAG | RAPTOR、HyDE、Self-RAG |

---

### 阶段7：LangChain 开发框架

**目标：** 熟练使用 LangChain 构建 LLM 应用

| 学习项 | 具体内容 |
|--------|---------|
| ChatModel | Ollama、OpenAI、Claude 封装 |
| PromptTemplate | 模板、部分变量、少样本 |
| OutputParser | Str、Json、List、Pydantic |
| Chain | LCEL 表达式、管道操作符 |
| DocumentLoader | 各种格式文档加载 |
| TextSplitter | 多种分割策略 |
| VectorStore | ChromaDB集成 |
| RetrievalQA | 问答链 |
| Memory | ConversationBufferMemory |
| Callback | 日志、监控、调试 |

---

### 阶段8：LangGraph 工作流编排

**目标：** 掌握图结构工作流的编排

| 学习项 | 具体内容 |
|--------|---------|
| StateGraph | 状态管理、节点、边 |
| Node/Edge | 节点函数、边定义 |
| 条件路由 | ConditionalEdge、路由函数 |
| 循环 | 带循环的工作流 |
| 并行 | 并行节点执行 |
| Checkpoint | 断点续传、状态持久化 |
| 应用 | 客服流程、审批流程、多步推理 |

---

### 阶段9：Agent 智能体开发

**目标：** 独立开发 Agent 应用

| 学习项 | 具体内容 |
|--------|---------|
| ReAct模式 | 思考→行动→观察循环 |
| 工具定义 | @tool装饰器、函数签名 |
| Tool注册 | 自动发现、描述生成 |
| AgentExecutor | LangChain Agent执行器 |
| Memory集成 | 对话记忆+Agent |
| Tool选择 | LLM分析→选择→调用 |
| 错误处理 | 工具异常、LLM解析失败 |
| 安全限制 | 最大迭代、敏感操作确认 |
| 实战 | 数据分析Agent、客服Agent、代码Agent |

---

### 阶段10：模型微调（LoRA/QLoRA）

**目标：** 掌握高效微调技术，能微调自己的模型

| 学习项 | 具体内容 |
|--------|---------|
| 微调概念 | 全量 vs 参数高效 |
| LoRA原理 | 低秩分解、rank选择 |
| QLoRA | 4bit量化+LoRA |
| PEFT库 | LoraConfig、get_peft_model |
| 数据准备 | Alpaca格式、ShareGPT格式 |
| 训练参数 | learning_rate、batch_size、warmup |
| DeepSpeed | ZeRO优化、分布式训练 |
| 评估 | 微调前后效果对比 |
| 部署 | LoRA权重合并、单独部署 |

---

### 阶段11：私有化本地部署

**目标：** 能独立部署 LLM 到生产环境

| 学习项 | 具体内容 |
|--------|---------|
| Ollama | 安装、模型管理、API使用 |
| vLLM | 高性能推理、PagedAttention |
| FastAPI | 封装API、文档、健康检查 |
| Docker | 镜像构建、Compose编排 |
| 负载均衡 | Nginx反向代理 |
| GPU配置 | CUDA、device_map、多卡 |
| 监控 | 日志、指标、告警 |
| 安全 | API鉴权、速率限制 |

---

### 阶段12：模型量化推理优化

**目标：** 掌握模型压缩和推理加速技术

| 学习项 | 具体内容 |
|--------|---------|
| 量化原理 | FP16/INT8/INT4 |
| GGUF格式 | llama.cpp、Ollama量化 |
| GPTQ | 基于Hessian的量化 |
| AWQ | 基于激活值的量化 |
| bitsandbytes | 4bit NormalFloat |
| FlashAttention | 高效注意力计算 |
| 连续批处理 | vLLM的批处理策略 |
| Speculative Decoding | 投机解码 |
| KV Cache | Prefix Caching |

---

### 阶段13：多Agent 系统

**目标：** 开发多角色协作的复杂 AI 系统

| 学习项 | 具体内容 |
|--------|---------|
| 架构模式 | Manager-Worker、Debate、Pipeline |
| 角色分工 | 角色定义、专业领域 |
| 通信机制 | 消息传递、共享状态 |
| 任务分解 | 大任务拆解、依赖管理 |
| CrewAI框架 | Agent/Task/Crew |
| AutoGen | 微软多Agent框架 |
| 实战 | 软件开发Agent团队、研究Agent团队 |

---

### 阶段14：多模态大模型

**目标：** 理解多模态原理，能调用多模态模型

| 学习项 | 具体内容 |
|--------|---------|
| CLIP | 图文对比学习、零样本分类 |
| LLaVA | 视觉语言模型、图片理解 |
| Stable Diffusion | 文生图、ControlNet |
| Whisper | 语音转文字 |
| TTS | 文字转语音 |
| 多模态RAG | 图文联合检索 |
| 工具链 | ComfyUI、Diffusers、Transformers |

---

## 🎯 学习建议

### 按阶段策略

- **阶段1-4**（基础）：逐行理解代码，打牢基础
- **阶段5-6**（应用入门）：动手搭建小项目（RAG问答系统）
- **阶段7-9**（框架+Agent）：结合LangChain做综合项目
- **阶段10-12**（优化部署）：在自己机器上实操
- **阶段13-14**（进阶）：了解前沿方向，按兴趣深入

### 学习资源

| 类型 | 资源 |
|------|------|
| 课程 | 吴恩达《CS224N》、李沐《动手学深度学习》 |
| 书 | 《深度学习》花书、《Attention Is All You Need》 |
| 框架 | PyTorch官方教程、LangChain文档 |
| 实战 | HuggingFace Course、Kaggle竞赛 |

### 项目练习路线

```
初学者项目:
  RAG问答系统 (阶段6) → Agent工具助手 (阶段9) → 聊天机器人部署 (阶段11)

进阶项目:
  多Agent协作系统 (阶段13) → 图文识别助手 (阶段14) → 领域模型微调 (阶段10)
```
