# Projeto de Servidor Meteorológico

Este projeto consiste em um sistema de monitoramento de distância utilizando uma placa ESP32, um sensor ultrassônico HC-SR04, uma API desenvolvida em FastAPI para armazenar os dados em um banco MySQL e um dashboard em Streamlit para visualização dos dados.
---

<BR>
<BR>



## **Visão Geral**
O sistema coleta dados de distância a cada 10 segundos através de um sensor conectado à ESP32. Esses dados são enviados para um servidor via HTTP POST, onde são armazenados em um banco de dados MySQL. Uma API desenvolvida em FastAPI fornece os dados para um dashboard em Streamlit, que exibe as últimas leituras de distância em tempo real.
<BR>
O projeto é dividido em três componentes principais:

- ESP32: Responsável pela coleta de dados do sensor e envio para o servidor.

- Backend (FastAPI): Recebe os dados, armazena no banco de dados MySQL e fornece uma API para consulta.

- Frontend (Streamlit): Exibe os dados em um dashboard interativo.


<BR>
<BR>


## **Funcionalidades**

#### Coleta de Dados:
- A ESP32 coleta dados de distância a cada 10 segundos e os envia para o servidor.

#### Armazenamento:
- Os dados são armazenados em um banco de dados MySQL na tabela esp32_sensor.

#### API:
- A API fornece dois endpoints:
  - POST /registrar: Recebe os dados de distância e os armazena no banco.
  - GET /dados: Retorna as últimas 10 leituras de distância.

#### Dashboard:
- Um dashboard em Streamlit exibe as últimas leituras de distância em tempo real.


<BR>
<BR>

## **Estrutura do Projeto**
````
projeto/
├── backend/                           # Código do servidor (FastAPI)
│      ├── api.py                      # Endpoints da API
│      ├── config.py                   # Configurações (IP, porta, banco de dados)
│      ├── database.py                 # Conexão e criação da tabela no MySQL
│      ├── models.py                   # Modelos Pydantic para validação de dados
│      └── services.py                 # Funções para interagir com o banco de dados
├── esp32/                             
│      └── distReg.ini                 # Script para leitura do sensor e envio de dados
└── frontend/                          # Código do dashboard (Streamlit)
|      └── dashboard.py                
├── app.py                             
└── requirements.txt                   
````
