# Rastro

Rastro é uma plataforma de integração, atribuição e inteligência de marketing. Seu propósito é conectar eventos hoje distribuídos entre anúncios, conversas, contatos, leads e vendas para reconstruir uma jornada de marketing compreensível e confiável.

> O projeto está em desenvolvimento. A documentação e as decisões técnicas evoluirão de forma incremental.

## Problema

O caminho entre uma campanha e a receita costuma ficar fragmentado em plataformas diferentes. Essa fragmentação dificulta relacionar um anúncio à conversa iniciada, ao lead criado no CRM e à venda concluída, reduzindo a qualidade da atribuição e do aprendizado de marketing.

## Fluxo principal

```text
Meta Ads → WhatsApp → Rastro → CRM → Venda → Rastro → Meta
```

## Objetivo do MVP

O MVP deverá conectar os eventos essenciais desse fluxo e preservar os vínculos necessários para explicar o caminho entre anúncio, conversa, lead e venda. O escopo será detalhado e implementado em etapas, priorizando confiabilidade e simplicidade.

## Stack planejada

- **Backend:** Python, FastAPI, SQLAlchemy, Alembic e Pytest
- **Frontend:** React e TypeScript
- **Dados:** PostgreSQL e Redis quando necessário
- **Infraestrutura:** Docker e Docker Compose

A adoção dessas tecnologias será incremental. Nesta etapa, somente a base HTTP do backend com FastAPI está configurada.

## Arquitetura inicial

O Rastro começará como um monólito modular. Essa abordagem mantém a operação simples enquanto permite separar responsabilidades e domínios com clareza, sem antecipar a complexidade de uma arquitetura distribuída.

As decisões iniciais estão registradas em [`docs/architecture.md`](docs/architecture.md), e a visão do produto em [`docs/product-overview.md`](docs/product-overview.md).

## Estrutura do repositório

```text
rastro-conecta/
├── .github/     # Configurações futuras do repositório
├── backend/     # Aplicação backend
├── docs/        # Documentação do produto e da arquitetura
├── frontend/    # Aplicação frontend
├── infra/       # Definições de infraestrutura
├── scripts/     # Scripts auxiliares do projeto
├── .gitignore
└── README.md
```

## Backend

Os comandos abaixo devem ser executados a partir de `backend/`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

A aplicação funciona com os valores padrão e não exige um arquivo `.env`. Quando necessário, `backend/.env.example` pode ser usado como referência para sobrescrever a configuração local.

Para iniciar a API em modo de desenvolvimento:

```powershell
uvicorn app.main:app --reload
```

Para executar os testes:

```powershell
pytest
```

Endpoint disponível nesta etapa:

- `GET /api/v1/health` — confirma que a aplicação HTTP está respondendo.
