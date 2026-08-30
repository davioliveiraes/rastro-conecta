# Rastro

Rastro é uma plataforma de rastreamento, atribuição e inteligência de marketing que acompanha a jornada do lead desde sua origem em uma campanha até o resultado comercial. O produto conecta anúncios, conversas, leads e vendas para mostrar de onde um lead veio, qual era sua qualidade e o que ele gerou para o negócio.

> O projeto está em desenvolvimento. A documentação e as decisões técnicas evoluirão de forma incremental.

## Problema

O caminho entre uma campanha e a receita costuma ficar fragmentado em plataformas diferentes. Essa fragmentação dificulta identificar a origem do lead, acompanhar sua qualificação, entender por que ele foi desqualificado e relacionar oportunidades, vendas e receita às ações de marketing.

## Princípio do produto

O Rastro busca responder três perguntas centrais:

1. De onde veio esse lead?
2. Esse lead era qualificado?
3. O que esse lead gerou para o negócio?

```text
ORIGEM → QUALIDADE → RESULTADO
```

A regra orientadora do produto é: **isso ajuda o Rastro a conectar de forma confiável a origem, a conversa, o lead, sua qualidade e o resultado comercial?**

## Fluxo principal

```text
Meta Ads → WhatsApp → Rastro → Lead → Qualificado / Desqualificado → CRM / Resultado comercial → Venda → Rastro → Meta
```

## Objetivo do MVP

O MVP deverá provar que o Rastro consegue identificar a origem de um lead, acompanhar sua jornada, classificá-lo inicialmente como pendente, qualificado ou desqualificado e relacionar essa qualidade à origem de marketing. Em seguida, deverá preservar o vínculo com oportunidades, vendas e receita para indicar quais campanhas realmente geram bons leads e resultado comercial.

## Capacidades planejadas

- Reconstruir a origem do lead por conta, campanha, conjunto, anúncio e criativo quando os dados estiverem disponíveis.
- Acompanhar eventos da jornada comercial e preservar seu histórico.
- Separar a qualidade do lead da etapa comercial em que ele se encontra.
- Registrar motivos de desqualificação e permitir análise por origem.
- Atribuir oportunidades, vendas e receita às ações de marketing de forma explicável.
- Analisar métricas como CPL, CPQL, CAC, ROAS e taxas de qualificação e fechamento.

## Stack planejada

- **Backend:** Python, FastAPI, SQLAlchemy, Alembic e Pytest
- **Frontend:** React e TypeScript
- **Dados:** PostgreSQL e Redis quando necessário
- **Infraestrutura:** Docker e Docker Compose

A adoção dessas tecnologias será incremental. Atualmente, o backend possui a base HTTP com FastAPI, a fundação de persistência com PostgreSQL, SQLAlchemy e Alembic e os modelos iniciais de `Organization`, `User` e `OrganizationUser` para a estrutura multi-tenant.

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
Copy-Item .env.example .env
```

O `.env.example` contém somente valores locais de desenvolvimento e pode ser usado como ponto de partida. A aplicação também possui padrões locais equivalentes e continua importável sem um arquivo `.env`.

### PostgreSQL local

Na raiz do repositório, execute:

```powershell
docker compose up -d postgres
docker compose ps
```

O Compose inicia somente o PostgreSQL e mantém seus dados em um volume nomeado.

Para evitar conflito com instalações locais existentes, o banco do Rastro é publicado em `localhost:5433` e continua usando `5432` dentro do container.

### API e testes

A partir de `backend/`, inicie a API em modo de desenvolvimento:

```powershell
uvicorn app.main:app --reload
```

Para executar os testes:

```powershell
pytest
```

Endpoint disponível nesta etapa:

- `GET /api/v1/health` — confirma que a aplicação HTTP está respondendo.

### Alembic

Os comandos do Alembic também devem ser executados a partir de `backend/`:

```powershell
alembic upgrade head
alembic current
alembic history
```

A primeira migration cria somente `organizations`, `users` e `organization_users`. Ela estabelece a associação N:N entre usuários e organizações, sem implementar autenticação, autorização ou recursos de negócio.
