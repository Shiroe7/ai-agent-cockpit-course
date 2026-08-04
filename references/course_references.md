# 课程参考资料

本页列出第10-12课相关的课程材料与技术文档，帮助学习者按主题进行拓展阅读。页码对应原始 PDF 页码或演示文稿页码。

## 课程主题资料

### Agent Planning-从推理到规划

- p.11：Planner-Executor-Replanner 与智能体运行闭环；
- p.41-42：证据验证、失败反馈与再规划；
- p.48-55：工作记忆、流程记忆与事实更新；
- p.18、52：工具契约、权限、版本与不可逆动作；
- p.20、32：规划与智能体评测维度；
- p.59、61：能力、方法、支撑与统一闭环。

### MCP & Skill

- p.11-20、22-27：Function Calling 与工具调用；
- p.30-38：MCP 客户端、服务端与通信架构；
- p.39-42、45-47：Harness、Skill 与任务编排。

### 大模型安全与合规

- p.8、13：大模型应用攻击面与常见风险；
- p.35、38、43：多轮对话安全、越狱与上下文污染；
- p.42：图像劫持与多模态提示注入；
- p.51、54-55：生命周期防护、输入预处理与输出分析；
- p.39、70-71、76：攻击、检测与事实核验指标。

### 自动驾驶和 Alpamayo

- p.29：VLM 感知建议与传统控制链执行的职责划分；
- p.34、38：自动驾驶任务与 VLA 流程；
- p.44-46：推理过程与安全约束；
- p.48以后：Alpamayo 案例。

### VLA Slides

- p.26-30：Action Gap 与视觉语言到动作的转换；
- p.53-69：推理与动作耦合；
- p.73-74：局限与未来方向。

## 在线技术文档

- [Model Context Protocol 架构](https://modelcontextprotocol.io/docs/learn/architecture)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [LangGraph Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)
- [LangGraph Memory](https://docs.langchain.com/oss/python/langgraph/add-memory)
- [LangChain Tools](https://docs.langchain.com/oss/python/langchain/tools)

## 对应实验

- 实验一可重点阅读智能体记忆、上下文污染与持久化相关内容；
- 实验二可重点阅读工具契约、Function Calling、MCP 与权限控制相关内容；
- 实验三可重点阅读多模态提示注入、VLM/VLA 边界与安全确认相关内容；
- 课程项目可结合评测指标、失败处理和安全约束完成方案设计。
