# **🌦️ Projeto de Servidor Meteorológico**

Este projeto implementa um sistema de monitoramento climático baseado em IoT, utilizando uma placa ESP32 integrada ao sensor BME280 para aquisição de dados meteorológicos. As informações são transmitidas para um servidor via API desenvolvida com FastAPI, armazenadas em um banco de dados MySQL e apresentadas em tempo real através de um dashboard interativo construído com Streamlit.
---

<BR>
<BR>



## 🌦️ Visão Geral do Sistema

O sistema realiza a coleta automática de **temperatura**, **umidade relativa do ar** e **pressão atmosférica** a cada **5 minutos**, utilizando um sensor **BME280** conectado a uma placa **ESP32**. Os dados são transmitidos ao servidor via requisições **HTTP POST**, sendo armazenados em um banco de dados **MySQL**.

A **API desenvolvida com FastAPI** disponibiliza endpoints seguros para envio e consulta dos dados, integrando-se ao **dashboard interativo em Streamlit**, que exibe:

- ✅ As leituras mais recentes em tempo real  
- 📊 Gráficos dinâmicos para análise histórica  
- 🌡️ Indicadores climáticos  
- 🔄 Atualizações automáticas  
- 📤 Exportação de relatórios nos formatos **CSV**, **XLSX** e **Json**

---

### 🔐 Funcionalidades de Segurança e Acesso

O sistema conta com um **mecanismo de autenticação de usuários com senha criptografada (bcrypt)**, permitindo:

- 🔑 **Login seguro com validação de credenciais**
- 🧑‍💼 **Controle de permissões baseado em perfil de usuário** (ex.: administrador ou visitante)
- ⚙️ **Acesso restrito a funcionalidades administrativas**, como gerenciamento de usuários

---

Essa abordagem garante a **integridade dos dados**, a **segurança do sistema** e uma **visualização clara e intuitiva** das informações meteorológicas.
---


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
│      ├── security.py                 # Autenticação de usuário
│      └── services.py                 # Funções para interagir com o banco de dados
├── esp32/                             
│      └── weather_sensor.ini          # Script para leitura do sensor e envio de dados
└── frontend/                          # Código do dashboard (Streamlit)
│      ├── views/              
|      |     └── home.py               # Pagina principal
|      |     └── reports.py            # Gráficos e Relatórios
|      |     └── settings.py           # Configurações (Só exibido para usuarios permitidos)
|      |     └── logout.py             
|      └── app.py     
├── README.md                                   
└── requirements.txt                   
````
