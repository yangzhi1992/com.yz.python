"""
阶段11：私有化本地部署
======================
学习内容:
  1. Ollama 本地部署
  2. vLLM 高性能推理
  3. Docker 部署
  4. FastAPI 封装 API
  5. 部署架构设计
"""

# ============ 11.1 Ollama 本地部署 ============
print("=== 11.1 Ollama 本地部署 ===")

OLLAMA_GUIDE = """
📦 Ollama 本地部署

# 1. 安装 Ollama
   Windows: https://ollama.com/download 下载安装包
   Linux:   curl -fsSL https://ollama.com/install.sh | sh

# 2. 下载模型
   ollama pull qwen2:7b        # 阿里通义千问 7B
   ollama pull llama3.1:8b     # Meta Llama 3.1
   ollama pull deepseek-r1:7b  # DeepSeek R1

# 3. 启动服务（默认端口 11434）
   ollama serve

# 4. 调用 API
   curl http://localhost:11434/api/chat -d '{
     "model": "qwen2:7b",
     "messages": [{"role":"user","content":"你好"}]
   }'

# 5. 常用管理命令
   ollama list              # 查看已下载模型
   ollama rm model_name     # 删除模型
   ollama pull model_name   # 下载模型
"""
print(OLLAMA_GUIDE)

# ============ 11.2 FastAPI 封装 ============
print("\n=== 11.2 FastAPI 封装 ===")

FASTAPI_CODE = """
📝 FastAPI 封装 LLM API 示例

# app.py
from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI(title="本地 LLM API")

class ChatRequest(BaseModel):
    message: str
    model: str = "qwen2:7b"

class ChatResponse(BaseModel):
    reply: str
    model: str

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    resp = requests.post("http://localhost:11434/api/chat", json={
        "model": req.model,
        "stream": False,
        "messages": [{"role": "user", "content": req.message}],
    })
    reply = resp.json()["message"]["content"]
    return ChatResponse(reply=reply, model=req.model)

@app.get("/health")
async def health():
    return {"status": "ok", "models": get_models()}

# 启动: uvicorn app:app --host 0.0.0.0 --port 8000
# 访问: curl http://localhost:8000/chat -d '{"message":"你好"}'
"""
print(FASTAPI_CODE)

# ============ 11.3 Docker 部署 ============
print("\n=== 11.3 Docker 部署 ===")

DOCKER_GUIDE = """
🐳 Docker 部署方案

# Dockerfile
FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime
RUN pip install fastapi uvicorn requests transformers
COPY app.py /app/app.py
WORKDIR /app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

# docker-compose.yml
version: '3.8'
services:
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

  api:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - ollama
    environment:
      - OLLAMA_HOST=http://ollama:11434

volumes:
  ollama_data:
"""
print(DOCKER_GUIDE)

# ============ 11.4 部署架构对比 ============
print("\n=== 11.4 部署架构对比 ===")

ARCH_COMPARISON = """
📊 部署方案对比

方案           硬件要求         吞吐量    延迟    适用场景
──────────────────────────────────────────────────────────
Ollama        1×GPU 6GB+        ~20 t/s   ~1s    个人/小团队
vLLM          1×GPU 24GB+       ~100 t/s  ~0.3s  生产环境
TGI           1×GPU 24GB+       ~80 t/s   ~0.4s   HuggingFace生态
TensorRT-LLM  1×GPU 80GB+       ~500 t/s  ~0.1s  极致性能

企业部署推荐:
  • 小规模 (<100 QPS): Ollama + FastAPI
  • 中规模 (<1000 QPS): vLLM + Kubernetes
  • 大规模 (>1000 QPS): TensorRT-LLM + 负载均衡

硬件选型:
  • 7B 模型: RTX 4090 (24GB) 足够
  • 13B 模型: A100 (40/80GB) 或 2×4090
  • 70B 模型: A100×4 或 H100
  • QLoRA 量化后: 70B→单卡24GB
"""
print(ARCH_COMPARISON)

# ============ 11.5 vLLM 部署 ============
print("\n=== 11.5 vLLM 高性能推理 ===")

VLLM_GUIDE = """
⚡ vLLM 部署

# 安装
pip install vllm

# 命令行启动服务
python -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen2-7B-Instruct \
    --port 8000 \
    --tensor-parallel-size 1 \
    --gpu-memory-utilization 0.9

# 调用（兼容 OpenAI 格式）
curl http://localhost:8000/v1/chat/completions -d '{
    "model": "Qwen/Qwen2-7B-Instruct",
    "messages": [{"role":"user","content":"你好"}]
}'

# 吞吐量对比（单卡 A100）
# Ollama:   ~20 tokens/s
# vLLM:     ~100 tokens/s  (5x)
# 核心优化：PagedAttention + 连续批处理
"""
print(VLLM_GUIDE)

print("\n✅ 阶段11完成！")
