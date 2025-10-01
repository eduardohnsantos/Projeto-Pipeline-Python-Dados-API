# 🌍 Projeto Pipeline de Dados — Clima & Qualidade do Ar

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![pandas](https://img.shields.io/badge/pandas-2.1%2B-yellow?logo=pandas)](https://pandas.pydata.org/)
[![Status](https://img.shields.io/badge/status-em%20desenvolvimento-orange)]()

Este repositório contém um **pipeline de dados em Python** que integra informações climáticas do **OpenWeatherMap** e de qualidade do ar do **OpenAQ**.  
O fluxo segue as etapas de **extração → transformação → qualidade de dados → carga (ETL)** e persiste os dados em formato **Parquet particionado**.

---

## 📚 Sumário

- [Arquitetura](#-arquitetura)
- [Instalação](#-instalação)
- [Configuração](#-configuração)
- [Execução](#-execução)
- [ETL em detalhes](#-etl-em-detalhes)
- [Qualidade de Dados](#-qualidade-de-dados)
- [Saídas](#-saídas)
- [Estrutura de Pastas](#-estrutura-de-pastas)
- [Possíveis Melhorias](#-possíveis-melhorias)
- [Licença](#-licença)

---

## 🏗 Arquitetura

```mermaid
flowchart TD
    A[OpenWeatherMap API ☁️] -->|requests| C[Transformações]
    B[OpenAQ API 🌫️] -->|requests| C[Transformações]
    C --> D[Validação de Qualidade 🔍]
    D --> E[Persistência Parquet 📂]
    E --> F[Notebooks / Visualização 📊]
