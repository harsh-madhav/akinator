# Akinator Game with AI

An Akinator-like game powered by OpenAI's GPT model, built with FastAPI (Python) and React (TypeScript).

## 🛠️ Prerequisites

- Docker and Docker Compose
- OpenAI API key (for the AI backend)

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/harsh-madhav/akinator.git
cd akinator
```

### 2. Set Up Environment Variables

Create a `.env` file in the root directory with your OpenAI API key:

```bash
# .env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4  # or gpt-3.5-turbo
```

### 3. Build and Run with Docker Compose

```bash
docker compose up --build
```

This will start all services:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Redis: Running on port 6379

## 🏗️ Project Structure

```
.
├── akinator-ui/          # Frontend React application
│   ├── src/              # Source files
│   ├── public/           # Static files
│   └── Dockerfile        # Frontend Docker configuration
│
├── backend/              # Backend FastAPI application
│   ├── app/              # Application code
│   │   ├── main.py       # FastAPI application
│   │   └── llm_game.py   # Game logic
│   └── Dockerfile        # Backend Docker configuration
│
├── docker-compose.yml    # Docker Compose configuration
└── .env                 # Environment variables
```

## 🌐 API Endpoints

- `POST /api/start` - Start a new game
- `POST /api/answer` - Submit an answer to the current question

