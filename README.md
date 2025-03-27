# Projeto de Monitoramento de Distância com ESP32, FastAPI e Streamlit
Este projeto consiste em um sistema de monitoramento de distância utilizando uma placa ESP32, um sensor ultrassônico HC-SR04, uma API desenvolvida em FastAPI para armazenar os dados em um banco MySQL e um dashboard em Streamlit para visualização dos dados.

## Visão Geral
O sistema coleta dados de distância a cada 10 segundos através de um sensor conectado à ESP32. Esses dados são enviados para um servidor via HTTP POST, onde são armazenados em um banco de dados MySQL. Uma API desenvolvida em FastAPI fornece os dados para um dashboard em Streamlit, que exibe as últimas leituras de distância.

## Estrutura do Projeto
projeto/
├── backend/               # Código do servidor (FastAPI)
│   ├── api.py             # Endpoints da API
│   ├── config.py          # Configurações (IP, porta, banco de dados)
│   ├── database.py        # Conexão e criação da tabela no MySQL
│   ├── models.py          # Modelos Pydantic para validação de dados
│   └── services.py        # Funções para interagir com o banco de dados
├── esp32/                 # Código da ESP32
│   └── distReg.ini        # Script para leitura do sensor e envio de dados
└── frontend/              # Código do dashboard (Streamlit)
    ├── app.py             # Dashboard para visualização dos dados
    └── requirements.txt   # Dependências do Streamlit


