# E-commerce Chat AI

This project implements an e-commerce chat AI using a hexagonal architecture. It provides functionalities for product information retrieval and chat interactions.

## Setup and Installation

### Prerequisites

*   Python 3.11
*   Docker (optional, for containerized deployment)

### Local Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd e-commerce-chat-ai
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/Scripts/activate  # On Windows
    # source venv/bin/activate    # On macOS/Linux
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure environment variables:**
    Create a `.env` file in the root directory of the project based on `.env.example`.
    ```
    GEMINI_API_KEY=your_gemini_api_key_here
    DATABASE_URL=sqlite:///./data/ecommerce_chat.db
    ENVIRONMENT=development
    ```
    Replace `your_gemini_api_key_here` with your actual Google Gemini API key.

### Running the Application Locally

```bash
uvicorn src.infrastructure.api.main:app --host 0.0.0.0 --port 8000 --reload
```
The API will be accessible at `http://localhost:8000`.

### Docker Setup

1.  **Build the Docker image:**
    ```bash
    docker build -t ecommerce-chat-ai .
    ```

### Running with Docker Compose

1.  **Configure environment variables:**
    Ensure you have a `.env` file configured as described in the "Local Setup" section.

2.  **Start the services:**
    ```bash
    docker-compose up --build
    ```
    The API will be accessible at `http://localhost:8000`.

## Architecture

This project follows a Hexagonal Architecture (also known as Ports and Adapters) to ensure a clear separation of concerns, maintainability, and testability. The core idea is to isolate the business logic (domain and application layers) from external concerns like databases, UI, or external services.

### Layers:

*   **Domain Layer:** Contains the core business entities, value objects, and business rules. It is independent of any external technology.
*   **Application Layer:** Orchestrates the domain objects to fulfill use cases. It defines interfaces (ports) that the infrastructure layer will implement.
*   **Infrastructure Layer:** Contains the adapters that connect the application to the outside world. This includes implementations for databases, external APIs (like the LLM provider), and the web API.

### Interaction Flow:

1.  **External Agents (e.g., HTTP requests):** Interact with the `Infrastructure` layer (specifically the API adapter).
2.  **API Adapter:** Translates external requests into calls to the `Application` layer's services.
3.  **Application Services:** Use `Domain` entities and `Domain Repositories` (interfaces defined in the domain, implemented in infrastructure) to perform business logic.
4.  **Infrastructure Adapters (e.g., Database, LLM Provider):** Implement the `Domain Repository` interfaces and interact with external systems.

**Diagrams illustrating this architecture should be added here.**

## API Documentation

This project uses FastAPI, which automatically generates interactive API documentation (Swagger UI).

Once the application is running (either locally or via Docker Compose), you can access the API documentation at:

*   **Swagger UI:** `http://localhost:8000/docs`
*   **ReDoc:** `http://localhost:8000/redoc`

These interfaces allow you to explore the available endpoints, their expected request/response formats, and even test them directly from your browser.

## Deployment Guide

For local development and testing, the `docker-compose.yml` file provides a convenient way to run the application in a containerized environment. Refer to the "Running with Docker Compose" section for instructions.

For production deployments, consider using orchestration tools like Kubernetes, or cloud-specific services (e.g., AWS ECS, Google Cloud Run) to manage scalability, reliability, and other production-grade requirements. The provided `Dockerfile` can be used as a base for building your production images.

## Testing

To run the unit and integration tests for the project, use `pytest`:

```bash
pytest
```

This command will discover and execute all tests located in the `tests/` directory.
