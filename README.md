# 🎬 CineReserve API

![CI](https://github.com/Oskar-Fernandes/cinereserve/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Django](https://img.shields.io/badge/Django-6.0-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![Redis](https://img.shields.io/badge/Redis-7-red)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)

API RESTful para sistema de reserva de ingressos do cinema **Cinépolis Natal**.

---

## 🏗️ Arquitetura
```
┌─────────────────────────────────────────────────────┐
│                    CineReserve API                   │
├──────────────┬──────────────┬───────────────────────┤
│    users     │    movies    │     reservations       │
│  ─────────   │  ─────────   │  ─────────────────     │
│  Registro    │  Filmes      │  Reservar Assento      │
│  Login JWT   │  Sessões     │  Checkout              │
│  Perfil      │  Mapa Asst.  │  Meus Ingressos        │
└──────┬───────┴──────┬───────┴──────────┬────────────┘
       │              │                  │
┌──────▼──────┐ ┌─────▼──────┐ ┌────────▼───────┐
│  PostgreSQL  │ │   Redis    │ │     Celery     │
│  (banco)     │ │  (locks +  │ │  (liberação    │
│              │ │   cache)   │ │   automática)  │
└─────────────┘ └────────────┘ └────────────────┘
```

---

## ⚙️ Tecnologias

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3.12 |
| Framework | Django 6 + Django REST Framework |
| Autenticação | JWT (djangorestframework-simplejwt) |
| Banco de Dados | PostgreSQL 16 |
| Cache / Lock | Redis 7 |
| Tarefas Assíncronas | Celery |
| Documentação | Swagger (drf-spectacular) |
| Testes | pytest + pytest-django |
| Containers | Docker + Docker Compose |
| CI/CD | GitHub Actions |

---

## ✅ Funcionalidades

- Cadastro e autenticação de usuários com JWT
- Listagem de filmes e sessões disponíveis
- Mapa de assentos em tempo real (disponível, reservado, comprado)
- Lock distribuído de 10 minutos por assento via Redis
- Checkout e geração de ingresso digital único
- Portal "Meus Ingressos" com histórico completo
- Rate limiting nos endpoints de autenticação
- Liberação automática de locks expirados via Celery
- Tratamento global de erros com respostas padronizadas
- Endpoint de health check (`/api/health/`)
- Comando de seed para popular o banco com dados de exemplo
- Pipeline CI/CD com GitHub Actions

---

## 🚀 Como Rodar

### Pré-requisitos
- Docker Desktop
- Python 3.12+
- Poetry

### 1. Clone o repositório
```bash
git clone https://github.com/Oskar-Fernandes/cinereserve.git
cd cinereserve
```

### 2. Configure o ambiente
```bash
cp .env.example .env
```

### 3. Instale as dependências
```bash
poetry install
```

### 4. Inicie os serviços
```bash
docker compose up -d db redis
```

### 5. Rode as migrations
```bash
poetry run python manage.py migrate
```

### 6. Popule o banco com dados de exemplo
```bash
poetry run python manage.py seed
```

### 7. Inicie o servidor
```bash
poetry run python manage.py runserver
```

---

## 📖 Documentação da API

Acesse o Swagger em: **http://localhost:8000/api/docs/**

---

## 📡 Endpoints

### Usuários
| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| POST | `/api/users/register/` | Cadastrar usuário | Não |
| POST | `/api/users/login/` | Login (retorna JWT) | Não |
| POST | `/api/users/token/refresh/` | Renovar token | Não |
| GET | `/api/users/profile/` | Ver perfil | Sim |

### Filmes
| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| GET | `/api/movies/` | Listar filmes | Não |
| GET | `/api/movies/{id}/` | Detalhe do filme | Não |
| GET | `/api/movies/{id}/sessions/` | Sessões do filme | Não |
| GET | `/api/movies/sessions/{id}/seats/` | Mapa de assentos | Sim |

### Reservas
| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| POST | `/api/reservations/sessions/{s}/seats/{s}/reserve/` | Reservar assento (lock 10min) | Sim |
| POST | `/api/reservations/sessions/{s}/seats/{s}/checkout/` | Finalizar e gerar ingresso | Sim |
| GET | `/api/reservations/my-tickets/` | Meus ingressos | Sim |

### Sistema
| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| GET | `/api/health/` | Status da API | Não |
| GET | `/api/docs/` | Documentação Swagger | Não |

---

## 🧪 Rodando os Testes
```bash
poetry run pytest
```

---

## 🐳 Docker
```bash
# Iniciar todos os serviços
docker compose up -d

# Parar todos os serviços
docker compose down
```

---

## 📁 Estrutura do Projeto
```
cinereserve/
├── core/               # Configurações Django, URLs, Celery
├── users/              # Cadastro e autenticação
├── movies/             # Filmes, sessões e assentos
├── reservations/       # Reservas e ingressos
├── .github/workflows/  # CI/CD GitHub Actions
├── docker-compose.yml
├── Dockerfile
└── pyproject.toml
```