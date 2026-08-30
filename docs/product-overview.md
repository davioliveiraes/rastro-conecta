# Visão do produto

## Visão do Rastro

Rastro é uma plataforma de rastreamento, atribuição e inteligência de marketing que acompanha a jornada do lead desde sua origem em uma campanha até o resultado comercial. Integrações são o meio técnico usado para reunir eventos que hoje ficam fragmentados entre mídia, comunicação e vendas.

O produto transforma esses eventos em uma jornada comercial rastreável e busca responder três perguntas centrais:

1. De onde veio esse lead?
2. Esse lead era qualificado?
3. O que esse lead gerou para o negócio?

```text
ORIGEM → QUALIDADE → RESULTADO
```

Sua regra orientadora é:

> Isso ajuda o Rastro a conectar de forma confiável a origem, a conversa, o lead, sua qualidade e o resultado comercial?

## Problema

Anúncios, conversas no WhatsApp, contatos, leads, atividades comerciais e vendas produzem dados em sistemas diferentes. Sem vínculos confiáveis entre esses eventos, a empresa pode saber quanto uma campanha gastou ou quantos leads gerou, mas não necessariamente quais leads eram qualificados, por que foram desqualificados e quais origens produziram oportunidades, vendas e receita.

## Proposta de valor

O Rastro conecta dados de mídia, comunicação e vendas para reconstruir o caminho entre origem, qualidade e resultado. Seu diferencial é permitir análises como quais campanhas geram os melhores leads, quais anúncios atraem leads desqualificados, quais motivos reduzem a qualidade comercial e qual investimento efetivamente produz vendas e receita.

## Jornada principal

```text
Anúncio
↓
WhatsApp
↓
Lead
↓
Qualificação
↓
Qualificado / Desqualificado
↓
Oportunidade
↓
Venda
↓
Receita
```

O fluxo de integração que sustenta essa jornada continua sendo:

```text
Meta Ads → WhatsApp → Rastro → CRM → Venda → Rastro → Meta
```

## Rastreamento no Rastro

Rastreamento significa acompanhar eventos de marketing e eventos comerciais relacionados à jornada de um lead. Não se refere a localização física, GPS, espionagem de usuários ou monitoramento genérico de navegação.

O caminho rastreável pode incluir, conforme os dados disponíveis:

```text
Meta Ads
↓
Campanha
↓
Conjunto
↓
Anúncio
↓
Click-to-WhatsApp
↓
Conversa
↓
Lead
↓
Qualificação
↓
Negociação
↓
Venda
```

### Tracking de origem

Uma responsabilidade do Rastro é reconstruir a origem do lead. Quando disponíveis, dados como `ad_account_id`, `campaign_id`, `adset_id`, `ad_id`, `creative_id`, `ctwa_clid`, `conversation_id`, contato, telefone, timestamps e parâmetros de origem poderão compor as evidências dessa relação.

A finalidade é responder qual conta, campanha, conjunto, anúncio ou criativo originou o lead, sem antecipar nesta documentação a estrutura técnica definitiva desses dados.

### Tracking comercial

O rastreamento continua depois da entrada do lead. Conceitualmente, o Rastro deverá acompanhar acontecimentos como:

```text
Lead recebido
↓
Em atendimento
↓
Qualificação
↓
Qualificado / Desqualificado
↓
Negociação
↓
Venda
```

Esse fluxo não define o pipeline comercial final. Ele estabelece que o produto precisa compreender o que acontece com o lead depois da conversa inicial.

### Histórico da jornada

Quando apropriado, o Rastro deverá preservar o histórico que explica a evolução do lead. Um histórico poderá registrar, por exemplo, o recebimento do lead, o início do atendimento, sua qualificação, o começo de uma negociação e a venda. Para um lead desqualificado, poderá registrar também quando isso ocorreu e o respectivo motivo.

Exemplos meramente ilustrativos:

```text
13:42 Lead recebido
13:45 Atendimento iniciado
14:03 Marcado como qualificado
15:18 Negociação iniciada
17:36 Venda realizada
```

```text
13:42 Lead recebido
13:49 Atendimento iniciado
14:10 Marcado como desqualificado
Motivo: sem capacidade de pagamento
```

A implementação técnica desse histórico permanece em aberto. O requisito é permitir reconstruir o “rastro” do lead de forma compreensível e auditável.

## Qualidade do lead

A qualificação é parte central do produto. O conceito inicial deve permitir ao menos os estados:

- `pending` — Pendente;
- `qualified` — Qualificado;
- `disqualified` — Desqualificado.

Esses valores representam uma direção inicial, não uma definição definitiva de enum ou schema.

### Qualificação e etapa comercial

Qualidade do lead e etapa comercial são dimensões diferentes:

| Dimensão | Pergunta respondida | Exemplos conceituais |
| --- | --- | --- |
| `qualification_status` | O lead atende aos critérios de qualidade? | `pending`, `qualified`, `disqualified` |
| `stage` | Em que ponto da jornada comercial o lead está? | `new`, `contacted`, `negotiation`, `won`, `lost` |

