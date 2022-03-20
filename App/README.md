# Configurações:
Siga as orientações a seguir para executar o projeto:

## Requerimentos:
- Linguagem de programação Python (Versão 3.6 ou Superior).
- Banco de Dados MySQL ou outro a sua preferência.

## Baixando os arquivos em seu computador:
Execute os seguintes comandos em seu terminal:
- git clone https://github.com/DhBarboza/lab-engenharia-software.git
- cd App

## Instalar Virtualenv:
- pip install virtualenv

## Criar ambiente de desenvolvimento:
Windows:
  - virtualenv -p python3 env

## Ativar ambiente de desenvolvimento:
Windows:
  - .\env\Scripts\activate

## Instalação de dependências:
- pip install -r requirements.txt

## Configuração do banco de Dados:
Configure a conexão com o seu banco de dados de acordo com os seguintes parâmetros:
  - Database: Nome do banco de Dados
  - Host: localhost || 127.0.0.1
  - Port: Utilize a porta padrão
  - Username: Nome de usuário do servidor
  - Password: A senha do seu servidor

Exemplo:
```bash
MYSQL_DATABASE=notice
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USERNAME=root 
MYSQL_PASSWORD=exemple1234
```

## Execute o seguinte comando para criar o banco de dados e as tabelas:
- python wsgi.py create_db

## Para executar a aplicação:
- python wsgi.py