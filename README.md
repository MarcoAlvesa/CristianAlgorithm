# Sistema de Sincronização NTP - Algoritmo de Cristian

![Docker](https://img.shields.io/badge/Docker-3.8+-blue?logo=docker)
![Python](https://img.shields.io/badge/Python-3.9+-yellow?logo=python)

## 📌 Visão Geral
Implementação didática do algoritmo de Cristian para sincronização de relógios em sistemas distribuídos, simulando:
- Um servidor NTP central
- Três clientes com diferentes drifts temporais (+3h, +6h, +9h)

**Destaques**:
- Protocolo UDP personalizado (inspirado no NTP)
- Ajuste gradual de relógios (5% por ciclo)
- Ambiente containerizado com Docker

## 🛠️ Tecnologias
- `Python 3.9`
- `Docker Compose`
- `NTP` (protocolo simplificado)

## ⚙️ Configuração

### Pré-requisitos
```bash
docker-compose version  # >= 3.8
python --version       # >= 3.9
```
## 🚀 Como Rodar o Projeto
# Construa e inicie os containers
```bash
docker-compose build && docker-compose up
```