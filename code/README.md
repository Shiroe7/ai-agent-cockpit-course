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

默认由 `MockVLM` 产生结构化识别结果，用于离线教学。在线拓展需先设置 `OPENAI_API_KEY`、`OPENAI_BASE_URL` 和 `VLM_MODEL`，再运行：

```powershell
python -m lab03_vlm_ui.cli --online
```

在线模式仍只生成候选动作，并保留结构校验、安全确认和模拟执行。

## 可选 MCP Server

按 `requirements-optional.txt` 中的版本范围安装 SDK：

```powershell
pip install -r requirements-optional.txt
python -m lab02_vehicle_tools.mcp_client_demo --vehicle CQ-AI-001
```

客户端会自动启动 MCP Server、列出工具并调用车辆状态工具。MCP Server 使用 JSON-RPC 协议，不能在服务器窗口直接输入自然语言。基础实验不依赖 MCP SDK，避免网络或版本变化阻塞教学。
