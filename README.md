# Books API

**Tech Challenge - Fase 1 - PosTech 8MLET**

* **Por:** Juliano Monteiro (rm369594)
* **GitHub:** [https://github.com/julianomont](https://github.com/julianomont)
* **Email:** [juliano.monteiro@outlook.com](mailto:juliano.monteiro@outlook.com)
* **LinkedIn:** [https://www.linkedin.com/in/julianofmonteiro](https://www.linkedin.com/in/julianofmonteiro)

API REST para consulta de dados de livros extraídos via web scraping do site [books.toscrape.com](http://books.toscrape.com).

### Links Importantes

| Recurso | Link |
|---------|------|
| **Documentação Swagger** | <a href="https://books-api-o2d6gk76rq-uc.a.run.app/docs" target="_blank">Ver Documentação</a> |
| **Dashboard** | <a href="https://books-dashboard-o2d6gk76rq-uc.a.run.app" target="_blank">Acessar Dashboard</a> |
| **Deploy** | <a href="https://books-api-o2d6gk76rq-uc.a.run.app" target="_blank">API Base URL</a> |
| **Repositório** | <a href="https://github.com/julianomont/8MLET-F1.git" target="_blank">GitHub</a> |
| **Vídeo Demonstração** | em breve |

---

## Índice

1. [Requisitos do Projeto](#descrição-do-projeto)
2. [Arquitetura](#arquitetura)
3. [Hospedagem no Google Cloud Platform (GCP)](#hospedagem-no-google-cloud-platform-gcp)
4. [Instalação e Configuração](#instalação-e-configuração)
5. [Execução](#execução)
6. [Documentação das Rotas da API](#documentação-das-rotas-da-api)
7. [Exemplos de Chamadas](#exemplos-de-chamadas)
8. [Dashboard de Monitoramento](#dashboard-de-monitoramento)

---

## Requisitos do Projeto

### Objetivo

API REST robusta que:
1. **Extrai dados** via web scraping de ~1000 livros do site books.toscrape.com
2. **Armazena** os dados em banco PostgreSQL
3. **Disponibiliza** endpoints HTTP para consulta, filtros e estatísticas
4. **Prepara dados** para consumo por modelos de Machine Learning
5. **Monitora** performance com logs estruturados e métricas

### Funcionalidades

| Funcionalidade | Descrição |
|----------------|-----------|
| **Web Scraping Robusto** | Extração de título, preço, rating, disponibilidade, categoria e imagem |
| **Listagem de Livros** | Consulta paginada de todos os livros |
| **Busca e Filtros** | Busca por título, categoria e faixa de preço |
| **Estatísticas** | Métricas gerais e por categoria |
| **Pipeline ML-Ready** | Features normalizadas e dataset para treinamento |
| **Autenticação JWT** | Proteção de rotas administrativas |
| **Monitoramento** | Logs estruturados, métricas e dashboard Streamlit |
| **Documentação** | Swagger UI integrada em `/docs` |

### Tecnologias Utilizadas

| Tecnologia | Uso |
|------------|-----|
| **FastAPI** | Framework para APIs REST |
| **SQLAlchemy** | ORM para banco de dados |
| **Pydantic** | Validação de dados |
| **BeautifulSoup4** | Web scraping |
| **httpx** | Cliente HTTP assíncrono |
| **pandas** | Análise de dados e estatísticas |
| **python-jose** | Autenticação JWT |
| **Streamlit** | Dashboard de monitoramento |
| **PostgreSQL** | Banco de dados relacional |

---

## Arquitetura

O projeto segue uma **arquitetura modular em camadas** (Clean Architecture).

### Diagrama de Arquitetura

```mermaid
flowchart TB
    subgraph Cliente["🌐 Cliente"]
        Browser["Navegador/Postman"]
        ML["Modelo ML"]
        Dashboard["Dashboard Streamlit"]
    end

    subgraph API["📡 FastAPI"]
        Router["Router v1"]
        Auth["Auth Middleware"]
        Logging["Logging Middleware"]
        
        subgraph Endpoints["Endpoints"]
            Books["/books"]
            Categories["/categories"]
            Stats["/stats"]
            MLEndpoint["/ml"]
            Health["/health"]
            Metrics["/metrics"]
            Scraping["/scraping 🔒"]
        end
    end

    subgraph Services["⚙️ Serviços"]
        BookService["BookService"]
        StatsService["StatsService"]
        MLService["MLService"]
        AuthService["AuthService"]
    end

    subgraph Data["💾 Dados"]
        Repository["Repository"]
        PG[("PostgreSQL")]
        Scraper["Web Scraper"]
        Site["books.toscrape.com"]
    end

    Browser --> Router
    ML --> MLEndpoint
    Dashboard --> Metrics

    Router --> Auth
    Auth --> Logging
    Logging --> Endpoints

    Books --> BookService
    Categories --> BookService
    Stats --> StatsService
    MLEndpoint --> MLService
    Scraping --> Scraper

    BookService --> Repository
    StatsService --> Repository
    MLService --> Repository

    Repository --> PG
    Scraper --> Site
    Scraper --> PG
```

### Estrutura de Pastas

```
MLE-P1/
├── 📁 data/                    # Dados (books.db)
├── 📁 docs/                    # Documentação adicional
├── 📁 scripts/                 # Scripts auxiliares
│   ├── run_scraper.py          # Execução do scraper
│   ├── create_admin.py         # Criação de admin
│   └── dashboard.py            # Dashboard Streamlit
└── 📁 src/                     # Código fonte
    ├── 📁 api/                 # Camada de API (endpoints e rotas)
    │   └── v1/endpoints/       # Endpoints versionados
    ├── 📁 core/                # Configurações centrais
    │   ├── config.py           # Settings da aplicação
    │   ├── database.py         # Conexão com banco
    │   ├── middleware.py       # Logs e métricas
    │   └── logging.py          # Sistema de logs
    ├── 📁 models/              # Models do banco (SQLAlchemy)
    ├── 📁 schemas/             # Schemas de validação (Pydantic)
    ├── 📁 repository/          # Camada de acesso a dados
    ├── 📁 services/            # Lógica de negócio
    ├── 📁 scraper/             # Módulo de web scraping
    └── main.py                 # Ponto de entrada da API
```

### Fluxo de Requisição

```mermaid
sequenceDiagram
    participant C as Cliente
    participant R as Router
    participant M as Middleware
    participant E as Endpoint
    participant S as Service
    participant D as Repository
    participant DB as PostgreSQL

    C->>R: GET /api/v1/books
    R->>M: Logging + Métricas
    M->>E: books.list_books()
    E->>S: BookService.get_books_paginated()
    S->>D: Repository.get_all()
    D->>DB: SELECT * FROM books
    DB-->>D: [BookModel, ...]
    D-->>S: [BookSchema, ...]
    S-->>E: (books, total)
    E-->>M: PaginatedBooks
    M-->>R: Response + Log
    R-->>C: JSON Response
```

---

## Hospedagem no Google Cloud Platform (GCP)

A aplicação é hospedada utilizando serviços serverless do Google Cloud, garantindo escalabilidade automática e baixo custo. A arquitetura é dividida em dois serviços principais rodando no Cloud Run.

### Componentes do Deploy
Toda a orquestração é feita pelo script deploy.sh, que automatiza os seguintes passos:

**Artifact Registry (books-repo):**
- Serve como o "Docker Hub" privado.
- Armazena as versões das imagens Docker da API e do Dashboard.
- Localização: us-central1.

**Cloud Build:**
- Constrói as imagens Docker na nuvem (sem depender da máquina local).
- Usa os arquivos cloudbuild.api.yaml e cloudbuild.dashboard.yaml como instruções.

**Cloud Run (Compute):**
- Serviço 1: API (books-api):
  - Container: src/main.py (FastAPI).
  - Porta: 8000.
  - Variáveis: DATABASE_URL (Conexão Postgres), JWT_SECRET_KEY (Segurança).
- Serviço 2: Dashboard (books-dashboard):
  - Container: scripts/dashboard.py (Streamlit).
  - Porta: 8501.
  - Variáveis: API_URL (Para consumir os dados da API).

### Fluxo de Deploy
| Passo | Descrição |
|---------|------|
| **Build** | O deploy.sh envia o código para o Cloud Build. |
| **Push** | As imagens construídas são salvas no Artifact Registry. |
| **Deploy** | O Cloud Run puxa as novas imagens e sobe novas revisões dos serviços. |
| **Configuração** | As variáveis de ambiente (como senhas do banco) são injetadas de forma segura durante o deploy (--set-env-vars). |

### Deploy Automático (GCP)

Para realizar o deploy no Google Cloud Platform (Cloud Run):

1. **Configurar o script de deploy**:
   Edite o arquivo `deploy.sh` e atualize as variáveis `DATABASE_URL` e `JWT_SECRET_KEY`.

2. **Executar o script**:
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```
   
   O script irá:
   - Criar o repositório no Artifact Registry (se não existir)
   - Construir as imagens Docker da API e Dashboard
   - Fazer o deploy no Cloud Run configurando as variáveis de ambiente

**Resumo da Arquitetura:**

    Cloud Build (Constrói) -> Artifact Registry (Armazena) -> Cloud Run (Executa API + Dashboard)


## Instalação e Configuração

### Requisitos

- Python 3.11+
- pip ou Poetry

### Passo 1: Clonar o Repositório

```bash
git clone <url-do-repositorio>
cd MLE-P1
```

### Passo 2: Criar Ambiente Virtual

```bash
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual
source .venv/bin/activate    # Linux/Mac
.venv\Scripts\activate       # Windows
```

### Passo 3: Instalar Dependências

```bash
# Via pip
pip install -r requirements.txt

# Ou via Poetry
poetry install
```

### Passo 4: Configurar Variáveis de Ambiente (Opcional)

Crie um arquivo `.env` na raiz do projeto:

```env
DEBUG=True
API_V1_STR=/api/v1
PROJECT_NAME="API de Livros"
DATABASE_URL=postgresql://user:pass@host:port/dbname
JWT_SECRET_KEY=sua-chave-secreta-aqui
```

---

## Execução

### 1. Popular o Banco de Dados (Scraping)

```bash
python scripts/run_scraper.py
```

Este comando extrai ~1000 livros e salva no banco de dados configurado.

### 2. Iniciar a API

```bash
uvicorn src.main:app --reload
```

### 3. Acessar a Documentação

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### 4. Executar Testes
```bash
# Executa testes unitários e de integração
pytest
```

---

## Documentação das Rotas da API

Base URL: `http://localhost:8000/api/v1`

### Autenticação (`/auth`)

| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/auth/login` | Autentica e retorna tokens JWT |
| `POST` | `/auth/refresh` | Renova o access token |

### Livros (`/books`)

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/books/` | Lista livros com paginação |
| `GET` | `/books/{id}` | Detalhes de um livro específico |
| `GET` | `/books/search` | Busca por título e/ou categoria |
| `GET` | `/books/top-rated` | Lista os mais bem avaliados |
| `GET` | `/books/price-range` | Filtra por faixa de preço |

### Categorias (`/categories`)

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/categories/` | Lista todas as categorias |

### Estatísticas (`/stats`)

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/stats/overview` | Estatísticas gerais (total, média, distribuição) |
| `GET` | `/stats/categories` | Estatísticas por categoria |

### Machine Learning (`/ml`)

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/ml/features` | Features normalizadas para inferência |
| `GET` | `/ml/training-data` | Dataset completo para treinamento com split train/test |
| `POST` | `/ml/predictions` | Recebe e processa predições de modelos |

### Scraping (`/scraping`) 🔒

| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/scraping/trigger` | Dispara scraping (requer token admin) |

### Saúde (`/health`)

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/health` | Verifica status da API |

### Métricas (`/metrics`)

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/metrics/` | Métricas consolidadas de performance |
| `GET` | `/metrics/requests` | Requisições recentes com detalhes |
| `GET` | `/metrics/summary` | Resumo rápido de métricas |

---

## Dashboard de Monitoramento

O projeto inclui um dashboard Streamlit para visualização de métricas em tempo real.

O Dashboard é uma aplicação separada construída com a biblioteca Streamlit (scripts/dashboard.py), que consome dados de performance expostos pela própria API.

**Arquitetura do Dashboard**

Coleta de Dados (LoggingMiddleware):
- Existe um interceptador (middleware) em src/core/middleware.py.
- Ele cronometra cada requisição (tempo de início vs. fim).
- Armazena métricas (status code, tempo de resposta, endpoint) em uma memória temporária (MetricsStore).

Exposição dos Dados (/api/v1/metrics):
- A API possui endpoints específicos para exportar esses dados em JSON.
- GET /metrics/: Retorna contadores gerais (Total de Requests, Erros, Uptime).
- GET /metrics/requests: Retorna a lista detalhada das últimas requisições.

Visualização (Streamlit):
- O script dashboard.py faz chamadas HTTP periódicas para esses endpoints.
- Usa Pandas para transformar os JSONs em DataFrames.
- Renderiza gráficos e tabelas interativas.

**Executar o Dashboard:**
```bash
# Primeiro, inicie a API
uvicorn src.main:app --reload

# Em outro terminal, inicie o dashboard
streamlit run scripts/dashboard.py
```

O dashboard exibe:
- Total de requisições e taxa de erro
- Gráficos por endpoint, status code e método HTTP
- Tabela de requisições recentes com filtros

---

## Exemplos de Chamadas

### Login (Obter Token)

**Primeiro, crie o usuário admin:**
```bash
python scripts/create_admin.py
```

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

### Refresh Token

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/refresh" \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "<REFRESH_TOKEN>"}'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

### Disparar Scraping (Rota Protegida)

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/scraping/trigger" \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

**Response:**
```json
{
  "message": "Scraping iniciado em background",
  "triggered_by": "admin"
}
```

---

### Listar Livros (Paginado)

**Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/books/?page=1&limit=10"
```

**Response:**
```json
{
  "total": 1000,
  "page": 1,
  "limit": 10,
  "items": [
    {
      "id": 1,
      "title": "A Light in the Attic",
      "price": 51.77,
      "rating": 3,
      "availability": true,
      "category": "Poetry",
      "image_url": "https://..."
    }
  ]
}
```

---

### Buscar por Título

**Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/books/search?title=Python"
```

**Response:**
```json
[
  {
    "id": 123,
    "title": "Learning Python",
    "price": 39.99,
    "rating": 5,
    "availability": true,
    "category": "Programming",
    "image_url": "https://..."
  }
]
```

---

### Buscar por Categoria

**Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/books/search?category=Fiction"
```

**Response:**
```json
[
  {
    "id": 45,
    "title": "The Great Gatsby",
    "price": 22.50,
    "rating": 4,
    "availability": true,
    "category": "Fiction",
    "image_url": "https://..."
  }
]
```

---

### Obter Detalhes de um Livro

**Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/books/1"
```

**Response:**
```json
{
  "id": 1,
  "title": "A Light in the Attic",
  "price": 51.77,
  "rating": 3,
  "availability": true,
  "category": "Poetry",
  "image_url": "https://..."
}
```

---

### Livros Mais Bem Avaliados

**Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/books/top-rated?limit=5"
```

**Response:**
```json
[
  {
    "id": 15,
    "title": "Best Book Ever",
    "price": 29.99,
    "rating": 5,
    "availability": true,
    "category": "Classics",
    "image_url": "https://..."
  }
]
```

---

### Filtrar por Faixa de Preço

**Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/books/price-range?min_price=10&max_price=30"
```

**Response:**
```json
[
  {
    "id": 22,
    "title": "Affordable Book",
    "price": 19.99,
    "rating": 4,
    "availability": true,
    "category": "Non-Fiction",
    "image_url": "https://..."
  }
]
```

---

### Listar Categorias

**Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/categories/"
```

**Response:**
```json
[
  "Fiction",
  "Poetry",
  "Fantasy",
  "Romance",
  "Science Fiction",
  "Mystery"
]
```

---

### Estatísticas Gerais

**Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/stats/overview"
```

**Response:**
```json
{
  "total_books": 1000,
  "avg_price": 35.07,
  "min_price": 10.00,
  "max_price": 59.99,
  "rating_distribution": {
    "1": 50,
    "2": 100,
    "3": 300,
    "4": 350,
    "5": 200
  },
  "top_categories": [
    {"name": "Fiction", "count": 150},
    {"name": "Romance", "count": 120}
  ]
}
```

---

### Estatísticas por Categoria

**Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/stats/categories"
```

**Response:**
```json
[
  {
    "category": "Fiction",
    "total_books": 150,
    "avg_price": 32.50,
    "avg_rating": 3.8
  },
  {
    "category": "Poetry",
    "total_books": 80,
    "avg_price": 28.00,
    "avg_rating": 4.2
  }
]
```

---

### Features para Machine Learning

**Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/ml/features"
```

**Response:**
```json
[
  {
    "id": 1,
    "price_norm": 0.85,
    "rating": 3,
    "category_code": 12,
    "availability": true
  }
]
```

---

### Dataset para Treinamento

**Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/ml/training-data?test_size=0.2"
```

**Response:**
```json
{
  "total_samples": 1000,
  "feature_names": ["price_norm", "rating", "category_code", "availability_int"],
  "target_name": "rating",
  "train": {
    "X": [[0.83, 3.0, 0.0, 1.0], ...],
    "y": [3, 1, 4, ...],
    "size": 800
  },
  "test": {
    "X": [[0.45, 2.0, 1.0, 1.0], ...],
    "y": [2, 5, 3, ...],
    "size": 200
  },
  "metadata": {
    "category_mapping": {"Fiction": 0, "Poetry": 1, ...},
    "price_min": 10.0,
    "price_max": 59.99,
    "test_size": 0.2
  }
}
```

---

### Enviar Predições de Modelos

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/ml/predictions" \
  -H "Content-Type: application/json" \
  -d '{"predictions": [{"book_id": 1, "predicted_rating": 4.5, "confidence": 0.92}]}'
```

**Response:**
```json
{
  "processed": 1,
  "rejected": 0,
  "predictions": [
    {"book_id": 1, "predicted_rating": 4.5, "confidence": 0.92}
  ],
  "errors": null
}
```

---

### Verificar Saúde da API

**Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/health"
```

**Response:**
```json
{
  "status": "saudável",
  "version": "1.0.0",
  "timestamp": "2026-01-01T19:00:00.000000"
}
```

---

## Documentação Adicional

Para mais detalhes sobre a implementação, consulte:

- [Arquitetura](docs/architecture.md) - Diagrama de arquitetura
- [Guia da API](docs/api_guide.md) - Referência rápida dos endpoints