Um lead pode estar **qualificado** e, ao mesmo tempo, na etapa de **negociação**. Essa separação evita usar o pipeline comercial como substituto da avaliação de qualidade.

### Classificação manual no MVP

Inicialmente, a qualificação poderá ser feita manualmente dentro do Rastro como Pendente, Qualificado ou Desqualificado. Em etapas futuras, essa informação poderá ser recebida ou sincronizada por integrações com CRMs externos.

Essa abordagem permite validar o conceito de qualidade antes de depender de automações comerciais mais complexas.

### Motivos de desqualificação

Um lead desqualificado poderá ter um motivo associado. Exemplos incluem falta de capacidade de pagamento, não atendimento aos critérios, região não atendida, produto indisponível, pesquisa de preço, ausência de resposta, contato inválido ou outro motivo relevante.

Essa lista é apenas ilustrativa e não representa um enum definitivo. A estrutura final será decidida quando a funcionalidade for implementada. O valor desse dado é responder não apenas quantos leads foram desqualificados, mas por que isso aconteceu.

## Atribuição e inteligência

O attribution engine permanece como domínio central. Ele deverá contribuir para relacionar evidências de origem não apenas ao lead, mas também à sua qualificação, oportunidade, venda e receita.

A atribuição deve ser explícita, auditável, baseada em evidências e explicável sempre que possível. Entre as perguntas que deverá apoiar estão:

- Qual origem gerou este lead?
- Qual origem gerou este lead qualificado?
- Qual origem gerou esta oportunidade?
- Qual origem gerou esta venda?
- Qual origem gerou esta receita?

### Valor da qualificação para marketing

Volume e CPL isolados não determinam a qualidade de uma campanha. Uma campanha pode gerar mais leads e ter CPL menor, enquanto outra produz proporcionalmente mais leads qualificados, oportunidades ou vendas. O Rastro deverá conectar qualidade e resultado à origem para tornar essa diferença visível.

### Métricas

As análises previstas incluem:

- leads, leads qualificados e leads desqualificados;
- taxa de qualificação e taxa de desqualificação;
- CPL e CPQL;
- custo por conversa;
- oportunidades e vendas;
- CAC, faturamento e ROAS;
- taxa de fechamento.

O **CPQL — Custo por Lead Qualificado** recebe destaque porque permite ir além do custo por lead:

```text
CPQL = investimento / leads qualificados
```

Essas métricas poderão futuramente ser analisadas por conta de anúncios, campanha, conjunto, anúncio e criativo. Uma visão por origem poderá reunir investimento, conversas, leads, qualidade, oportunidades, vendas, receita e seus indicadores derivados, sem que isso implique a definição de um dashboard nesta etapa.

## Relação com CRM

O Rastro não pretende substituir o CRM. O CRM poderá permanecer como sistema operacional da equipe comercial, enquanto o Rastro funciona como camada de rastreamento, integração, atribuição e inteligência.

No MVP, a qualificação poderá ser registrada no próprio Rastro. Posteriormente, status de qualificação, etapas e resultados poderão ser sincronizados com CRMs externos conforme os contratos de cada integração.

## Fechamento do ciclo com a Meta

Conceitualmente, o ciclo poderá ser fechado da seguinte forma:

```text
Meta Ads
↓
WhatsApp
↓
Rastro
↓
Lead
↓
Qualificação
↓
Venda
↓
Rastro
↓
Conversions API
↓
Meta
```

Eventos futuros poderão representar acontecimentos como Lead, Qualified Lead, Opportunity e Purchase. Os nomes, formatos e condições de envio não estão definidos: dependerão das APIs e dos contratos adotados na implementação.

## Objetivo do MVP

O MVP deverá provar que o Rastro consegue:

1. identificar a origem de um lead;
2. acompanhar sua jornada depois da entrada;
3. classificá-lo como pendente, qualificado ou desqualificado;
4. relacionar essa classificação à origem de marketing;
5. relacionar posteriormente venda e receita ao mesmo caminho;
6. gerar inteligência sobre quais campanhas trazem bons leads e resultados comerciais.

O fluxo conceitual revisado é:

```text
Meta Ads → WhatsApp → Rastro → Lead → Qualificado / Desqualificado → CRM / Resultado comercial → Venda → Rastro → Meta
```

## O que o Rastro não pretende ser

O Rastro não é definido como dashboard, ferramenta de Meta Ads, CRM, sistema de WhatsApp, plataforma genérica de integração ou ferramenta isolada de relatórios. Esses sistemas e capacidades podem participar do fluxo, mas a finalidade central do Rastro é tornar a jornada comercial do lead rastreável e relacionar origem, qualidade e resultado.

O produto também não pretende substituir o gerenciador de anúncios da Meta, o WhatsApp ou os CRMs externos.
