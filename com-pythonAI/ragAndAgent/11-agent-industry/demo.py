"""
11-agent-industry: 行业落地案例
=================================
学习内容: 银行CRM、智能客服、TableAgent 行业落地实战
"""

print("=" * 60)
print("📚 Agent 行业落地 - 学习路线")
print("=" * 60)

INDUSTRY_CASES = """
┌────────────────────────────────────────────────────────────┐
│              Agent 行业落地全景图                           │
├───────────────┬────────────────────────────────────────────┤
│  金融          │ 银行CRM、风控分析、投研报告、合规审查      │
│  客服          │ 智能客服、工单处理、FAQ自动回复            │
│  数据分析      │ TableAgent、BI分析、报表生成               │
│  医疗          │ 病历分析、用药推荐、影像辅助诊断           │
│  教育          │ 智能辅导、试卷批改、学习路径规划           │
│  法律          │ 合同审查、法规检索、案件分析               │
│  电商          │ 商品推荐、客户运营、价格分析               │
│  制造          │ 设备诊断、工艺优化、质量检测               │
└───────────────┴────────────────────────────────────────────┘
"""
print(INDUSTRY_CASES)

print("\n" + "=" * 60)
print("🔧 Demo: 三大行业落地案例")
print("=" * 60)

# ============ 案例1: 银行CRM ============
print("\n📌 案例1: 银行CRM Agent")
print("-" * 40)

class BankCRMAgent:
    """银行客户关系管理 Agent"""

    def get_customer_info(self, customer_id):
        data = {
            "C001": {"name": "张三", "balance": 500000, "products": ["存款", "基金"],
                     "risk_level": "中等", "last_contact": "2026-06-01"},
            "C002": {"name": "李四", "balance": 2000000, "products": ["理财", "保险"],
                     "risk_level": "高", "last_contact": "2026-05-15"},
        }
        return data.get(customer_id, {"name": "未知"})

    def analyze_needs(self, customer):
        """分析客户需求"""
        needs = []
        if customer.get("balance", 0) > 1000000:
            needs.append("私人银行服务")
        if "存款" in customer.get("products", []):
            needs.append("理财升级")
        if customer.get("last_contact", "") < "2026-06-01":
            needs.append("客户回访")
        return needs

    def recommend_product(self, customer):
        """推荐产品"""
        risk = customer.get("risk_level", "低")
        products = {
            "低": "货币基金、定期存款",
            "中等": "混合基金、指数基金",
            "高": "股票基金、私募基金",
        }
        return products.get(risk, "稳健型产品")

    def serve(self, customer_id, intent):
        customer = self.get_customer_info(customer_id)
        print(f"  客户: {customer['name']}")
        print(f"  资产: {customer['balance']:,}元")
        print(f"  持仓: {', '.join(customer['products'])}")

        if intent == "需求分析":
            needs = self.analyze_needs(customer)
            print(f"  识别需求: {needs}")
        elif intent == "产品推荐":
            rec = self.recommend_product(customer)
            print(f"  推荐产品: {rec}")
        elif intent == "综合服务":
            needs = self.analyze_needs(customer)
            rec = self.recommend_product(customer)
            print(f"  需求: {needs}")
            print(f"  推荐: {rec}")

bank = BankCRMAgent()
print("银行CRM Agent:")
bank.serve("C001", "综合服务")

# ============ 案例2: 智能客服 ============
print("\n📌 案例2: 智能客服 Agent")
print("-" * 40)

class CustomerServiceAgent:
    """智能客服 Agent"""

    def __init__(self):
        self.faq = {
            "退货": "退货流程: 1.联系客服 2.填写退货单 3.寄回商品 4.退款 (3-5工作日)",
            "退款": "退款将在收到退货后3-5个工作日原路返回",
            "物流": "快递一般3-5天送达，可登录APP查看物流信息",
            "发票": "电子发票在确认收货后7天自动发送到注册邮箱",
            "换货": "换货流程与退货类似，请在退货单备注换货需求",
        }
        self.order_db = {}

    def search_faq(self, question):
        """FAQ 匹配"""
        for keyword, answer in self.faq.items():
            if keyword in question:
                return answer
        return None

    def check_order(self, order_id):
        orders = {
            "ORD001": {"status": "已发货", "tracking": "SF1234567890"},
            "ORD002": {"status": "已签收", "time": "2026-07-08"},
        }
        return orders.get(order_id, {"status": "未找到"})

    def handle(self, user_input):
        print(f"  用户: {user_input}")

        # 1. FAQ 匹配
        answer = self.search_faq(user_input)
        if answer:
            print(f"  客服: {answer}")
            return answer

        # 2. 订单查询
        if "订单" in user_input:
            order_info = self.check_order("ORD001")
            print(f"  客服: 您的订单状态: {order_info['status']}")
            return f"订单状态: {order_info['status']}"

        # 3. 转人工
        print("  客服: 已转接人工客服，请稍候...")
        return "转人工"

