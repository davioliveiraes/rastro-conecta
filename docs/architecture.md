# Arquitetura

Este documento registra somente as decisões arquiteturais iniciais do Rastro. Detalhes de implementação serão definidos à medida que o produto evoluir e as necessidades forem validadas.

## Princípio orientador

A arquitetura deve ajudar o Rastro a conectar de forma confiável a origem, a conversa, o lead, sua qualidade e o resultado comercial. Simplicidade operacional, separação clara de responsabilidades, manutenção e rastreabilidade têm prioridade sobre abstrações prematuras.

## Monólito modular

O sistema começará como um monólito modular. Backend e regras de negócio serão implantados como uma única aplicação, com limites internos claros entre responsabilidades. Essa escolha reduz a complexidade inicial e não pressupõe uma futura divisão em microserviços.

## Tecnologias planejadas

- O backend é desenvolvido em Python com FastAPI.
- O frontend será desenvolvido futuramente em React com TypeScript.
- PostgreSQL é o banco de dados principal.
- Redis será adotado apenas quando houver uma necessidade concreta que justifique seu uso.

O backend possui a base HTTP e a fundação de persistência. Cache e os demais componentes de infraestrutura permanecem para etapas futuras.

## Persistência

A persistência utiliza PostgreSQL, com SQLAlchemy 2 em modo síncrono e Psycopg 3 como driver. Sessões, engine e base declarativa ficam centralizadas em `app/core/database.py`, sem abrir conexão durante a importação da aplicação.

Migrações são gerenciadas pelo Alembic, que lê a mesma `DATABASE_URL` usada pela aplicação através das settings. A primeira migration estabelece somente a fundação multi-tenant; entidades dos domínios de tracking, qualificação e atribuição permanecem para etapas futuras.

## Domínios conceituais

### Rastreamento da jornada

Tracking é um domínio importante do Rastro e representa a correlação de eventos de marketing e eventos comerciais ao longo da jornada do lead. O sistema deverá preservar evidências suficientes para reconstruir origem, mudanças relevantes de qualidade e resultados, sem definir antecipadamente um modelo definitivo de eventos.

### Qualificação e etapa comercial

`qualification_status` e `stage` representam conceitos diferentes e deverão permanecer separados. O primeiro descreve se o lead está pendente, qualificado ou desqualificado; o segundo descreve sua posição na jornada comercial. Essa distinção deverá orientar futuros modelos e integrações, mas não define agora enums ou schemas finais.

### Histórico e auditoria

Mudanças relevantes da jornada deverão ser historicamente explicáveis quando necessário. A arquitetura futura deve permitir identificar o que aconteceu, quando aconteceu e qual evidência sustenta uma atribuição ou classificação, sem antecipar nesta etapa a forma de armazenamento desse histórico.

## Integrações externas

Integrações com Meta, WhatsApp e CRMs externos deverão ficar atrás de providers ou adapters. Esse limite evita espalhar detalhes de APIs externas pelo domínio e permite que contratos, autenticação e mudanças de cada fornecedor sejam tratados no ponto apropriado.

O CRM não será substituído pelo Rastro: ele poderá continuar como sistema operacional comercial e atuar como provider de qualificações, etapas e resultados. No MVP, parte dessas informações poderá ser registrada diretamente no Rastro antes da automação com CRMs.

O fechamento do ciclo com a Meta poderá futuramente comunicar eventos comerciais relevantes por meio da Conversions API. Nomes e contratos de eventos serão definidos conforme as APIs utilizadas, sem pressupor agora um formato definitivo.

## Multi-tenancy

`Organization` representa o tenant no Rastro. Um `User` pode participar de múltiplas organizações, e uma organização pode possuir múltiplos usuários; a entidade explícita `OrganizationUser` representa essa associação N:N e registra o papel básico do membro.

`User` não possui `organization_id` por decisão intencional. Recursos de domínio pertencentes a um tenant deverão possuir `organization_id`, e suas futuras consultas deverão sempre considerar o contexto da organização para preservar o isolamento de dados.

As três entidades criam apenas a fundação estrutural do multi-tenancy. Autenticação, autorização, resolução do contexto da organização, filtros automáticos e mecanismos como PostgreSQL Row Level Security não estão implementados e serão avaliados em etapas posteriores.

### Request Identity

A resolução da identidade do usuário é separada da seleção do tenant. Durante o desenvolvimento e os testes, `X-Rastro-User-Id` funciona como fonte temporária de identidade e somente é aceito nos ambientes `development` e `test`. Esse header não é autenticação e é explicitamente recusado em `production`; o resolvedor deverá ser substituído por autenticação real antes do uso produtivo.

A identidade temporária somente é considerada válida quando o UUID corresponde a um `User` existente e ativo. A futura adoção de JWT, OAuth ou outro provedor de identidade não deverá alterar as regras de membership e isolamento do tenant.

### Tenant Context

A organização ativa é selecionada por requisição com `X-Rastro-Organization-Id`; ela não é persistida como atributo do usuário. A seleção somente é aceita quando existe uma `OrganizationUser` ligando o usuário atual à organização informada.

Após essa validação, uma dependency do FastAPI produz um `RequestContext` imutável com `user_id`, `organization_id` e o `role` da membership. O contexto pertence exclusivamente à requisição e não utiliza estado global mutável.

### Tenant Isolation

Recursos futuros pertencentes a uma organização deverão ser consultados combinando o identificador do recurso com `context.organization_id`. Conhecer um UUID não concede acesso: UUID não substitui autorização, e toda operação multi-tenant deverá considerar a organização atual para prevenir acesso cruzado e vulnerabilidades como IDOR ou Broken Object Level Authorization.

Essa regra estabelece a base de isolamento, mas não implementa RBAC completo, middleware global, filtros automáticos nem PostgreSQL Row Level Security.

## Webhooks e idempotência

Webhooks serão uma entrada importante para eventos produzidos por sistemas externos. Seu processamento deverá considerar validação da origem, rastreabilidade, falhas e reenvios.

Como o mesmo evento pode ser recebido mais de uma vez, idempotência é um requisito arquitetural. Operações repetidas não devem gerar contatos, leads, mudanças de qualificação, resultados ou atribuições duplicadas.

## Domínio central de atribuição

O attribution engine será um domínio central do Rastro. Ele deverá relacionar evidências de origem aos eventos da jornada e contribuir para explicar qual origem gerou um lead, um lead qualificado, uma oportunidade, uma venda ou uma receita.

A atribuição deverá permanecer explícita, auditável, baseada em evidências e explicável sempre que possível. Regras, modelos e estratégias específicas serão definidos em etapas posteriores.

## Segurança de credenciais

Credenciais de integrações externas deverão ser protegidas, ter acesso restrito e nunca ser incorporadas ao código-fonte ou expostas em logs. Os mecanismos concretos de armazenamento, criptografia e rotação serão definidos quando as integrações forem implementadas.

## Evolução incremental

A arquitetura evoluirá conforme o fluxo principal for validado. Novos componentes e abstrações só deverão ser adicionados quando resolverem necessidades concretas, preservando o monólito modular e evitando dependências desnecessárias.
