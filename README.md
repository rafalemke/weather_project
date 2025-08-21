# **🌦️ Projeto de Servidor Meteorológico**

Este projeto é um sistema de monitoramento climático IoT end-to-end. Um sensor BME280 acoplado a um ESP32 captura dados meteorológicos, que são transmitidos para um servidor de borda (Raspberry Pi) localizado em uma rede remota. Para garantir a comunicação segura e estável pela internet, foi implementado um túnel com Cloudflare, que expõe uma API desenvolvida em FastAPI. A API alimenta um banco de dados MySQL e permite a visualização dos dados em tempo real através de um dashboard interativo construído com Streamlit.
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

<table align="center">
  <tr>
    <td align="center">
      <img src="data/Print_home.png" alt="Print da tela inicial do projeto" width="400"/>
    </td>
    <td align="center">
      <img src="data/print_relatorio.png" alt="Print do relatório gerado pela aplicação" width="400"/>
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="data/print_analise.png" alt="Print da tela de análise de dados" width="400"/>
    </td>    
    <td align="center">
      <img src="data/print_export.png" alt="Print da funcionalidade de exportação" width="400"/>
    </td>
  </tr>
</table>

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
