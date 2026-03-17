
# 🎬 CineReserve API

![CI](https://github.com/Oskar-Fernandes/cinereserve/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.12+-blue)
![Django](https://img.shields.io/badge/Django-6.0-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![Redis](https://img.shields.io/badge/Redis-7-red)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

> API RESTful para sistema de reserva de ingressos do cinema **Cinepolis Natal**.

---

## 🏗️ Arquitetura
```
┌─────────────────────────────────────────────────────────┐
│                     CineReserve API                      │
├──────────────┬──────────────┬───────────────────────────┤
│    users     │    movies    │       reservations         │
│  Registro    │  Filmes      │  Reservar Assento          │
│  Login JWT   │  Sessoes     │  Checkout                  │
│  Perfil      │  Mapa Asst.  │  Meus Ingressos            │
└──────┬───────┴──────┬───────┴──────────┬────────────────┘
       │              │                  │
┌──────▼──────┐ ┌─────▼──────┐ ┌────────▼────────────────┐
│  PostgreSQL  │ │   Redis    │ │        Celery            │
│  (banco)     │ │  (locks +  │ │  - Auto-release locks    │
│              │ │   cache)   │ │  - Email confirmacao     │
└─────────────┘ └────────────┘ └─────────────────────────┘
```

---

## ⚙️ Tecnologias

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3.12+ |
| Framework | Django 6 + Django REST Framework |
| Autenticacao | JWT (djangorestframework-simplejwt) |
| Banco de Dados | PostgreSQL 16 |
| Cache / Lock Distribuido | Redis 7 |
| Tarefas Assincronas | Celery |
| Email | Mailtrap (SMTP Sandbox) |
| Documentacao | Swagger (drf-spectacular) |
| Testes | pytest + pytest-django |
| Containers | Docker + Docker Compose |
| CI/CD | GitHub Actions |

---

## ✅ Funcionalidades

### Requisitos Tecnicos
- [x] API RESTful com Django REST Framework e Poetry
- [x] Autenticacao JWT
- [x] Banco de dados PostgreSQL
- [x] Redis como distributed lock para reservas temporarias
- [x] Cache Redis nos endpoints de alta leitura (filmes e sessoes)
- [x] Paginacao em todos os endpoints de listagem
- [x] Testes unitarios e de integracao (9/9 passando)
- [x] Documentacao Swagger em `/api/docs/`
- [x] Docker + Docker Compose
- [x] Repositorio publico no GitHub

### Casos de Uso
- [x] Cadastro e login com JWT
- [x] Listagem de filmes disponiveis
- [x] Listagem de sessoes por filme
- [x] Mapa de assentos em tempo real (disponivel, reservado, comprado)
- [x] Lock distribuido de 10 minutos por assento via Redis
- [x] Checkout e geracao de ingresso digital unico
- [x] Portal "Meus Ingressos" com historico completo

### Bonus
- [x] Rate limiting nos endpoints de autenticacao
- [x] Celery para liberacao automatica de locks expirados
- [x] Celery para envio de email de confirmacao apos checkout
- [x] Pipeline CI/CD com GitHub Actions
- [x] Health check endpoint
- [x] Seed de dados de exemplo
- [x] Tratamento global de erros padronizado

---

## 🚀 Como Rodar

### Pre-requisitos
- Docker Desktop instalado e rodando
- Python 3.12+
- Poetry

### 1. Clone o repositorio
```bash
git clone https://github.com/Oskar-Fernandes/cinereserve.git
cd cinereserve
```

### 2. Configure o ambiente
```bash
cp .env.example .env
```

Edite o `.env` com suas credenciais se necessario.

### 3. Instale as dependencias
```bash
poetry install
```

### 4. Inicie os servicos (PostgreSQL + Redis)
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

### 7. Crie o superusuario (opcional)
```bash
poetry run python manage.py createsuperuser
```

### 8. Inicie o servidor
```bash
poetry run python manage.py runserver
```

Acesse: **http://localhost:8000/api/docs/**

---

## 📖 Documentacao da API

| URL | Descricao |
|-----|-----------|
| http://localhost:8000/api/docs/ | Swagger UI |
| http://localhost:8000/api/health/ | Health Check |
| http://localhost:8000/admin/ | Painel Admin |

---

## 📡 Endpoints

### Usuarios
| Metodo | Endpoint | Descricao | Auth |
|--------|----------|-----------|------|
| POST | `/api/users/register/` | Cadastrar usuario | Nao |
| POST | `/api/users/login/` | Login (retorna JWT) | Nao |
| POST | `/api/users/token/refresh/` | Renovar token | Nao |
| GET | `/api/users/profile/` | Ver perfil | Sim |

### Filmes
| Metodo | Endpoint | Descricao | Auth |
|--------|----------|-----------|------|
| GET | `/api/movies/` | Listar filmes | Nao |
| GET | `/api/movies/{id}/` | Detalhe do filme | Nao |
| GET | `/api/movies/{id}/sessions/` | Sessoes do filme | Nao |
| GET | `/api/movies/sessions/{id}/seats/` | Mapa de assentos | Sim |

### Reservas
| Metodo | Endpoint | Descricao | Auth |
|--------|----------|-----------|------|
| POST | `/api/reservations/sessions/{s}/seats/{s}/reserve/` | Reservar assento (lock 10min) | Sim |
| POST | `/api/reservations/sessions/{s}/seats/{s}/checkout/` | Finalizar e gerar ingresso | Sim |
| GET | `/api/reservations/my-tickets/` | Meus ingressos | Sim |

### Sistema
| Metodo | Endpoint | Descricao | Auth |
|--------|----------|-----------|------|
| GET | `/api/health/` | Status da API | Nao |
| GET | `/api/docs/` | Documentacao Swagger | Nao |

---

## 🔄 Fluxo de Reserva
```
1. POST /api/users/login/          → Obter token JWT
2. GET  /api/movies/               → Listar filmes
3. GET  /api/movies/{id}/sessions/ → Ver sessoes disponiveis
4. GET  /api/movies/sessions/{id}/seats/ → Ver mapa de assentos
5. POST /api/reservations/.../reserve/  → Reservar assento (lock 10min)
6. POST /api/reservations/.../checkout/ → Finalizar compra + email
7. GET  /api/reservations/my-tickets/   → Ver ingressos
```

---

## Como Testar a API pelo Swagger

### Passo 1 - Acesse o Swagger
Abra no navegador: http://localhost:8000/api/docs/

### Passo 2 - Registre um usuario
Clique em POST /api/users/register/ > Try it out > cole o body abaixo > Execute:
```json
{
  "username": "teste",
  "email": "teste@email.com",
  "password": "senha123"
}
```

### Passo 3 - Faca o login
Clique em POST /api/users/login/ > Try it out > cole o body abaixo > Execute:
```json
{
  "email": "teste@email.com",
  "password": "senha123"
}
```

Na resposta, copie o valor do campo "access" (o token JWT).

### Passo 4 - Autorize no Swagger
Clique no botao "Authorize" no canto superior direito da pagina.
Cole APENAS o token no campo Value (sem a palavra Bearer).
Clique em Authorize e depois em Close.

### Passo 5 - Teste o fluxo completo
1. GET /api/movies/ - Liste os filmes
2. GET /api/movies/1/sessions/ - Veja as sessoes do filme 1
3. GET /api/movies/sessions/1/seats/ - Veja o mapa de assentos
4. POST /api/reservations/sessions/1/seats/2/reserve/ - Reserve o assento 2
5. POST /api/reservations/sessions/1/seats/2/checkout/ - Finalize a compra
6. GET /api/reservations/my-tickets/ - Veja seus ingressos

## 🧪 Rodando os Testes
```bash
poetry run pytest
```

---

## 🐳 Docker
```bash
# Iniciar todos os servicos
docker compose up -d

# Parar todos os servicos
docker compose down

# Ver logs
docker compose logs -f
```

---

## 📁 Estrutura do Projeto
```
cinereserve/
├── core/                        # Configuracoes Django, URLs, Celery
│   ├── settings.py
│   ├── urls.py
│   ├── celery.py
│   ├── exceptions.py
│   └── views.py
├── users/                       # Cadastro e autenticacao
├── movies/                      # Filmes, sessoes e assentos
│   └── management/commands/     # Comando seed
├── reservations/                # Reservas e ingressos
├── .github/workflows/ci.yml     # CI/CD GitHub Actions
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
└── .env.example
```

---

## 🔒 Seguranca

- JWT com expiracao de 1 hora (refresh de 7 dias)
- Rate limiting: 5 req/min no registro, 10 req/min no login
- Variaveis sensiveis isoladas no `.env`
- `.env` nunca commitado no repositorio
'@ | Set-Content README.md -Encoding UTF8