# Ingestão de Séries Econômicas

Pipeline de ingestão de dados econômicos desenvolvido em Python, aplicando princípios de **Domain-Driven Design (DDD), Clean Architecture e Dependency Inversion**.

O sistema consulta séries temporais disponibilizadas pelo Banco Central do Brasil, transforma os registros em entidades de domínio e realiza a persistência em PostgreSQL.

A aplicação foi projetada para permitir a substituição de provedores de dados e mecanismos de persistência sem modificar a lógica central.

## Quick Start

### Pré-requisitos

- Docker Engine / Docker Desktop com Docker Compose
- GNU Make
- Git

Não é necessário instalar Python ou PostgreSQL localmente para executar a ingestão.

### Executar

```bash
git clone https://github.com/Juan-Sotomayor/economic-series-ingestion.git
cd economic-series-ingestion
make up
```

O comando inicializa o PostgreSQL, constrói a imagem da aplicação e executa a ingestão da série configurada.

O arquivo `.env` é criado automaticamente a partir de `.env.example`, caso ainda não exista.

**Resultado esperado:**

```text
Ingestão concluída: 10 observações processadas.
```

A aplicação está inicialmente configurada para consultar as dez observações mais recentes da série 11 do SGS (Selic diária).

### Verificar a persistência

Execute:

```bash
docker compose exec -T db sh -c \
'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT COUNT(*) AS total FROM observations;"'
```

O resultado esperado após a primeira execução é uma tabela com dez registros.

A execução pode ser repetida utilizando `make up`. A persistência utiliza uma chave composta e `ON CONFLICT DO UPDATE` para evitar duplicações de observações com a mesma série e data.

### Encerrar os serviços

```bash
docker compose down
```

Esse comando remove os contêineres e a rede do projeto, preservando o volume de dados.

Para remover também o volume e reiniciar o banco do zero:

```bash
docker compose down -v
```

**Atenção:** a segunda opção exclui os dados persistidos nesse volume.

## Arquitetura

A aplicação é organizada em três camadas:

| Camada | Responsabilidade |
|---|---|
| Domain | Representação das observações econômicas, independente de serviços externos |
| Application | Contratos e caso de uso que coordena a ingestão |
| Infrastructure | Integração com a API do Bacen e persistência PostgreSQL |

O fluxo principal é:

```text
Banco Central (API SGS)
         |
         v
     BacenAdapter
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

O caso de uso depende de contratos (`DataProvider` e `ObservationRepository`), e não diretamente das implementações concretas.

A escolha das implementações ocorre no ponto de entrada da aplicação.

As decisões arquiteturais e responsabilidades dos componentes serão detalhadas em `docs/architecture.md`.

## Estrutura do projeto

```text
src/
├── domain/
│   └── entities.py
├── application/
│   ├── ports/
│   │   ├── data_provider.py
│   │   └── repository.py
│   └── use_cases/
│       └── import_series.py
├── infrastructure/
│   ├── providers/
│   │   └── bacen.py
│   └── database/
│       └── postgres_repository.py
└── main.py

tests/
scripts/
compose.yaml
Dockerfile
Makefile
requirements.txt
requirements-dev.txt
```

## Decisões técnicas

**Abstração de provedores**

O contrato `DataProvider` define a obtenção de observações, permitindo implementar outros adaptadores sem alterar o caso de uso.

**Abstração da persistência**

O contrato `ObservationRepository` separa as operações de armazenamento da tecnologia utilizada.

**Modelo de domínio independente**

As observações são representadas por uma `dataclass`, utilizando tipos Python como `date` e `Decimal`.

**Idempotência na persistência**

A combinação de identificador da série e data é utilizada como chave primária. O PostgreSQL executa upsert para evitar a criação de registros duplicados na reimportação.

**Execução reproduzível**

Docker Compose e Make automatizam as dependências e a execução da aplicação.

## Testes

Os testes unitários utilizam implementações simuladas do provedor e do repositório, permitindo validar o caso de uso sem conexão com serviços externos.

Para executar localmente, com Python e suporte a ambientes virtuais instalados:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pytest -v
```

Os testes atualmente contemplam:

- Importação de observações fornecidas por um provedor simulado.
- Comportamento da aplicação quando o provedor não retorna registros.

A integração com PostgreSQL e a reexecução sem duplicações também foram verificadas manualmente.

## Tecnologias

- Python
- PostgreSQL
- psycopg
- Docker / Docker Compose
- GNU Make
- pytest
- Git / GitHub

## Limitações e próximos passos

Esta implementação é um MVP focado em separação de responsabilidades, integração e reprodutibilidade.

Possíveis melhorias:

- Introduzir migrações versionadas para o schema do banco.
- Ampliar os testes automatizados de integração.
- Adicionar outros provedores de séries econômicas.
- Implementar ingestão incremental por intervalos de datas.
- Evoluir observabilidade e tratamento de falhas externas.

## Fonte de dados

[Banco Central do Brasil — Portal de Dados Abertos](https://dadosabertos.bcb.gov.br/)