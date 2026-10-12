# Arquitetura do Sistema

## 1. Visão geral

O projeto implementa um pipeline de ingestão de séries temporais econômicas, seguindo princípios de Clean Architecture, separação de responsabilidades e inversão de dependências.

O sistema foi dividido em três camadas:

- **Domain:** representação das informações econômicas.
- **Application:** contratos e coordenação dos casos de uso.
- **Infrastructure:** comunicação com a API do Bacen e persistência PostgreSQL.

A arquitetura busca preservar a lógica da aplicação quando tecnologias externas são substituídas.

## 2. Fluxo de execução

```text
Banco Central — API SGS
          |
          v
     BacenAdapter
          |
          v
    Observation
          |
          v
 ImportEconomicSeries
          |
          v
  PostgresRepository
          |
          v
      PostgreSQL
```

O fluxo representa a execução da ingestão, não a direção das dependências de código.

## 3. Responsabilidades das camadas

### Domain

Arquivo: `src/domain/entities.py`

Define a classe `Observation`, que representa uma observação de uma série econômica.

A entidade contém identificador da série, data e valor.

A implementação utiliza `dataclass(frozen=True)` para criar objetos com atributos não reatribuíveis pela interface convencional.

As anotações de tipo não realizam validação automática durante a execução.

### Application

Arquivos:

- `src/application/ports/data_provider.py`
- `src/application/ports/repository.py`
- `src/application/use_cases/import_series.py`

O contrato `DataProvider` define como obter observações.

O contrato `ObservationRepository` define como persisti-las.

O caso de uso `ImportEconomicSeries` coordena essas operações sem conhecer as implementações concretas.

### Infrastructure

Arquivos:

- `src/infrastructure/providers/bacen.py`
- `src/infrastructure/database/postgres_repository.py`

O `BacenAdapter` realiza requisições HTTP, interpreta o JSON e converte os registros em objetos `Observation`.

O `PostgresRepository` estabelece a conexão com PostgreSQL, cria a tabela necessária e persiste as observações.

## 4. Inversão de dependências

A aplicação depende de abstrações, não diretamente do Bacen ou PostgreSQL.

A infraestrutura fornece implementações compatíveis com os contratos definidos na aplicação.

Isso permite desenvolver outros adaptadores e repositórios preservando o caso de uso, desde que respeitem o contrato e a semântica dos dados.

O arquivo `src/main.py` funciona como *composition root*: configura as implementações concretas e as conecta ao caso de uso.

## 5. Persistência e idempotência

A tabela `observations` possui chave primária composta por:

- `series_id`
- `observation_date`

A persistência utiliza `INSERT ... ON CONFLICT DO UPDATE`.

Com isso, uma observação já existente é atualizada em vez de gerar uma linha duplicada.

A reexecução com as mesmas dez observações foi validada manualmente e manteve dez registros no PostgreSQL.

## 6. Estratégia de testes

Os testes automatizados utilizam um provedor simulado e um repositório em memória.

Eles verificam:

- Importação de observações.
- Comportamento quando não existem registros.

Esses testes são independentes do Bacen e do PostgreSQL.

A integração real e a execução em um clone limpo foram verificadas manualmente.

## 7. Decisões e limitações

O projeto prioriza um MVP funcional e reproduzível.

**Decisões:**

- Utilização de `Protocol` para definir contratos.
- Separação entre entidades de domínio e detalhes de infraestrutura.
- PostgreSQL com upsert para evitar duplicações.
- Docker Compose para gerenciar os serviços.
- Make para oferecer uma interface simples de execução.

**Limitações:**

- A aplicação consulta as dez observações mais recentes, sem ingestão histórica incremental.
- O schema é criado pela aplicação, sem migrações versionadas.
- Ainda não existem testes automatizados de integração com PostgreSQL.
- A entidade não implementa validação explícita de tipos em tempo de execução.
- O projeto utiliza princípios de modelagem de domínio, mas não pretende implementar todos os padrões de DDD.

Essas limitações foram mantidas para preservar o escopo do desafio e a simplicidade operacional.