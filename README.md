README.md
 
# 🚇 Metro Train Breakdown Multi-Agent System
 
This solution demonstrates a fully automated multi-agent response workflow for metro rail disruptions, implemented using **AutoGen v0.4.18**, **FastAPI**, and a lightweight **HTML/JavaScript frontend**.
 
---
 
## 🔧 Tech Stack
 
- 🧠 [AutoGen v0.4.18](https://github.com/microsoft/autogen) (`autogen-agentchat`)

- 🖥️ FastAPI + Uvicorn (Python 3.9–3.11)

- 🧰 FunctionCallingTool-based tools

- 📦 GroupChatManager orchestration

- 🖼️ Jinja2-based frontend UI
 
---
 
## ✅ Features
 
- Detects train disruptions

- Notifies drivers and depot teams

- Drafts public alerts and internal updates

- Confirms resolution and closes the loop with the public

- Fully async, message-based agentic execution
 
---
 
## 🚀 Getting Started
 
### 1. 📦 Create a Virtual Environment (Python 3.9–3.11)
 
```bash

python3.9 -m venv .venv

source .venv/bin/activate  # Windows: .venv\Scripts\activate

 