"""
模块4：Tokenizer 分词器
========================
作用：将文本切分为 token，是模型输入/输出的接口

文件格式: tokenizer.model / vocab.json
路径示例: models/tokenizer/
"""

# ============ 4.1 学习路线 ============
print("=" * 60)
print("📚 Tokenizer 分词器 - 学习路线")
print("=" * 60)

LEARNING_ROADMAP = """
【阶段1】Tokenization 基础
  ├── 为什么需要 Tokenizer？
  │   └── 模型只能处理数字，不能处理文字
  ├── 字符级 (Character)
  │   └── 每个字符一个 token
  ├── 单词级 (Word)
  │   └── 每个单词一个 token (I, am, a, student)
  └── 子词级 (Subword) ← 主流
      └── 兼顾词汇量和OOV问题

【阶段2】主流 Tokenizer 算法
  ├── BPE (Byte Pair Encoding)
  │   ├── GPT, Llama, BERT 使用
  │   └── 从字符开始，逐步合并高频对
  ├── WordPiece
  │   ├── BERT 使用
  │   └── 基于概率而非频率合并
  ├── Unigram
  │   ├── T5, XLNet 使用
  │   └── 从大词汇表开始逐步剪枝
  └── SentencePiece
      ├── Llama, Gemma 使用
      └── 直接处理原始文本（不依赖空格）

【阶段3】Tokenizer 关键指标
  ├── 词汇表大小 (vocab_size)
  │   └── BERT: 30k, GPT: 50k, Llama: 32k, Qwen: 152k
  ├── 压缩率 (chars/token)
  │   └── 中文: 约1.5 chars/token，英文: 约3.5 chars/token
  ├── 特殊 Token
  │   └── [CLS], [SEP], [PAD], [MASK], <s>, </s>
  └── 最大长度限制
      └── BERT: 512, GPT: 2048, Llama: 4096, Qwen: 32768

【阶段4】实战
  ├── 使用 HF Tokenizer
  ├── 自定义 Tokenizer 训练
  ├── 添加特殊 Token
  └── Tokenizer 测试与评估
"""
print(LEARNING_ROADMAP)

# ============ 4.2 从零实现 BPE ============
print("\n" + "=" * 60)
print("🔧 Demo: 从零实现 BPE 分词器")
print("=" * 60)

from collections import Counter
import re

class BPE:
    """从零实现 BPE (Byte Pair Encoding)"""

    def __init__(self, vocab_size=300):
        self.vocab_size = vocab_size
        self.vocab = {}
        self.merges = {}  # pair → new_token

    def _get_stats(self, words):
        """统计相邻 token 对的出现频率"""
        pairs = Counter()
        for word, freq in words.items():
            symbols = word.split()
            for i in range(len(symbols)-1):
                pairs[(symbols[i], symbols[i+1])] += freq
        return pairs

    def _merge_vocab(self, pair, words):
        """合并最频繁的 token 对"""
        new_word = " ".join(pair)
        pattern = re.compile(r'(?<!\S)' + re.escape(" ".join(pair)) + r'(?!\S)')
        new_words = {}
        for word, freq in words.items():
            new_word_str = pattern.sub(new_word.replace(" ", ""), word)
            new_words[new_word_str] = freq
        return new_words

    def train(self, texts):
        """训练 BPE 分词器"""
        # 1. 初始词汇：字符级别
        words = Counter()
        for text in texts:
            word = " ".join(list(text)) + " </w>"
            words[word] += 1

        self.vocab = set()
        for word in words:
            for token in word.split():
                self.vocab.add(token)

        # 2. 迭代合并
        num_merges = self.vocab_size - len(self.vocab)
        print(f"初始词汇: {len(self.vocab)} tokens, 计划合并 {num_merges} 次")

        for i in range(num_merges):
            pairs = self._get_stats(words)
            if not pairs:
                break
            best = pairs.most_common(1)[0][0]
            self.merges[best] = "".join(best)
            words = self._merge_vocab(best, words)
            self.vocab.add("".join(best))

            if i % 1000 == 0:
                print(f"  合并 {i}: '{best[0]}+{best[1]}' → '{''.join(best)}'")

        print(f"最终词汇: {len(self.vocab)} tokens")

    def encode(self, text):
        """编码：文本 → token IDs"""
        tokens = list(text) + ["</w>"]
        while len(tokens) > 1:
            pairs = [(tokens[i], tokens[i+1]) for i in range(len(tokens)-1)]
            # 找到优先级最高的 pair（最早合并的）
            min_pair = None
            min_idx = float('inf')
            for pair in pairs:
                if pair in self.merges:
                    idx = list(self.merges.keys()).index(pair)
                    if idx < min_idx:
                        min_idx = idx
                        min_pair = pair
            if min_pair is None:
                break
            merged = self.merges[min_pair]
            i = 0
            new_tokens = []
            while i < len(tokens):
                if i < len(tokens)-1 and (tokens[i], tokens[i+1]) == min_pair:
                    new_tokens.append(merged)
                    i += 2
                else:
                    new_tokens.append(tokens[i])
                    i += 1
            tokens = new_tokens
        return tokens[:-1]  # 去掉 </w>

