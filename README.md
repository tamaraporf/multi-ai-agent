# Multi AI Agent

A multi-agent AI system built with FastAPI, Streamlit, LangChain, and Groq, featuring web search capabilities through Tavily API.

## 🚀 Features

- **Multiple AI Models**: Support for various Groq AI models
  - `llama-3.3-70b-versatile` - Advanced language model
  - `llama-3.1-8b-instant` - Fast and efficient model
- **Web Search Integration**: Powered by Tavily API for real-time information retrieval
- **Interactive UI**: Built with Streamlit for easy interaction
- **RESTful API**: FastAPI backend for programmatic access
- **Customizable System Prompts**: Define your AI agent's behavior
- **Structured Logging**: Comprehensive logging system for debugging and monitoring

## 🏗️ Architecture

```
├── app/
│   ├── backend/        # FastAPI backend
│   │   └── api.py      # API endpoints
│   ├── common/         # Shared utilities
│   │   ├── logger.py   # Logging configuration
│   │   └── custom_exception.py
│   ├── config/         # Configuration
│   │   └── settings.py # Environment variables
│   ├── core/           # Core logic
│   │   └── ai_agent.py # AI agent implementation
│   └── frontend/       # Streamlit UI
│       └── ui.py       # User interface
├── logs/               # Application logs
├── Dockerfile          # Docker configuration
├── Jenkinsfile         # CI/CD pipeline
└── requirements.txt    # Python dependencies
```

## 📋 Prerequisites

- Python 3.11+
- Groq API Key ([Get it here](https://console.groq.com/keys))
- Tavily API Key ([Get it here](https://app.tavily.com/))

## 🔧 Installation

### 1. Clone the repository

```bash
git clone https://github.com/tamaraporf/multi-ai-agent.git
cd multi-ai-agent
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

## 🚀 Usage

### Running the Application

Start both backend and frontend services:

```bash
python app/main.py
```

This will launch:
- **Backend API**: http://127.0.0.1:9999
- **Frontend UI**: http://localhost:8501

### Using the Web Interface

1. Open your browser and navigate to `http://localhost:8501`
2. Define your AI agent with a custom system prompt
3. Select an AI model from the dropdown
4. (Optional) Enable web search for real-time information
5. Enter your query and click "Ask Agent"

### Using the API

#### Health Check

```bash
curl http://127.0.0.1:9999/
```

#### Chat Endpoint

```bash
curl -X POST http://127.0.0.1:9999/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "llama-3.3-70b-versatile",
    "system_prompt": "You are a helpful assistant",
    "messages": ["What is the weather like today?"],
    "allow_search": true
  }'
```

## 🐳 Docker Deployment

### Build the image

```bash
docker build -t multi-ai-agent .
```

### Run the container

```bash
docker run -p 9999:9999 -p 8501:8501 \
  -e GROQ_API_KEY=your_key \
  -e TAVILY_API_KEY=your_key \
  multi-ai-agent
```

## 📊 API Documentation

### POST `/chat`

Send a message to the AI agent and receive a response.

**Request Body:**

```json
{
  "model_name": "llama-3.3-70b-versatile",
  "system_prompt": "You are a helpful assistant",
  "messages": ["Your question here"],
  "allow_search": false
}
```

**Response:**

```json
{
  "response": "AI agent's response here"
}
```

**Status Codes:**
- `200`: Success
- `400`: Invalid model name
- `500`: Server error

## 🛠️ Development

### Project Structure

- **Backend (`app/backend/`)**: FastAPI application handling API requests
- **Frontend (`app/frontend/`)**: Streamlit web interface
- **Core (`app/core/`)**: AI agent logic using LangChain and LangGraph
- **Common (`app/common/`)**: Shared utilities (logging, exceptions)
- **Config (`app/config/`)**: Configuration and environment settings

### Available Models

| Model | Description | Best For |
|-------|-------------|----------|
| `llama-3.3-70b-versatile` | Advanced reasoning | Complex tasks, long conversations |
| `llama-3.1-8b-instant` | Fast responses | Quick queries, simple tasks |

### Logging

Logs are stored in the `logs/` directory with daily rotation:
- Format: `log_YYYY-MM-DD.log`
- Level: INFO and above
- Console and file output

## 🔒 Security Best Practices

- Never commit `.env` files to version control
- Rotate API keys regularly
- Use environment variables for sensitive data
- Keep dependencies updated

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is part of the LLMOps Udemy course.

## 🙏 Acknowledgments

- [LangChain](https://python.langchain.com/) - AI application framework
- [Groq](https://groq.com/) - Fast AI inference
- [Tavily](https://tavily.com/) - Search API
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [Streamlit](https://streamlit.io/) - Interactive UI framework

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check the [documentation](https://github.com/tamaraporf/multi-ai-agent/wiki)

---

**Built with ❤️ for LLMOps learning**
