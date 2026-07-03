# 🤖 Multi-Agent Research Assistant

A Multi-Agent AI System where 3 specialized agents collaborate 
to take a user's research query and produce a fully written, 
polished research report automatically.

Built by **Tooba Nadeem** as a portfolio project for ML/AI Engineering.

---

## 🧠 How It Works
User Query
↓
[1] Research Agent   → Searches web & extracts raw data
↓
[2] Summarizer Agent → Structures data into key points
↓
[3] Writer Agent     → Writes full polished report
↓
Final Research Report ✅

---

## 🛠️ Tech Stack

| Tool                  | Purpose                        |
|-----------------------|--------------------------------|
| Google Gemini API     | Powers all 3 AI agents         |
| Tavily API            | Real-time web search           |
| Streamlit             | Frontend UI                    |
| Python 3.11           | Core language                  |
| python-dotenv         | API key management             |

---

## 📁 Project Structure
multi_agent_research_assistant/
│
├── agents/
│   ├── research_agent.py
│   ├── summarizer_agent.py
│   └── writer_agent.py
│
├── tools/
│   └── web_search.py
│
├── pipeline/
│   └── orchestrator.py
│
├── ui/
│   └── app.py
│
├── outputs/
│   └── reports/
│
├── .env
├── requirements.txt
└── README.md

---

## ⚙️ Setup & Installation

### 1 — Clone or Download the Project
```bash
cd "C:\Ai Agents\multi_agent_research_assistant"
```

### 2 — Create Conda Environment
```bash
conda create -n multi_agent_env python=3.11
conda activate multi_agent_env
```

### 3 — Install Dependencies
```bash
pip install -r requirements.txt
```

### 4 — Add Your API Keys
Create a `.env` file in the root folder:
GEMINI_API_KEY=your_gemini_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here

### 5 — Run the App
```bash
streamlit run ui/app.py
```

---

## 🔑 API Keys

| API           | Free? | Link                          |
|---------------|-------|-------------------------------|
| Google Gemini | ✅ Yes | https://aistudio.google.com   |
| Tavily Search | ✅ Yes | https://app.tavily.com        |

---

## ✨ Features

- 🔍 Real-time web search using Tavily
- 🤖 3 specialized AI agents working in sequence
- 🎨 Choose writing tone: Professional / Academic / Casual
- 📄 Full structured research report output
- 🔗 Clickable sources with references
- ⬇️ Download report as .txt file
- 💾 Auto-saves reports to outputs/reports/

---

## 👩‍💻 Author

**Tooba Nadeem**
ML/AI Engineer (in progress)