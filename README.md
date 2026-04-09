
<h1 align="center">PythonClaw</h1>

<p align="center">
  <strong>OpenClaw 的纯 Python 版本</strong><br>
  记忆 · RAG · skills · Web 仪表盘 · 语音 · 守护进程Daemon · 多渠道channel
</p>



---

## 主要特性

| | 特性 | 详细信息 |
|---|---------|--------|
| 🧠 | **与提供商无关** | DeepSeek、Grok、Claude、Gemini、Kimi、GLM — 或任何兼容 OpenAI 的 API |
| 🛠️ | **三层技能系统** | 渐进式加载：元数据 → 指令 → 资源。通过 [ClawHub](https://clawhub.com) 社区市场（13K+ 免费技能） |
| 💾 | **持久记忆** | 基于 Markdown 的长期记忆，包含每日日志和语义召回 |
| 🔍 | **混合 RAG** | BM25 + 密集嵌入 + RRF 融合 + LLM 重排序 |
| 🌐 | **Web 仪表盘** | 浏览器 UI，用于聊天、配置、技能目录、身份编辑和市场 |
| 🎙️ | **语音输入** | Web 聊天中的 Deepgram 语音转文本 |
| ⏰ | **定时任务** | 通过 YAML 安排任务或让代理创建自己的任务 |
| 📡 | **多渠道** | CLI、Web、Telegram、Discord、WhatsApp — 相同的代理，不同的界面 |
| 🔄 | **守护进程模式** | PID 管理的后台进程，带有 `start` / `stop` / `status` 命令 |
| 🧬 | **灵魂 + 角色** | 将核心身份与可交换的角色呈现分开 |
| 🔧 | **TOOLS.md** | 本地环境笔记 — 代理的备忘单 |
| 🔒 | **按组隔离** | 每个聊天会话获取自己的记忆（可选） |
| 🔁 | **并发控制** | 每会话锁 + 全局信号量防止交错 |

---

## 快速开始

```bash
pip install pythonclaw

# 首次设置 — 选择 LLM 提供商并输入 API 密钥
pythonclaw onboard

# 启动代理守护进程（Web 仪表盘位于 http://localhost:7788）
pythonclaw start

# 交互式 CLI 聊天
pythonclaw chat

# 停止守护进程
pythonclaw stop
```

**从源码安装：**

```bash
git clone https://github.com/ericwang915/PythonClaw.git
cd PythonClaw
pip install -e .
pythonclaw onboard
```

---

## 命令行参考

| 命令 | 描述 |
|---------|------------|
| `pythonclaw onboard` | 交互式设置向导 — 选择 LLM 提供商，输入 API 密钥 |
| `pythonclaw start` | 以后台守护进程方式启动代理 |
| `pythonclaw start -f` | 在前台启动（不守护进程化） |
| `pythonclaw start --channels telegram discord whatsapp` | 启动时启用消息渠道 |
| `pythonclaw stop` | 停止运行中的守护进程 |
| `pythonclaw status` | 显示守护进程状态（PID、运行时间、端口） |
| `pythonclaw chat` | 交互式 CLI 聊天（前台 REPL） |
| `pythonclaw skill search <query>` | 在 [ClawHub](https://clawhub.com) 上搜索技能 |
| `pythonclaw skill browse` | 浏览评分最高的技能 |
| `pythonclaw skill install <id>` | 安装社区技能 |
| `pythonclaw skill info <id>` | 查看技能详情 |

### 首次运行

```
$ pythonclaw start

  ╔══════════════════════════════════════╗
  ║       PythonClaw — 设置向导          ║
  ╚══════════════════════════════════════╝

  选择您的 LLM 提供商：

    1. DeepSeek
    2. Grok (xAI)
    3. Claude (Anthropic)
    4. Gemini (Google)
    5. Kimi (Moonshot)
    6. GLM (Zhipu / ChatGLM)

  输入数字 (1-6): 2
  → Grok (xAI)

  API 密钥: ********
  → 密钥已设置 (xai-****)

  验证中... ✔ 有效！
  ✔ 设置完成！

[PythonClaw] 守护进程已启动 (PID 12345)。
[PythonClaw] 仪表盘: http://localhost:7788
```

---

## 架构

```
┌──────────────────────────────────────────────────────────────┐
│                         PythonClaw                            │
├──────────┬────────────┬───────────┬──────────────────────────┤
│ CLI      │ 守护进程   │ 会话管理  │      核心                │
│          │            │           │                          │
│ onboard  │ start /    │ Store(MD) │ Agent                    │
│ chat     │ stop /     │ Manager   │ ├─ 记忆 (Markdown)       │
│ skill …  │ status     │ Locks +   │ ├─ RAG (混合)            │
│          │            │ Semaphore │ ├─ 技能 (3层)            │
│ Web UI ◄─┤ 渠道       │           │ ├─ 压缩                  │
│ 语音输入  │ Telegram   │ 按组隔离  │ ├─ 灵魂 + 角色          │
│          │ Discord    │           │ ├─ 组上下文              │
│          │ WhatsApp   │           │ └─ 工具执行              │
├──────────┴────────────┴───────────┴──────────────────────────┤
│               LLM 提供商抽象层                               │
│ DeepSeek │ Grok │ Claude │ Gemini │ Kimi │ GLM              │
├──────────────────────────────────────────────────────────────┤
│              ClawHub 市场 (clawhub.com)                      │
└──────────────────────────────────────────────────────────────┘
```

---

## Web 仪表盘

使用 `pythonclaw start` 启动并打开 **http://localhost:7788**。

- **仪表盘** — 代理状态、灵魂/角色预览、工具列表
- **聊天** — 实时聊天，支持语音输入（Deepgram）
- **技能目录** — 按类别浏览已安装的技能
- **市场** — 从 [ClawHub](https://clawhub.com) 搜索和安装技能
- **配置** — 在浏览器中编辑 LLM 提供商、API 密钥和设置

---

## 配置

所有配置都存储在 `pythonclaw.json` 中（由 `pythonclaw onboard` 自动创建）。
请参阅 [`pythonclaw.example.json`](pythonclaw.example.json) 获取完整模板。

```jsonc
{
  "llm": {
    "provider": "grok",
    "grok": { "apiKey": "xai-...", "model": "grok-3" }
  },
  "tavily":   { "apiKey": "" },
  "deepgram": { "apiKey": "" },
  "web":      { "host": "0.0.0.0", "port": 7788 },
  "channels": {
    "telegram": { "token": "" },
    "discord":  { "token": "" },
    "whatsapp": { "phoneNumberId": "", "token": "", "verifyToken": "pythonclaw_verify" }
  },
  "isolation":   { "perGroup": false },
  "concurrency": { "maxAgents": 4 }
}
```

环境变量（如 `DEEPSEEK_API_KEY`、`TAVILY_API_KEY`）会覆盖 JSON 值。

---

## 支持的 LLM 提供商

| 提供商 | 默认模型 | 安装额外项 |
|----------|---------------|---------------|
| **DeepSeek** | `deepseek-chat` | — |
| **Grok (xAI)** | `grok-3` | — |
| **Claude (Anthropic)** | `claude-sonnet-4-20250514` | — (已包含) |
| **Gemini (Google)** | `gemini-2.0-flash` | — (已包含) |
| **Kimi (Moonshot)** | `moonshot-v1-128k` | — |
| **GLM (Zhipu)** | `glm-4-flash` | — |
| 任何兼容 OpenAI 的 | 自定义 | — |

---

## 技能

### 三层渐进式加载

| 级别 | 加载时机 | 内容 |
|-------|-------------|--------|
| **L1 — 元数据** | 始终（启动时） | YAML 前置 matter 中的 `name` + `description` |
| **L2 — 指令** | 代理激活技能时 | 完整的 SKILL.md 内容 |
| **L3 — 资源** | 按需 | 捆绑的脚本、模式、数据文件 |

```yaml
---
name: code_runner
description: 在隔离的子进程中安全执行 Python 代码。
---
# 代码运行器

## 指令
运行 `python {skill_path}/run_code.py "expression"`
```

### ClawHub 市场

浏览并安装来自 [ClawHub](https://clawhub.com) 的 13,000+ 社区技能 — 免费，无需 API 密钥：

```bash
pythonclaw skill search "数据库备份"
pythonclaw skill install <skill-id>
```

也可从 Web 仪表盘的 **市场** 选项卡访问。

---

## 记忆 & RAG

### Markdown 记忆

```
~/.pythonclaw/context/memory/
├── MEMORY.md           # 精选长期记忆
└── 2026-02-23.md       # 每日追加日志
```

当启用 **按组隔离**（配置中 `"isolation": { "perGroup": true }`）时，
每个会话（Telegram 聊天、Discord 频道等）在 `~/.pythonclaw/context/groups/<session-id>/` 下获取自己的 `memory/`、`persona/`
和 `soul/`，而全局记忆仍可通过读取回退访问。

### TOOLS.md — 本地笔记

```
~/.pythonclaw/context/tools/
└── TOOLS.md              # 您的环境特定备忘单
```

技能定义工具的 *工作方式*。`TOOLS.md` 存储 *您的* 具体信息 — SSH 主机、设备
昵称、项目路径、首选默认值、API 端点。将它们分开意味着
您可以更新技能而不会丢失笔记，并且可以共享技能而不会泄露您的
基础设施。可从 Web 仪表盘编辑。

### 混合 RAG 管道

```
查询 → BM25 (稀疏) + 嵌入 (密集) → RRF 融合 → LLM 重排序 → Top-K
```

---

## 作为库使用

```python
from pythonclaw import Agent
from pythonclaw.core.llm.openai_compatible import OpenAICompatibleProvider

provider = OpenAICompatibleProvider(
    api_key="sk-...",
    base_url="https://api.deepseek.com/v1",
    model_name="deepseek-chat",
)

agent = Agent(provider=provider)
print(agent.chat("法国的首都是什么？"))
```

---

## 项目结构

```
PythonClaw/
├── pythonclaw/
│   ├── main.py                # CLI 入口 (onboard/start/stop/status/chat/skill)
│   ├── onboard.py             # 交互式设置向导
│   ├── daemon.py              # 基于 PID 的守护进程生命周期
│   ├── server.py              # 多渠道守护进程服务器
│   ├── core/
│   │   ├── agent.py           # 核心推理循环
│   │   ├── tools.py           # 工具模式和执行
│   │   ├── skill_loader.py    # 三层技能系统
│   │   ├── skillhub.py        # ClawHub 市场客户端
│   │   ├── persistent_agent.py
│   │   ├── compaction.py      # 上下文压缩
│   │   ├── llm/               # 提供商适配器
│   │   ├── memory/            # Markdown 记忆
│   │   ├── knowledge/         # 知识库 RAG
│   │   └── retrieval/         # BM25 + 密集 + 融合 + 重排序
│   ├── channels/              # Telegram, Discord, WhatsApp
│   ├── scheduler/             # 定时任务, 心跳
│   ├── web/                   # FastAPI 仪表盘 + 静态资源
│   └── templates/             # 内置技能模板
├── context/                   # 运行时数据 (gitignored)
├── pyproject.toml
├── pythonclaw.example.json    # 配置模板
└── LICENSE
```

---

## 开发

```bash
git clone https://github.com/ericwang915/PythonClaw.git
cd PythonClaw
python -m venv .venv && source .venv/bin/activate
pip install -e .
pytest tests/ -v
```

---


