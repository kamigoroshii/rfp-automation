# RFP Automation System

Enterprise-level multi-agent AI platform for automating Request for Proposal (RFP) response processes for cable and wire manufacturers.

## Overview

The RFP Automation System discovers RFPs from multiple sources, parses technical specifications, matches products from OEM catalogs, generates pricing estimates, and consolidates responses—reducing manual effort and improving response accuracy and speed.

## Architecture

- **Sales Agent**: Discovers and summarizes RFPs from websites and emails
- **Document Agent**: Parses PDF documents and extracts specifications
- **Technical Agent**: Matches RFP specifications with product catalog using semantic search
- **Pricing Agent**: Calculates cost estimates using rules and ML models
- **Learning Agent**: Continuous improvement through feedback loops
- **Orchestrator Agent**: Coordinates all agents using CrewAI framework

## Technology Stack

- **Backend**: Python 3.10+, FastAPI, CrewAI
- **Databases**: PostgreSQL, Redis, Qdrant
- **AI/ML**: HuggingFace Transformers, spaCy, XGBoost
- **Frontend**: React.js, Tailwind CSS
- **DevOps**: Docker, GitHub Actions

## Quick Start

### Prerequisites

- Python 3.10 or higher
- PostgreSQL 15+
- Redis 7+
- Docker (optional)

### Installation

1. Clone the repository
2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Setup environment variables:
   ```bash
   cp .env.template .env
   # Edit .env with your configuration
   ```

5. Initialize database:
   ```bash
   python shared/database/init_db.py
   ```

6. Load product catalog:
   ```bash
   python agents/technical/product_loader.py
   ```

7. Start the API server:
   ```bash
   uvicorn orchestrator.api.main:app --reload
   ```

### Docker Deployment

```bash
docker-compose up -d
```

## Project Structure

```
rfp-automation-system/
├── agents/              # Agent implementations
│   ├── sales/          # Sales Agent
│   ├── document/       # Document Agent
│   ├── technical/      # Technical Agent
│   ├── pricing/        # Pricing Agent
│   └── learning/       # Learning Agent
├── orchestrator/       # Orchestrator and API
│   ├── api/           # FastAPI routes
│   ├── tasks/         # Celery tasks
│   └── tools/         # CrewAI tools
├── shared/            # Shared utilities
│   ├── models.py      # Data models
│   ├── database/      # Database connections
│   ├── cache/         # Redis cache
│   └── vector_db/     # Qdrant client
├── frontend/          # React dashboard
├── data/              # Sample data and generators
├── tests/             # Test suites
└── docker/            # Docker configurations
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

```bash
# Run all tests
pytest

# Run unit tests
pytest tests/unit

# Run integration tests
pytest tests/integration

# Run with coverage
pytest --cov=. --cov-report=html
```

## License

Proprietary - All rights reserved
