# Ingestão de Séries Econômicas

Sistema de ingestão de dados econômicos desenvolvido em Python, com foco em **Domain-Driven Design (DDD), Clean Architecture e desacoplamento de serviços**.

## Sobre o projeto

O projeto tem como objetivo desenvolver uma aplicação capaz de consultar séries temporais econômicas disponibilizadas pelo Banco Central do Brasil e persistir os registros em um banco de dados.

O principal desafio está na arquitetura: construir um sistema no qual os provedores de dados e os mecanismos de persistência sejam substituíveis, preservando a lógica central da aplicação.

## Objetivos técnicos

- Consumir dados de uma API pública do Banco Central.
- Modelar entidades de domínio independentes da infraestrutura.
- Organizar a aplicação em três camadas: domínio, aplicação e infraestrutura.
- Implementar contratos para acesso a dados e persistência.
- Persistir registros em um banco de dados.
- Automatizar a execução por meio de Docker Compose e Make.
- Implementar testes para validar o comportamento e o desacoplamento.

## Tecnologias previstas

- Python
- PostgreSQL
- Docker e Docker Compose
- Make
- pytest

## Arquitetura proposta

O sistema será organizado em três camadas:

**Domínio:** entidades, conceitos e regras independentes de tecnologias externas.

**Aplicação:** casos de uso e contratos que coordenam o comportamento do sistema.

**Infraestrutura:** implementações de provedores externos, persistência e configuração técnica.

A documentação das decisões arquiteturais será mantida separadamente, no diretório `docs/`.

## Estado do projeto

**Em desenvolvimento.**

O projeto será construído incrementalmente, começando pela integração com a API e evoluindo para uma aplicação desacoplada, testável e reproduzível.

O objetivo operacional é permitir que a aplicação seja executada por meio do comando `make up`, sem exigir configuração manual dos serviços.

## Fonte dos dados

[Banco Central do Brasil — Portal de Dados Abertos](https://dadosabertos.bcb.gov.br/)