# 测试 BPE
print("\n🧪 训练 BPE:")
bpe = BPE(vocab_size=50)
bpe.train(["low lower lowest", "new newer newest", "big bigger biggest"])

print("\n编码测试:")
for word in ["low", "lower", "lowest", "new", "newer"]:
    tokens = bpe.encode(word)
    print(f"  '{word}' → {tokens}")

# ============ 4.3 使用 HuggingFace Tokenizer ============
print("\n" + "=" * 60)
print("🔧 Demo: 使用 HuggingFace Tokenizer")
print("=" * 60)

HF_TOKENIZER_GUIDE = """
# 安装: pip install transformers

from transformers import AutoTokenizer

## 1. 加载 Tokenizer
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2-7B-Instruct")
# 或: tokenizer = AutoTokenizer.from_pretrained("bert-base-chinese")

## 2. 编码 (文本 → token IDs)
text = "大模型基于Transformer架构"
tokens = tokenizer(text)
print(tokens)
# {'input_ids': [151644, 8948, 1707, ...], 'attention_mask': [1, 1, ...]}

## 3. 解码 (token IDs → 文本)
ids = tokens["input_ids"]
decoded = tokenizer.decode(ids)
print(decoded)

## 4. 查看分词结果
tokens = tokenizer.tokenize(text)
print(tokens)
# 中文: 每个字约1个token
# 英文: 常见词1个, 长词拆分为多个

## 5. 控制参数
tokens = tokenizer(
    text,
    max_length=512,
    truncation=True,        # 超长截断
    padding=True,           # 填充到等长
    return_tensors="pt",    # 返回 PyTorch 张量
)

## 6. 特殊 Token
print(f"pad_token:  {tokenizer.pad_token}")
print(f"eos_token:  {tokenizer.eos_token}")
print(f"bos_token:  {tokenizer.bos_token}")
print(f"unk_token:  {tokenizer.unk_token}")

## 7. 词汇表大小
print(f"vocab_size: {tokenizer.vocab_size}")
"""

print(HF_TOKENIZER_GUIDE)

# ============ 4.4 Tokenizer 对比 ============
print("\n" + "=" * 60)
print("🔧 Demo: 主流 Tokenizer 对比")
print("=" * 60)

COMPARISON = """
各模型 Tokenizer 特点:

模型         算法         词汇量   中文支持   特殊 Token
───────────────────────────────────────────────────────────
BERT         WordPiece    30,522   ✅        [CLS][SEP][MASK]
GPT-2        BPE          50,257   ❌        <|endoftext|>
Llama 2      BPE (SP)     32,000   ⚠️ 差     <s></s>
Llama 3      BPE (tiktoken) 128,000 ✅ 好     <|begin_of_text|>
Qwen2        BPE (tiktoken) 151,936 ✅ 好     <|im_start|><|im_end|>
ChatGLM3     SentencePiece 65,024  ✅ 好     [MASK][gMASK]
DeepSeek     BPE (SP)     102,400  ✅ 好     <｜begin▁of▁sentence｜>
Baichuan2    BPE (SP)     125,696  ✅ 好     <reserved_106>

关键指标：
  • 中文压缩率 (chars/token):
    BERT: ~1.5, Llama2: ~1.3, Qwen2: ~1.8, DeepSeek: ~2.0
  • 句子 "大模型改变了人工智能世界" 的 token 数:
    Llama2: 12 tokens, Qwen2: 9 tokens, DeepSeek: 8 tokens
  • 中文场景优先选择: Qwen2 / DeepSeek / ChatGLM3 的 Tokenizer

Token 数量预估:
  • 1000中文字 ≈ 650 tokens (Qwen2)
  • 1000英文字 ≈ 300 tokens (GPT)
  • 1 token ≈ 0.75 个中文 ≈ 3.5 个英文字母
"""
print(COMPARISON)

# ============ 4.5 Token 计数 ============
print("\n" + "=" * 60)
print("🔧 Demo: Token 计数与成本估算")
print("=" * 60)

def estimate_tokens(text, is_chinese=True):
    """估算文本的 token 数量"""
    if is_chinese:
        ratio = 1.5  # 中文 chars/token
    else:
        ratio = 3.5  # 英文 chars/token
    return int(len(text) / ratio)

def estimate_cost(input_tokens, output_tokens, model="qwen2:7b"):
    """估算 API 调用成本"""
    rates = {
        "qwen2:7b":    (0.5, 1.5),    # 输入/输出 元/百万tokens
        "gpt-4o":      (25, 100),
        "deepseek-v2": (1.0, 2.0),
    }
    in_rate, out_rate = rates.get(model, (1.0, 1.0))
    cost = (input_tokens * in_rate + output_tokens * out_rate) / 1_000_000
    return cost

# 测试
texts = [
    "大模型改变了人工智能世界" * 100,
    "大模型改变了人工智能世界" * 1000,
]
for text in texts:
    tokens = estimate_tokens(text)
    cost = estimate_cost(tokens, 100)
    print(f"  文本: {len(text)} 字 → ~{tokens} tokens → 约 ¥{cost:.4f}")

print("\n✅ Tokenizer模块完成！")