print("\n智能客服 Agent:")
cs = CustomerServiceAgent()
cs.handle("我想退货怎么操作？")
cs.handle("查一下我的订单")

# ============ 案例3: TableAgent ============
print("\n📌 案例3: TableAgent (数据分析 Agent)")
print("-" * 40)

class TableAgent:
    """数据分析 Agent - 自然语言查询表格数据"""

    def __init__(self):
        self.data = [
            {"月份": "1月", "销售额": 120000, "成本": 80000, "利润": 40000},
            {"月份": "2月", "销售额": 135000, "成本": 85000, "利润": 50000},
            {"月份": "3月", "销售额": 110000, "成本": 75000, "利润": 35000},
            {"月份": "4月", "销售额": 150000, "成本": 90000, "利润": 60000},
        ]

    def query(self, question):
        """自然语言 → SQL → 执行 → 回答"""
        print(f"  问题: {question}")

        if "总利润" in question or "总销售额" in question or "总计" in question:
            if "利润" in question:
                total = sum(r["利润"] for r in self.data)
                return f"  分析: 总利润为 {total:,} 元"
            elif "销售额" in question:
                total = sum(r["销售额"] for r in self.data)
                return f"  分析: 总销售额为 {total:,} 元"

        if "平均" in question:
            if "销售额" in question:
                avg = sum(r["销售额"] for r in self.data) / len(self.data)
                return f"  分析: 月均销售额 {avg:,.0f} 元"
            if "利润" in question:
                avg = sum(r["利润"] for r in self.data) / len(self.data)
                return f"  分析: 月均利润 {avg:,.0f} 元"

        if "最高" in question or "最多" in question:
            if "销售额" in question:
                max_row = max(self.data, key=lambda r: r["销售额"])
                return f"  分析: 最高销售额在{max_row['月份']}，为 {max_row['销售额']:,} 元"

        if "趋势" in question or "变化" in question:
            trends = [f"{r['月份']}: {r['销售额']:,}元" for r in self.data]
            return f"  分析: 销售趋势\n    " + "\n    ".join(trends)

        return "  分析: 无法理解查询，请重新描述"

# 测试
ta = TableAgent()
print("\nTableAgent (数据分析):")
print(ta.query("总利润是多少？"))
print(ta.query("销售额趋势如何？"))
print(ta.query("哪个月销售额最高？"))

# ============ 行业落地架构 ============
print("\n" + "=" * 60)
print("🔧 Demo: 企业级 Agent 架构")
print("=" * 60)

ENTERPRISE_ARCH = """
┌────────────────────────────────────────────────────────────────┐
│              企业级 Agent 架构                                  │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  用户入口                                                      │
│  ┌──────┐ ┌──────┐ ┌──────┐                                    │
│  │ 网页  │ │ 飞书  │ │ 微信  │  ← 多渠道接入                  │
│  └──┬───┘ └──┬───┘ └──┬───┘                                    │
│     └────────┼────────┘                                        │
│              ▼                                                  │
│  ┌─────────────────────┐                                       │
│  │  统一接入层 (API网关) │ ← 鉴权 / 限流 / 路由              │
│  └─────────┬───────────┘                                       │
│            ▼                                                    │
│  ┌─────────────────────┐                                       │
│  │  意图识别 Agent      │ ← 分类用户意图                      │
│  └──┬──────┬──────┬───┘                                       │
│     │      │      │                                            │
│     ▼      ▼      ▼                                            │
│  ┌───┐ ┌────┐ ┌────┐                                          │
│  │客服│ │CRM │ │分析│  ← 专业 Agent 集群                    │
│  └───┘ └────┘ └────┘                                          │
│     │      │      │                                            │
│     └──┬───┴──┬───┘                                            │
│        ▼      ▼                                                │
│  ┌────────┐ ┌────────┐                                         │
│  │知识库   │ │数据库   │  ← 企业内部系统                     │
│  └────────┘ └────────┘                                         │
│                                                                │
│  监控: 对话日志 → 标注 → 模型优化 → 持续迭代                  │
└────────────────────────────────────────────────────────────────┘
"""
print(ENTERPRISE_ARCH)

print("\n✅ Agent 行业落地完成！")
print("\n🎉 RAG + Agent 全部 11 个模块完成！")
