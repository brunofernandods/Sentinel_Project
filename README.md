# Sentinel
Sentinel - Camera Monitoring System

Overview

Sentinel is a camera monitoring system developed in Python, utilizing the Ultralytics YOLO library for real-time object detection. The system features a graphical interface built with the Flet framework and integrates with a MySQL database for camera management.

[![LOGO](https://i.postimg.cc/13q3Ph9P/LOGO-OFICIAL-TRANSPARENTE.png)](https://postimg.cc/RWvBQY6b)

## Screenshots

[![Whats-App-Image-2024-02-26-at-09-18-32.jpg](https://i.postimg.cc/NMSQZpWL/Whats-App-Image-2024-02-26-at-09-18-32.jpg)](https://postimg.cc/yghqZX6z)

## Features

- Real-time Visualization: The system allows real-time viewing of registered cameras, highlighting detected objects in the image.

- Camera Registration: It is possible to register new cameras, providing a number, establishment name, address, environment, and contact associated with each one.

- Camera Deletion: Registered cameras can be removed from the system.

- Recording Explorer: The system has a button that opens the file explorer in the recordings folder, facilitating access to video records.

- Light/Dark Mode: The system offers the option to switch between light and dark modes for better user preference adaptation.

## Prerequisites

Before running the system, make sure to have the following dependencies installed:

- Python 3.11
- OpenCV
- Ultralytics YOLO
- Flet
- MySQL Connector
- Winsound (for Windows)

## Database Configuration

The system uses a MySQL database to store camera information. Make sure to correctly configure the credentials in the backend.py file::

```bash
  db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sua_senha",
    database="sentinel"
)
```
Use these parameters to create the database:
```bash
CREATE DATABASE sentinel;

CREATE TABLE cameras (
    numero INT PRIMARY KEY,
    localizacao VARCHAR(255),
    endereco VARCHAR(255),
    comodo VARCHAR(255),
    contato VARCHAR(255)
);
```
## Running the System
Clone the repository to your local machine:

```bash
git clone https://github.com/SchmittAdrian/Sentinel.git
cd sentinel
```
Install the dependencies:
```bash
pip install -r requirements.txt
```

Run the application:
```bash
python main.py
```

## Comments

The prediction model used in the project is private and for the exclusive use of collaborators. This repository contains the standard detection model, making it possible to switch to a customized model.

# Sentinel
Sentinel - Sistema de Monitoramento por Câmeras

Visão Geral

O Sentinel é um sistema de monitoramento por câmeras desenvolvido em Python, utilizando a biblioteca Ultralytics YOLO para detecção de objetos em tempo real. O sistema é composto por uma interface gráfica construída com o framework Flet e integração com um banco de dados MySQL para gerenciamento das câmeras.

[![LOGO](https://i.postimg.cc/13q3Ph9P/LOGO-OFICIAL-TRANSPARENTE.png)](https://postimg.cc/RWvBQY6b)

## Screenshots

[![Whats-App-Image-2024-02-26-at-09-18-32.jpg](https://i.postimg.cc/NMSQZpWL/Whats-App-Image-2024-02-26-at-09-18-32.jpg)](https://postimg.cc/yghqZX6z)

## Funcionalidades

- Visualização em Tempo Real: O sistema permite a visualização em tempo real das câmeras cadastradas, destacando objetos detectados na imagem.

- Cadastro de Câmeras: É possível cadastrar novas câmeras, informando número, nome do estabelecimento, endereço, ambiente e contato associados a cada uma.

- Exclusão de Câmeras: Câmeras cadastradas podem ser excluídas do sistema.

- Explorador de Gravações: O sistema possui um botão que abre o explorador de arquivos na pasta de gravações, facilitando o acesso aos registros de vídeo.

- Modo Claro/Escuro: O sistema oferece a opção de alternar entre os modos claro e escuro para melhor adaptação às preferências do usuário.

## Pré-requisitos

Antes de executar o sistema, certifique-se de ter as seguintes dependências instaladas:

- Python 3.11
- OpenCV
- Ultralytics YOLO
- Flet
- MySQL Connector
- Winsound (for Windows)

## Configuração do Banco de Dados

O sistema utiliza um banco de dados MySQL para armazenar informações das câmeras. Certifique-se de configurar corretamente as credenciais no arquivo backend.py:

```bash
  db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sua_senha",
    database="sentinel"
)
```
Utilize estes parâmetros para cria seu banco de dados:
```bash
CREATE DATABASE sentinel;

CREATE TABLE cameras (
    numero INT PRIMARY KEY,
    localizacao VARCHAR(255),
    endereco VARCHAR(255),
    comodo VARCHAR(255),
    contato VARCHAR(255)
);
```
## Execução do Sistema
Clone o repositório para sua máquina local:

```bash
git clone https://github.com/SchmittAdrian/Sentinel.git
cd sentinel
```
Instale as dependências:
```bash
pip install -r requirements.txt
```

Execute o aplicativo:
```bash
python main.py
```

## Observações

O modelo de predição utilizado no projeto é privado e de uso exclusivo dos colaboradores. Neste reposositório, contém o modelo padrão de detecção, sendo possível a troca para um modelo perssonalizado. 
