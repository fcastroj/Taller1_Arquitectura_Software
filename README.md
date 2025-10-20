# IA de Chat para E-commerce

Este proyecto implementa una IA de chat para e-commerce utilizando una arquitectura hexagonal. Proporciona funcionalidades para la recuperación de información de productos y la interacción por chat.

## Configuración e Instalación

### Prerrequisitos

*   Python 3.11
*   Docker (opcional, para despliegue en contenedores)

### Configuración Local

1.  **Clonar el repositorio:**
    ```bash
    git clone <repository_url>
    cd e-commerce-chat-ai
    ```

2.  **Crear un entorno virtual:**
    ```bash
    python -m venv venv
    source venv/Scripts/activate  # En Windows
    # source venv/bin/activate    # En macOS/Linux
    ```

3.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar variables de entorno:**
    Crea un archivo `.env` en el directorio raíz del proyecto basado en `.env.example`.
    ```
    GEMINI_API_KEY=tu_clave_api_gemini_aqui
    DATABASE_URL=sqlite:///./data/ecommerce_chat.db
    ENVIRONMENT=development
    ```
    Reemplaza `tu_clave_api_gemini_aqui` con tu clave API real de Google Gemini.

### Ejecutar la Aplicación Localmente

```bash
uvicorn src.infrastructure.api.main:app --host 0.0.0.0 --port 8000 --reload
```
La API será accesible en `http://localhost:8000`.

### Configuración de Docker

1.  **Construir la imagen de Docker:**
    ```bash
    docker build -t ecommerce-chat-ai .
    ```

### Ejecutar con Docker Compose

1.  **Configurar variables de entorno:**
    Asegúrate de tener un archivo `.env` configurado como se describe en la sección "Configuración Local".

2.  **Iniciar los servicios:**
    ```bash
    docker-compose up --build
    ```
    La API será accesible en `http://localhost:8000`.

## Arquitectura

Este proyecto sigue una Arquitectura Hexagonal (también conocida como Puertos y Adaptadores) para asegurar una clara separación de preocupaciones, mantenibilidad y capacidad de prueba. La idea central es aislar la lógica de negocio (capas de dominio y aplicación) de preocupaciones externas como bases de datos, UI o servicios externos.

### Capas:

*   **Capa de Dominio:** Contiene las entidades de negocio centrales, objetos de valor y reglas de negocio. Es independiente de cualquier tecnología externa.
*   **Capa de Aplicación:** Orquesta los objetos de dominio para cumplir con los casos de uso. Define interfaces (puertos) que la capa de infraestructura implementará.
*   **Capa de Infraestructura:** Contiene los adaptadores que conectan la aplicación con el mundo exterior. Esto incluye implementaciones para bases de datos, APIs externas (como el proveedor LLM) y la API web.

### Flujo de Interacción:

1.  **Agentes Externos (ej. solicitudes HTTP):** Interactúan con la capa de `Infraestructura` (específicamente el adaptador de API).
2.  **Adaptador de API:** Traduce las solicitudes externas en llamadas a los servicios de la capa de `Aplicación`.
3.  **Servicios de Aplicación:** Utilizan entidades de `Dominio` y `Repositorios de Dominio` (interfaces definidas en el dominio, implementadas en infraestructura) para realizar la lógica de negocio.
4.  **Adaptadores de Infraestructura (ej. Base de Datos, Proveedor LLM):** Implementan las interfaces del `Repositorio de Dominio` e interactúan con sistemas externos.

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENTE (Frontend)                       │
│                  (Navegador, Postman, etc.)                 │
└────────────────────────┬────────────────────────────────────┘
                         │ Solicitudes HTTP
                         ↓
┌─────────────────────────────────────────────────────────────┐
│              CAPA DE INFRAESTRUCTURA                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  FastAPI (main.py)                                   │  │
│  │  - Endpoints HTTP                                    │  │
│  │  - Validación de solicitudes                         │  │
│  │  - Serialización de respuestas                       │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                   │
│                         ↓                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Repositorios (SQLAlchemy)                           │  │
│  │  - product_repository.py                             │  │
│  │  - chat_repository.py                                │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Servicios Externos                                  │  │
│  │  - gemini_service.py (IA de Google Gemini)           │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│              CAPA DE APLICACIÓN                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Servicios (Casos de Uso)                             │  │
│  │  - product_service.py                                │  │
│  │  - chat_service.py                                   │  │
│  │  Orquesta: Repositorios + Servicios Externos         │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  DTOs (Objetos de Transferencia de Datos)            │  │
│  │  - Validación con Pydantic                           │  │
│  │  - Transformación de datos                           │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│              CAPA DE DOMINIO                                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Entidades (Lógica de Negocio)                       │  │
│  │  - Product                                           │  │
│  │  - ChatMessage                                       │  │
│  │  - ChatContext                                       │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Repositorios (Interfaces)                           │  │
│  │  - IProductRepository                                │  │
│  │  - IChatRepository                                   │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Excepciones (Excepciones del Dominio)               │  │
│  │  - ProductNotFoundError                              │  │
│  │  - InvalidProductDataError                           │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Documentación de la API

Este proyecto utiliza FastAPI, que genera automáticamente documentación interactiva de la API (Swagger UI).

Una vez que la aplicación esté en ejecución (ya sea localmente o mediante Docker Compose), puedes acceder a la documentación de la API en:

*   **Swagger UI:** `http://localhost:8000/docs`
*   **ReDoc:** `http://localhost:8000/redoc`

Estas interfaces te permiten explorar los endpoints disponibles, sus formatos esperados de solicitud/respuesta e incluso probarlos directamente desde tu navegador.

## Guía de Despliegue

Para el desarrollo y las pruebas locales, el archivo `docker-compose.yml` proporciona una forma conveniente de ejecutar la aplicación en un entorno en contenedores. Consulta la sección "Ejecutar con Docker Compose" para obtener instrucciones.

Para despliegues en producción, considera utilizar herramientas de orquestación como Kubernetes, o servicios específicos de la nube (ej. AWS ECS, Google Cloud Run) para gestionar la escalabilidad, fiabilidad y otros requisitos de nivel de producción. El `Dockerfile` proporcionado se puede utilizar como base para construir tus imágenes de producción.

## Pruebas

Para ejecutar las pruebas unitarias y de integración del proyecto, utiliza `pytest`:

```bash
pytest
```

Este comando descubrirá y ejecutará todas las pruebas ubicadas en el directorio `tests/`.