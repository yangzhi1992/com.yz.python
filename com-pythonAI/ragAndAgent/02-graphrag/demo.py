"""
02-graphrag: GraphRAG 知识图谱增强检索
========================================
学习内容: 知识图谱构建、GraphRAG原理、社区检测、全局搜索
"""

print("=" * 60)
print("📚 GraphRAG - 学习路线")
print("=" * 60)

LEARNING = """
【阶段1】知识图谱基础
  ├── 三元组: (实体, 关系, 实体)
  │   └── (北京, 是首都, 中国)
  ├── 图谱 vs 向量: 结构关系 vs 语义相似
  └── 构建方式: 人工标注 / NLP 提取 / LLM 生成

【阶段2】GraphRAG 原理 (微软 2024)
  ┌─────────────────────────────────────────────┐
  │ GraphRAG vs 传统 RAG                        │
  │                                             │
  │ 传统 RAG:                                    │
  │   文档→分块→向量→检索(局部相似)              │
  │   ❌ 无法回答全局性问题                      │
  │   ❌ 无法理解实体间关系                      │
  │                                             │
  │ GraphRAG:                                    │
  │   文档→实体提取→图谱构建→社区检测→全局摘要   │
  │   ✅ 全局理解                               │
  │   ✅ 关系推理                               │
  └─────────────────────────────────────────────┘

【阶段3】GraphRAG 流程
  1. 文档 → LLM 提取实体和关系
  2. 构建知识图谱 (Neo4j / NetworkX)
  3. 社区检测 (Leiden / Louvain)
  4. 为每个社区生成摘要
  5. 回答时: 局部搜索 + 全局搜索 融合

【阶段4】主流方案
  ├── Microsoft GraphRAG (Python)
  ├── LightRAG (轻量级GraphRAG)
  ├── Neo4j + LLM (企业级)
  └── NebulaGraph + LLM
"""
print(LEARNING)

# ============ 从零实现 GraphRAG ============
print("\n" + "=" * 60)
print("🔧 Demo: 从零实现简易 GraphRAG")
print("=" * 60)

import json
import numpy as np
from collections import defaultdict

class SimpleGraphRAG:
    """简易 GraphRAG 实现"""

    def __init__(self):
        self.entities = {}       # entity_id → {name, type, desc}
        self.relations = []      # [(head, rel, tail)]
        self.communities = []    # [{entities: [], summary: ""}]
        self.graph = defaultdict(list)  # entity → [neighbors]

    def extract_from_text(self, text):
        """模拟 LLM 从文本提取实体和关系"""
        # 模拟提取结果
        entities = {
            "Transformer": {"type": "模型架构", "desc": "2017年提出的深度学习架构"},
            "Attention": {"type": "机制", "desc": "自注意力机制是Transformer的核心"},
            "BERT": {"type": "模型", "desc": "基于Transformer的预训练模型"},
            "GPT": {"type": "模型", "desc": "基于Transformer的自回归模型"},
            "RAG": {"type": "技术", "desc": "检索增强生成"},
        }
        relations = [
            ("Transformer", "包含", "Attention"),
            ("BERT", "基于", "Transformer"),
            ("GPT", "基于", "Transformer"),
            ("RAG", "使用", "Transformer"),
        ]
        return entities, relations

    def build_graph(self, text):
        """构建知识图谱"""
        entities, relations = self.extract_from_text(text)
        self.entities = entities
        self.relations = relations

        for h, r, t in relations:
            self.graph[h].append((r, t))
            self.graph[t].append((f"被{r}", h))

        print(f"  实体: {len(entities)}个")
        print(f"  关系: {len(relations)}条")

    def detect_communities(self):
        """模拟社区检测 (Leiden算法简化版)"""
        # 基于关系的紧密程度分组
        visited = set()
        communities = []

        for entity in self.entities:
            if entity not in visited:
                community = {entity}
                # BFS 找邻居
                queue = [entity]
                while queue:
                    current = queue.pop(0)
                    for _, neighbor in self.graph[current]:
                        if neighbor not in visited and neighbor in self.entities:
                            visited.add(neighbor)
                            community.add(neighbor)
                            queue.append(neighbor)
                visited.add(entity)
                communities.append(list(community))

        self.communities = communities
        print(f"  检测到 {len(communities)} 个社区:")
        for i, c in enumerate(communities):
            print(f"    社区{i+1}: {', '.join(c)}")
        return communities

    def global_search(self, query):
        """全局搜索: 基于社区摘要回答"""
        summaries = []
        for i, community in enumerate(self.communities):
            # 生成社区摘要
            entities_desc = [f"{e}({self.entities[e]['desc']})" for e in community]
            summary = f"社区{i+1}包含: {', '.join(entities_desc)}"
            summaries.append(summary)

        return f"[GraphRAG全局搜索]\n  查询: {query}\n  社区摘要:\n" + "\n".join(f"    {s}" for s in summaries)

    def local_search(self, query, target_entity):
        """局部搜索: 基于实体关系链回答"""
        if target_entity not in self.graph:
            return f"未找到实体: {target_entity}"

        relations = self.graph[target_entity]
        rel_str = "\n".join(f"    {target_entity} {r[0]} {r[1]}" for r in relations)
        return f"[GraphRAG局部搜索]\n  查询: {query}\n  实体关系:\n{rel_str}"

# ============ 测试 ============
print("\n🧪 测试 GraphRAG:")
gr = SimpleGraphRAG()
gr.build_graph("Transformer包含Attention机制，BERT和GPT都基于Transformer，RAG使用Transformer")
gr.detect_communities()

print(f"\n{gr.global_search('Transformer相关的技术有哪些')}")
print(f"\n{gr.local_search('BERT基于什么架构', 'BERT')}")

# ============ GraphRAG vs 传统 RAG ============
print("\n" + "=" * 60)
print("🔧 Demo: GraphRAG vs 传统 RAG 对比")
print("=" * 60)

COMPARISON = """
┌───────────────────┬────────────────────────┬────────────────────────┐
│     维度          │    传统 RAG             │    GraphRAG            │
├───────────────────┼────────────────────────┼────────────────────────┤
│ 数据结构           │ 向量 (无结构)          │ 图 (三元组)            │
│ 检索粒度           │ 文本块                 │ 实体 + 关系链          │
│ 局部问题           │ ✅ 好                  │ ✅ 好                  │
│ 全局问题           │ ❌ 差                  │ ✅ 好 (社区摘要)       │
│ 关系推理           │ ❌ 不支持              │ ✅ 支持                │
│ 构建成本           │ 低 (一次性计算)        │ 高 (LLM提取)           │
│ 更新难度           │ 易 (追加)              │ 难 (图谱重构)          │
│ 适用场景           │ 问答、搜索              │ 分析、报告、推理       │
│ 代表方案           │ ChromaDB + BGE         │ Microsoft GraphRAG     │
└───────────────────┴────────────────────────┴────────────────────────┘

选择建议:
  • 简单问答 → 传统 RAG
  • 需要关系推理 → GraphRAG
  • 高频更新 → 传统 RAG
  • 多文档综合分析 → GraphRAG
  • 两者结合 → 混合 RAG (向量 + 图谱)
"""
print(COMPARISON)

print("\n✅ GraphRAG 完成！")
