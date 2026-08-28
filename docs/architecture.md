# Arquitetura

Este documento registra somente as decisões arquiteturais iniciais do Rastro. Detalhes de implementação serão definidos à medida que o produto evoluir e as necessidades forem validadas.

## Princípio orientador

A arquitetura deve ajudar o Rastro a conectar de forma confiável o anúncio, a conversa, o lead e a venda. Simplicidade operacional, separação clara de responsabilidades, manutenção e rastreabilidade têm prioridade sobre abstrações prematuras.

## Monólito modular

O sistema começará como um monólito modular. Backend e regras de negócio serão implantados como uma única aplicação, com limites internos claros entre responsabilidades. Essa escolha reduz a complexidade inicial e não pressupõe uma futura divisão em microserviços.

## Tecnologias planejadas

- O backend é desenvolvido em Python com FastAPI.
- O frontend será desenvolvido futuramente em React com TypeScript.
- PostgreSQL será o banco de dados principal.
- Redis será adotado apenas quando houver uma necessidade concreta que justifique seu uso.

Nesta etapa, somente a base HTTP do backend e sua configuração estão implementadas. Persistência, cache e infraestrutura permanecem para etapas futuras.

## Integrações externas

Integrações com Meta, WhatsApp e CRMs externos deverão ficar atrás de providers ou adapters. Esse limite evita espalhar detalhes de APIs externas pelo domínio e permite que contratos, autenticação e mudanças de cada fornecedor sejam tratados no ponto apropriado.

## Multi-tenancy

O Rastro deve ser projetado com multi-tenancy em mente. `organization_id` é um conceito importante para associar dados e operações à organização correta e apoiar o isolamento entre clientes. A estratégia detalhada de isolamento será decidida antes da implementação dos dados, sem antecipá-la neste momento.

## Webhooks e idempotência

Webhooks serão uma entrada importante para eventos produzidos por sistemas externos. Seu processamento deverá considerar validação da origem, rastreabilidade, falhas e reenvios.

Como o mesmo evento pode ser recebido mais de uma vez, idempotência é um requisito arquitetural. Operações repetidas não devem gerar contatos, leads, vendas ou atribuições duplicadas.

## Domínio central de atribuição

O attribution engine será um domínio central do Rastro. Ele será responsável por relacionar os eventos da jornada e sustentar uma explicação rastreável do vínculo entre anúncio, conversa, lead, venda e receita. Regras e modelos específicos serão definidos em etapas posteriores.

## Segurança de credenciais

Credenciais de integrações externas deverão ser protegidas, ter acesso restrito e nunca ser incorporadas ao código-fonte ou expostas em logs. Os mecanismos concretos de armazenamento, criptografia e rotação serão definidos quando as integrações forem implementadas.

## Evolução incremental

A arquitetura evoluirá conforme o fluxo principal for validado. Novos componentes e abstrações só deverão ser adicionados quando resolverem necessidades concretas, preservando o monólito modular e evitando dependências desnecessárias.
