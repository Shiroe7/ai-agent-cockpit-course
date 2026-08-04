# AI智能体及其座舱应用：第10-12课

本仓库提供“AI智能体及其座舱应用”课程第10-12课的教学课件、实验指导、报告模板、案例代码与课程项目脚手架。内容围绕多轮对话记忆、工具调用、多模态座舱交互和课程项目设计展开。

## 课程内容

- 第10课：智能体框架、开发流程与多轮对话记忆；
- 第11课：车辆数据工具调用与基于 VLM 的座舱 UI 理解；
- 第12课：课程项目选题、方案设计、安全约束、评测与展示。

## 目录结构

- `slides/`：第10-12课教学课件的 TeX 源文件与 PDF；
- `docs/`：实验指导书、实验报告模板和课程项目设计书模板；
- `code/`：三个可离线运行的案例、自动测试与课程项目脚手架；
- `references/`：课程参考资料及其对应主题；
- `build.ps1`：重新编译全部课程 PDF。

## 实践项目

### 实验一：多轮对话记忆智能体

`lab01_memory_chat` 使用 SQLite 保存会话消息和结构化事实，支持同一会话内记忆、跨进程恢复、事实更新与会话隔离。

### 实验二：车辆数据工具调用智能体

`lab02_vehicle_tools` 提供本地车辆模拟数据、工具 Schema、统一结果结构、参数校验与可选 MCP Server，用于理解模型决策与工具执行之间的边界。

### 实验三：多模态座舱交互智能体

`lab03_vlm_ui` 提供 MockVLM 和在线 VLM 适配接口，将界面理解结果转换为结构化 `ActionPlan`，并通过目标校验、风险分级、用户确认和审计日志约束动作执行。

三个案例默认使用模拟数据，无需 API Key；涉及座舱控制的动作仅做模拟执行，不连接真实车辆控制接口。

## 快速开始

建议使用 Python 3.10 或更高版本。在仓库根目录执行：

```powershell
cd code
python -m unittest discover -s tests -v
python -m lab01_memory_chat.cli --session demo
python -m lab02_vehicle_tools.cli --vehicle CQ-AI-001
python -m lab03_vlm_ui.cli
```

需要运行 MCP Server 或连接兼容接口的在线模型时，安装可选依赖：

```powershell
pip install -r requirements-optional.txt
```

## 编译课程材料

课程材料使用 XeLaTeX 编译。在仓库根目录执行：

```powershell
powershell -ExecutionPolicy Bypass -File .\build.ps1
```

也可进入对应目录分别编译：

```powershell
cd slides
xelatex lesson10.tex
xelatex lesson11.tex
xelatex lesson12.tex

cd ..\docs
xelatex experiment_guide.tex
xelatex experiment_report_template.tex
xelatex capstone_design_template.tex
```

## 学习建议

1. 先运行离线案例，理解状态、工具和安全门如何协作；
2. 对照实验指导书完成测试，再替换模型或扩展工具；
3. 模型只负责理解、规划和提出候选行动，应用代码负责参数校验、授权、执行与审计；
4. 工具或 VLM 缺少证据时，不推断或编造车辆状态；
5. 高风险动作必须经过用户确认，课程代码默认只进行模拟执行。

## 使用边界

- MCP 示例面向 Python SDK v1，依赖范围约束为 `mcp>=1.27,<2`；
- 在线 VLM 示例采用 OpenAI-compatible 接口，不绑定具体模型供应商；
- 本仓库用于教学与实验，不构成真实车辆控制系统或生产级安全方案；
- 若实验使用截图、语音或车辆数据，应确保来源合法并完成必要的隐私处理。
