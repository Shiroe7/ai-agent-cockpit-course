# 案例代码

本目录只依赖 Python 3.10+ 标准库即可运行基础实验。可选的真实模型与 MCP 功能见 `.env.example` 和 `requirements-optional.txt`。

## 一键验证

```powershell
python -m unittest discover -s tests -v
```

## 实验一：多轮对话记忆

```powershell
python -m lab01_memory_chat.cli --session student-01
```

可测试：

1. 输入“我叫小刘，我喜欢安静的座舱”；
2. 隔几轮后询问“我叫什么？”或“我喜欢什么？”；
3. 退出并重新启动，确认信息仍可恢复；
4. 切换 `--session student-02`，确认不同会话不会串数据。

## 实验二：车辆数据工具调用

```powershell
python -m lab02_vehicle_tools.cli --vehicle CQ-AI-001
```

可询问“查询胎压”“还有多少续航”“解释故障码 BMS_102”等。程序会输出工具选择、参数、结果和审计日志。

## 实验三：VLM 座舱 UI 理解

```powershell
python -m lab03_vlm_ui.cli
```

默认由 `MockVLM` 产生结构化识别结果，用于离线教学。`OpenAICompatibleVLM` 提供真实多模态模型接入示例。

## 可选 MCP Server

安装当前稳定版 SDK：

```powershell
pip install -r requirements-optional.txt
python -m lab02_vehicle_tools.mcp_server
```

基础实验不依赖 MCP SDK，避免网络或版本变化阻塞教学。
