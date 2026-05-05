# 🤖 AI Coding Agent with Tool Execution

An intelligent CLI-based AI agent that performs tasks using structured reasoning and dynamically executes tools like file creation, system commands, and API calls.

---

## 🚀 Features

- 🧠 Chain-of-Thought Reasoning (START → PLAN → TOOL → OUTPUT)
- 💻 Generates and writes code directly into files
- 🛠️ Executes system commands and handles file operations
- 🌦️ Integrated Weather API (demonstrates tool extensibility)
- 🔌 Modular design to easily add new tools
- ⚡ Powered by Google Gemini API (OpenAI-compatible)

---

## 🏗️ Tech Stack

- Python
- OpenAI SDK (Gemini API Compatible)
- Pydantic (Structured Outputs)
- Requests (API Handling)
- Subprocess (System Commands)

---

## 📂 Project Structure

```
AI-Agent/
│── agent.py
│── tools.py
│── .env
│── README.md
```

---

## ⚙️ How It Works

1. User enters a query
2. Agent plans steps (PLAN)
3. Executes tools if needed (TOOL)
4. Observes results (OBSERVE)
5. Returns final answer (OUTPUT)

---

## 🛠️ Available Tools

### 🌦️ Weather Tool

Fetches real-time weather using:
https://wttr.in/

### 📁 File Writer

Creates and writes structured multi-line code into files

### 💻 Command Executor

Runs system commands in the terminal

---

## ▶️ Setup & Run

### 1. Clone the Repository

```bash
git clone https://github.com/Techyshiva/ai-coding-agent.git
cd ai-coding-agent
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Add API Key

Create a `.env` file:

```
OPENAI_API_KEY=your_api_key_here
```

Or just paste the Key in the Section given in The Request area

### 4. Run the Agent

```bash
python agent.py
```

---

## 💡 Example Prompts

```
Create a simple HTML file
```

```
What is the weather in Mumbai?
```

```
Create a folder and write a Python script
```

---

## 🔮 Future Improvements

- GUI (Streamlit / Web App)
- Memory-based conversations
- More tools (database, browser automation)
- Multi-agent workflows

---

## 👨‍💻 Author

Shivam Mhaske  
Email: mhaskeshivam1@gmail.com  
GitHub: https://github.com/Techyshiva

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!
