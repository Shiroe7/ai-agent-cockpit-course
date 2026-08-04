# AI智能体及其座舱应用：第10-12课时基础包

这是课程第10-12课时的第一版可运行教学基础包，已经把“少量教学课件 + 重点实验指导书 + 实验报告 + 案例代码 + 课程项目模板”放在同一目录中。

## 覆盖范围

- 第10课：智能体框架、开发流程与多轮对话记忆；
- 第11课：车辆数据工具调用与基于 VLM 的座舱 UI 理解；
- 第12课：课程项目选题、架构、安全、评测与答辩。

## 课程资源

- `slides/`：第10-12课的 Beamer/Metropolis TeX 源文件与 PDF；
- `docs/`：实验指导书、实验报告模板、课程项目设计书模板、工作总结与验收说明的 TeX 与 PDF；
- `code/`：三个可离线运行的案例、8项自动测试和课程项目脚手架；
- `references/`：已使用材料、页码和后续增量合并规则；
- `build.ps1`：一键重新编译全部 PDF。

其中 `docs/work_summary_acceptance.pdf` 汇总了本次完成目标、实现思路、当前状态、验收步骤、边界和教师签字清单。

## 三项实验

1. `lab01_memory_chat`：SQLite 多轮/跨会话记忆，包含事实新增与更新；
2. `lab02_vehicle_tools`：本地车辆模拟数据、工具 Schema、统一结果与可选 MCP Server；
3. `lab03_vlm_ui`：MockVLM/在线 VLM 适配器、ActionPlan、安全门、确认与审计日志。

三个案例默认使用 mock 或本地数据，不需要 API Key；座舱案例只做模拟执行，不连接真实车辆控制接口。

## 快速开始

```powershell
cd code
python -m unittest discover -s tests -v
python -m lab01_memory_chat.cli --session demo
python -m lab02_vehicle_tools.cli --vehicle CQ-AI-001
python -m lab03_vlm_ui.cli
```

需要在线模型或 MCP 示例时，再安装可选依赖：

```powershell
pip install -r requirements-optional.txt
```

## TeX 与 PDF

在本目录执行：

```powershell
powershell -ExecutionPolicy Bypass -File .\build.ps1
```

也可分别在 `slides/` 和 `docs/` 中使用 XeLaTeX 编译：

```powershell
xelatex lesson10.tex
xelatex lesson11.tex
xelatex lesson12.tex

xelatex experiment_guide.tex
xelatex experiment_report_template.tex
xelatex capstone_design_template.tex
xelatex work_summary_acceptance.tex
```

幻灯片已使用用户指定的 `csl-cqu/slides-template` 新版主题、配色和重庆大学标识。

## 使用原则

1. 先离线跑通，再连接真实模型；
2. 模型只提出候选行动，应用代码负责校验、授权与审计；
3. 工具或 VLM 没有证据时，不编造车辆状态；
4. 高风险动作必须确认，教学代码默认只模拟；
5. 新增群内 PPT 后，增量补充图示、案例和引用，不破坏三项实验主线。

## 当前边界

- MCP 示例按当前稳定 Python SDK v1 接口编写，可选依赖暂时约束为 `<2`；正式冻结课程环境时需再次核对版本。
- VLM 在线调用采用 OpenAI-compatible 接口示例，不绑定具体厂商。
- 本目录已按可直接建立 GitHub 仓库的结构整理，但尚未替课程组公开发布，也未擅自选择开源许可证。
