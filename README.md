# Timely - AI Productivity Coach

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5--turbo-orange.svg)](https://openai.com)
[![Tailwind CSS](https://img.shields.io/badge/TailwindCSS-3.3+-blue.svg)](https://tailwindcss.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A modern, AI-powered productivity coach application that helps users make better decisions about task prioritization, daily planning, and time management. Built with FastAPI, OpenAI GPT, and a responsive Tailwind CSS frontend.

## Features

- **Conversational AI Interface** - Natural language interaction with personalized coaching
- **Intelligent Task Management** - Priority-based task organization and completion tracking
- **Multiple Personality Modes** - Coach, Friend, Strict, or Zen communication styles
- **Energy Level Awareness** - AI adapts suggestions based on user's current energy state
- **Daily Planning Assistant** - Generate realistic schedules with time block recommendations
- **Morning Check-in System** - Start each day with motivational guidance
- **Responsive Web Design** - Optimized for desktop and mobile devices
- **Real-time Token Tracking** - Monitor AI usage and associated costs

## Architecture

```
timely-ai-coach/
├── backend/                 # FastAPI application
│   ├── api/                # REST API endpoints
│   ├── core/               # Configuration and database setup
│   ├── models/             # SQLAlchemy database models
│   └── services/           # Business logic layer
├── frontend/               # Client-side application
│   ├── src/                # JavaScript source and CSS
│   └── dist/               # Compiled assets
├── llm/                    # AI agent components
│   ├── agents/             # AI assistant implementations
│   ├── prompts/            # Prompt template system
│   └── memory/             # Future vector memory integration
├── docker/                 # Container configuration
└── docs/                   # Project documentation
```

## Quick Start

### Prerequisites

- Python 3.11 or higher
- Node.js 18.0 or higher
- OpenAI API key
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/aaronalcuizar/timely-ai-coach.git
   cd timely-ai-coach
   ```

2. **Backend setup**
   ```bash
   # Create and activate virtual environment
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Frontend setup**
   ```bash
   cd frontend
   npm install
   npm run build-css
   cd ..
   ```

4. **Environment configuration**
   ```bash
   cp .env.example .env
   # Edit .env file and add your OpenAI API key
   ```

### Running the Application

1. **Start the backend server**
   ```bash
   uvicorn backend.main:app --reload
   ```

2. **Open the frontend**
   ```bash
   cd frontend
   # Windows
   start index.html
   
   # macOS
   open index.html
   
   # Linux
   xdg-open index.html
   ```

3. **Access the application**
   - Frontend: Open the HTML file in your browser
   - Backend API: http://127.0.0.1:8000
   - API Documentation: http://127.0.0.1:8000/docs

## Docker Deployment

### Quick Start with Docker Compose

```bash
# Build and run all services
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Documentation: http://localhost:8000/docs
```

### Manual Docker Build

```bash
# Build backend image
docker build -t timely-backend -f docker/Dockerfile.backend .

# Run backend container
docker run -e OPENAI_API_KEY=your_key_here -p 8000:8000 timely-backend
```

## Configuration

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Required
OPENAI_API_KEY=sk-your-openai-api-key-here

# Optional
ANTHROPIC_API_KEY=your-anthropic-key-here
JWT_SECRET_KEY=your-super-secret-jwt-key
DEBUG=true
DATABASE_URL=sqlite:///./timely.db
```

### OpenAI API Setup

1. Create an account at [OpenAI Platform](https://platform.openai.com)
2. Generate an API key from the API keys section
3. Add the key to your `.env` file
4. The application uses GPT-3.5-turbo for cost-effective responses

## Development

### Backend Development

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Code formatting
black backend/
isort backend/

# Type checking
mypy backend/

# Start development server with hot reload
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

```bash
cd frontend

# Build CSS with watch mode
npm run build-css

# Run development server (optional)
npm run dev
```

### API Testing

```bash
# Health check
curl http://localhost:8000/health

# Test chat endpoint
curl -X POST http://localhost:8000/api/v1/chat/next-task \
  -H "Content-Type: application/json" \
  -d '{"message": "What should I do next?", "energy_level": "medium"}'
```

## API Documentation

Interactive API documentation is automatically generated and available at:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Application health check |
| POST | `/api/v1/chat/next-task` | Get AI task recommendations |
| POST | `/api/v1/chat/plan-day` | Generate daily schedules |
| POST | `/api/v1/chat/morning-checkin` | Morning motivation and planning |

## Technology Stack

### Backend Technologies
- **FastAPI** - Modern Python web framework
- **OpenAI GPT-4** - Large language model for AI responses
- **SQLAlchemy** - SQL toolkit and Object-Relational Mapping
- **Pydantic** - Data validation using Python type annotations
- **Uvicorn** - Lightning-fast ASGI server

### Frontend Technologies
- **HTML5** - Modern web markup
- **Tailwind CSS** - Utility-first CSS framework
- **Vanilla JavaScript** - ES6+ features for interactivity
- **Font Awesome** - Professional icon library

### DevOps and Deployment
- **Docker** - Application containerization
- **GitHub Actions** - Continuous integration and deployment
- **Railway/Render** - Cloud platform deployment options

## Deployment Options

### Railway (Recommended)
1. Fork this repository
2. Connect your fork to [Railway](https://railway.app)
3. Add environment variables in Railway dashboard
4. Deploy automatically from main branch

### Render
1. Fork this repository
2. Create new web service on [Render](https://render.com)
3. Configure build and start commands
4. Add environment variables
5. Deploy from GitHub integration

### Self-Hosted Docker
```bash
# Production deployment
docker-compose -f docker-compose.prod.yml up -d
```

## Contributing

We welcome contributions to improve Timely. Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/enhancement-name`)
3. Make your changes with clear, descriptive commits
4. Add tests for new functionality
5. Ensure all tests pass (`pytest`)
6. Update documentation as needed
7. Submit a pull request with a clear description

### Development Guidelines

- Follow PEP 8 style guidelines for Python code
- Use conventional commit messages
- Add comprehensive tests for new features
- Update documentation for API changes
- Ensure Docker builds succeed

## Testing

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=backend --cov-report=html

# Run specific test file
pytest backend/tests/test_api.py

# Run tests in watch mode
pytest-watch
```

## Troubleshooting

### Common Issues

#### 1. Backend Shows "Offline" Status
**Problem**: Frontend shows "offline" even with valid OpenAI API key
**Solution**: 
- Restart the backend server completely
- Check that you're using fresh assistant instances, not cached global instances
- Verify API key is correctly loaded in `.env` file

#### 2. Unicode/Emoji Errors on Windows
**Problem**: `UnicodeEncodeError: 'charmap' codec can't encode character`
**Solution**: 
- Remove emoji characters from console output
- Use `print()` statements without emoji in server startup

#### 3. Port Already in Use Error
**Problem**: `[Errno 10048] error while attempting to bind on address`
**Solution**:
```bash
# Kill processes using port 8000
taskkill /F /IM python.exe /T

# Wait and restart
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

#### 4. OpenAI API Errors
**Problem**: API calls failing or using fallbacks
**Solution**:
- Verify API key is valid and has credits
- Check OpenAI usage dashboard for quota limits
- Ensure you have access to GPT-3.5-turbo model

#### 5. Frontend Connection Loop
**Problem**: Frontend continuously retrying connection
**Solution**:
- Check that backend is running on correct port
- Verify CORS configuration allows frontend origin
- Clear browser cache and refresh

### API Testing

Test the backend directly:
```bash
# Health check
curl http://localhost:8000/health

# Test AI integration
curl -X POST http://localhost:8000/api/v1/chat/next-task \
  -H "Content-Type: application/json" \
  -d '{"message": "What should I do next?", "energy_level": "medium"}'
```

### Token Usage Monitoring

Monitor costs by checking token usage in responses:
- Typical response: 100-300 tokens (~$0.0001-0.0003)
- Daily usage estimate: 50-100 requests = ~$0.01-0.03
- Set up OpenAI usage alerts in your dashboard

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for complete details.

## Support and Documentation

- **Bug Reports**: [GitHub Issues](https://github.com/aaronalcuizar/timely-ai-coach/issues)
- **Feature Requests**: [GitHub Discussions](https://github.com/aaronalcuizar/timely-ai-coach/discussions)
- **Documentation**: Available in the `/docs` directory
- **API Reference**: Generated automatically at `/docs` endpoint

## Acknowledgments

- OpenAI for providing the GPT API that powers the AI functionality
- The FastAPI team for creating an excellent Python web framework
- Tailwind CSS for the utility-first CSS framework
- The open-source community for the various libraries and tools used

---

**Author**: [Aaron Alcuizar](https://github.com/aaronalcuizar)  
**Project Repository**: [https://github.com/aaronalcuizar/timely-ai-coach](https://github.com/aaronalcuizar/timely-ai-coach)
```