# 🤖 TaskPilot AI – Intelligent Agentic Assistant

TaskPilot AI is an intelligent AI assistant built using Python, Groq LLM, and Streamlit. It uses LLM-powered function calling to understand user instructions and execute tasks through specialized Python tools.

## 🚀 Features

- **AI Conversational Assistant:** Answers general questions using an LLM.
- **Smart Calculator:** Performs mathematical calculations.
- **Task Management:** Add, retrieve, and complete tasks.
- **Knowledge Retrieval:** Searches a predefined knowledge base.
- **Agentic Workflow:** Dynamically selects and executes tools using LLM function calling.
- **Interactive Interface:** Chat-based UI developed using Streamlit.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend development |
| Groq API | LLM inference |
| GPT-OSS 120B | Language model |
| Function Calling | Tool selection and execution |
| Streamlit | User interface |
| JSON | Task storage |

## 🏗️ Project Architecture

```text
User
 |
 v
Streamlit Interface
 |
 v
AI Agent (Python)
 |
 v
Groq LLM
 |
 v
Tool Selection
 |
 +-- Calculator
 |
 +-- Task Manager
 |
 +-- Knowledge Search
 |
 v
Tool Execution
 |
 v
AI Response
```

## 📂 Project Structure

```text
TaskPilot-AI/
│
├── app.py
├── agent.py
├── tools.py
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Alok-Kumar-cmd/TaskPilot-AI.git

cd TaskPilot-AI
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API key

Create a `.env` file in the project directory:

```env
GROQ_API_KEY=your_groq_api_key
```

Never upload your API key to GitHub.

### 5. Run the application

```bash
streamlit run app.py
```

## 🧠 Agentic Workflow

TaskPilot AI follows an agentic execution loop:

1. Receives a natural-language instruction.
2. Sends the instruction to the LLM.
3. The LLM determines whether a tool is required.
4. The selected Python function is executed.
5. The tool result is returned to the LLM.
6. The LLM generates a final response.

## 🔮 Future Enhancements

- Conversational memory
- Retrieval-Augmented Generation (RAG)
- Web search integration
- Voice-based interaction
- Multi-agent collaboration
- Database integration

## 👨‍💻 Developer

**Alok Kumar**

AI/ML Enthusiast | Python Developer

## 📜 License

This project is developed for educational and portfolio purposes.
