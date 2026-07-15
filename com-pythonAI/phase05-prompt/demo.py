"""
阶段5：提示词工程（Prompt Engineering）
=======================================
学习内容:
  1. Prompt 设计原则
  2. Few-Shot 示例学习
  3. Chain-of-Thought (CoT) 思维链
  4. 结构化 Prompt 模板
  5. 调用 Ollama/OpenAI API
"""

import json

# ============ 5.1 Prompt 设计原则 ============
print("=== 5.1 Prompt 设计原则 ===")

PRINCIPLES = """
📐 Prompt 设计六大原则

1. 明确角色 (Role)
   ❌ "帮我写代码"
   ✅ "你是一个资深Python工程师，帮我写一个..."

2. 具体任务 (Task)
   ❌ "分析这段文本"
   ✅ "从这段文本中提取：日期、金额、对方账户名"

3. 提供上下文 (Context)
   ❌ "翻译成英文"
   ✅ "以下是一封商务邮件，请翻译成正式的商务英文"

4. 限定格式 (Format)
   ❌ "列出要点"
   ✅ "以JSON格式返回：[{\"key\": \"value\"}]"

5. 示例引导 (Example)
   ❌ "帮我分类"
   ✅ "示例：'今天心情很好' → 正面\n请分类：'...'"

6. 约束条件 (Constraint)
   ❌ "写一个总结"
   ✅ "用100字以内总结，不要添加原文没有的信息"
"""
print(PRINCIPLES)

# ============ 5.2 Few-Shot 示例 ============
print("=== 5.2 Few-Shot 示例 ===")

few_shot_prompt = """
你是一个文本分类器，将用户评论分类为：正面 / 负面 / 中性

示例1：
  评论：这个产品质量非常好，推荐购买！
  分类：正面

示例2：
  评论：发货太慢了，等了一周都没到
  分类：负面

示例3：
  评论：一般般吧，凑合用
  分类：中性

--- 现在分类以下评论 ---

评论：客服态度很好，问题很快解决了
分类："""

print(f"Few-Shot Prompt:\n{few_shot_prompt}")
print("→ 期望输出: 正面\n")

# ============ 5.3 CoT 思维链 ============
print("=== 5.3 Chain-of-Thought (CoT) 思维链 ===")

cot_prompt = """
问题：小明有10个苹果，给了小红3个，又买了5个，然后吃掉了2个，还剩几个？

让我们一步一步思考：
1. 开始有10个苹果
2. 给小红3个: 10 - 3 = 7
3. 又买了5个: 7 + 5 = 12
4. 吃掉2个: 12 - 2 = 10
答案：10

--- 现在解决以下问题 ---

问题：一个长方形的长是8米，宽是5米，如果长增加2米，面积增加多少平方米？
"""
print(f"CoT Prompt:\n{cot_prompt}")
print("→ 期望: 长8×宽5=40㎡, 长10×宽5=50㎡, 增加10㎡\n")

# ============ 5.4 结构化 Prompt 模板 ============
print("=== 5.4 结构化 Prompt 模板 ===")

class PromptTemplate:
    """结构化 Prompt 模板"""

    @staticmethod
    def analysis(text, aspects):
        return f"""请分析以下文本：

文本: {text}

请从以下维度分析（每个维度100字以内）：
{chr(10).join(f'- {a}' for a in aspects)}

以JSON格式返回：
{{
    "维度1": "分析结果",
    "维度2": "分析结果"
}}
"""

    @staticmethod
    def extract(text, fields):
        return f"""从以下文本中提取信息：

文本: {text}

提取字段：{', '.join(fields)}

以JSON格式返回，不存在的字段填null。
"""

    @staticmethod
    def summarize(text, max_words=100):
        return f"""请总结以下文本（{max_words}字以内）：

{text}

要求：
1. 保留核心信息
2. 不要添加原文没有的内容
3. 用中文回答
"""

# 测试模板
print(PromptTemplate.extract(
    "张三在2024年3月15日购买了iPhone15，花费8999元",
    ["姓名", "日期", "商品", "金额"]
))

# ============ 5.5 调用 Ollama API ============
print("\n=== 5.5 调用 LLM API（Ollama）===")

def call_ollama(prompt, model="qwen2:7b"):
    """调用本地 Ollama API"""
    import requests
    try:
        resp = requests.post("http://localhost:11434/api/chat", json={
            "model": model,
            "stream": False,
            "messages": [{"role": "user", "content": prompt}],
        }, timeout=30)
        return resp.json()["message"]["content"]
    except Exception as e:
        return f"[API不可用] {e}"

# 测试（有 Ollama 时取消注释）
# print(call_ollama("用一句话解释什么是大模型"))

def call_openai(prompt, api_key=None, model="gpt-4"):
    """调用 OpenAI API"""
    from openai import OpenAI
    try:
        client = OpenAI(api_key=api_key)
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"[API不可用] {e}"

print("""
Ollama 本地调用:
  curl http://localhost:11434/api/chat -d '{
    "model": "qwen2:7b",
    "messages": [{"role":"user","content":"你好"}]
  }'

OpenAI 云端调用:
  from openai import OpenAI
  client = OpenAI(api_key="sk-xxx")
  resp = client.chat.completions.create(
      model="gpt-4",
      messages=[{"role":"user","content":"你好"}]
  )
""")

# ============ 5.6 Prompt 优化技巧 ============
print("\n=== 5.6 Prompt 优化技巧 ===")

TIPS = """
🎯 Prompt 优化技巧

1. 用温度控制创造性
   temperature=0.0: 精确、确定性（适合提取信息）
   temperature=0.7: 平衡（适合对话）
   temperature=1.0: 创造性高（适合写作）

2. 负向提示（排除内容）
   "不要解释，直接给出答案"
   "不要使用专业术语"

3. 角色扮演增强
   "你是一个拥有20年经验的资深律师"
   "你是一个小学老师，用简单的语言解释"

4. 逐步引导
   "第一步：理解问题\n第二步：分析原因\n第三步：给出建议"

5. 输出格式约束
   "以JSON格式返回"
   "以Markdown表格输出"
   "每行不超过20个字"
"""
print(TIPS)

print("\n✅ 阶段5完成！")
