
# ADP
Atualização dos Dados de Plantio-ADP

## Tela da aplicação
```plaintext
============================================================
Bem-vindo ao Sistema de Atualização dos Dados de Plantio-ADP
                     Veeries - Inteligência em Agronegócio
Engenheiro de dados: Eduardo Alves de Carvalho
Contato:             eduardo@e-setorial.com.br
============================================================

Credencial: app_dba  
Conexão com o banco de dados estabelecida.

MENU:
- Criar estrutura do banco de dados
- Atualizar dados para um ano específico
- Apagar dados para um ano específico
- Contar registros nas tabelas
- Remover arquivos de cache do Python
- Remover tabelas - DROP TABLES
- Iniciar Flask
- Testar endpoints - Visão do cliente
- Parar Flask
- Sair
- Escolha uma opção:
```

## Estrutura de arquivos
```plaintext
.
|-- README.md
|-- airflow
|   `-- dags
|       `-- airflow_dag.py
|-- api
|   |-- __init__.py
|   |-- db_operations_api.py
|   `-- endpoints.py
|-- api.py
|-- config.py
|-- data
|   `-- dct_municipio_uf.csv
|-- data_pipeline
|   |-- __init__.py
|   |-- api_requests.py
|   |-- data_processing.py
|   `-- db_operations.py
|-- main.py
|-- requirements.txt
`-- setup_and_run_api.sh
```
## Requirements
```plaintext
pip install requests mysql-connector-python sqlalchemy flask flask_sqlalchemy flask_jwt_extended pandas python-dotenv 
```

## Configuração dos arquivos `.env`
### .env
Ajuste o valor de APP_ENV para `app_operator` ou `app_dba` conforme deseje utilizar uma ou outra credencial

```plaintext
APP_ENV=app_operator
#APP_ENV=app_dba
```

### .env.api
Usuário WebService - Grant de Select

```plaintext
DB_USER_API='insira-seu-usuario'
DB_PASSWORD_API='insira-sua-senha'
DB_HOST_API='insira-seu-host'
DB_PORT_API=3306
DB_NAME_API='insira-seu-banco-de-dados'
JWT_SECRET_KEY='insira-sua-secret-key'

# String_de_conexao_MySQL="mysql+mysqlconnector://insira-seu-usuario@insira-seu-host:3306/insira-seu-banco-de-dados?charset=utf8"
```

### .env.app_dba
Usuário DBA

```plaintext
DB_USER_APP='insira-seu-usuario'
DB_PASSWORD_APP='insira-sua-senha'
DB_HOST_APP='insira-seu-host'
DB_PORT_APP=3306
DB_NAME_APP='insira-seu-banco-de-dados'

# String_de_conexao_MySQL="mysql+mysqlconnector://insira-seu-usuario@insira-seu-host:3306/insira-seu-banco-de-dados?charset=utf8"
```

### .env.app_operator
Usuário Operador - Não Dropa nem Recria as tabelas

```plaintext
DB_USER_APP='insira-seu-usuario'
DB_PASSWORD_APP='insira-sua-senha'
DB_HOST_APP='insira-seu-host'
DB_PORT_APP=3306
DB_NAME_APP='insira-seu-banco-de-dados'

# String_de_conexao_MySQL="mysql+mysqlconnector://insira-seu-usuario@insira-seu-host:3306/insira-seu-banco-de-dados?charset=utf8"
```

## Testando os Endpoints
Para testar os endpoints protegidos, você precisa primeiro obter um token de acesso. Vamos usar o endpoint `/login` para isso:

### Token Flask
```sh
curl -X POST http://localhost:5000/login -H "Content-Type: application/json" -d '{"username": "admin", "password": "admin"}'
```

Isso deve retornar um token JWT:

```json
{
  "success": true,
  "access_token": "seu-token-jwt"
}
```

Agora, você pode usar esse token para acessar os endpoints protegidos.

## Endpoints da API
1. Área Colhida
Endpoint: /area_colhida  
Método: GET  
Parâmetros Obrigatórios:  
municipio_id: Código do município (IBGE)  
year: Ano desejado  

Exemplo de Chamada da API com curl:

```sh
curl -X GET "http://localhost:5000/area_colhida?municipio_id=1100049&year=2020" -H "Authorization: Bearer <YOUR_TOKEN>"
```

Descrição  
Esse endpoint retorna a área colhida para o município e ano especificados.

Exemplo de Resposta de Sucesso:

```json
{
  "success": true,
  "data": [...],
  "message": "Dados recuperados com sucesso"
}
```

Exemplo de Resposta de Erro:

```json
{
  "success": false,
  "data": null,
  "message": "Parâmetros obrigatórios: municipio_id, year"
}
```

2. Produtividade
Endpoint: /produtividade  
Método: GET  
Parâmetros Obrigatórios:  
estado: Lista de estados brasileiros (UF)  
year: Ano desejado  

Exemplo de Chamada da API com curl:

```sh
curl -X GET "http://localhost:5000/produtividade?estado=SP&estado=RJ&year=2020" -H "Authorization: Bearer <YOUR_TOKEN>"
```

Descrição  
Esse endpoint retorna a produtividade para os estados e ano especificados.

Exemplo de Resposta de Sucesso:

```json
{
  "success": true,
  "data": [...],
  "message": "Dados recuperados com sucesso"
}
```

Exemplo de Resposta de Erro:

```json
{
  "success": false,
  "data": null,
  "message": "Parâmetros obrigatórios: estado, year"
}
```

3. Quantidade Produzida
Endpoint: /quantidade_produzida  
Método: GET  
Parâmetros Obrigatórios:  
municipio: Lista de códigos de municípios (IBGE)  
ano: Lista de anos desejados  

Exemplo de Chamada da API com curl:

```sh
curl -X GET "http://localhost:5000/quantidade_produzida?municipio=1100049&municipio=1100130&ano=2020&ano=2021" -H "Authorization: Bearer <YOUR_TOKEN>"
```

Descrição  
Esse endpoint retorna a quantidade produzida para os municípios e anos especificados.

Exemplo de Resposta de Sucesso:

```json
{
  "success": true,
  "data": [...],
  "message": "Dados recuperados com sucesso"
}
```

Exemplo de Resposta de Erro:

```json
{
  "success": false,
  "data": null,
  "message": "Parâmetros obrigatórios: municipio, ano"
}
```

Exemplo de Resposta de Erro (Excesso de Dados):

```json
{
  "success": false,
  "data": null,
  "message": "Número de dados solicitados excede o limite de 100"
}
```

## Endpoints Externos da API SIDRA do IBGE
Para alimentar nossa base de dados, utilizamos dois endpoints da API SIDRA do IBGE. Abaixo estão os detalhes de cada endpoint e exemplos de como utilizá-los.

### Endpoint: Área Colhida

Este endpoint retorna dados sobre a área colhida para um determinado ano.

```plaintext
URL: https://apisidra.ibge.gov.br/values/t/5457/n6/all/v/216/p/{year}/c782/40124?formato=json
```

Parâmetros:  
year: Ano desejado para a consulta (ex: 2020)  

Exemplo de URL:

```plaintext
https://apisidra.ibge.gov.br/values/t/5457/n6/all/v/216/p/2020/c782/40124?formato=json
```

### Endpoint: Quantidade Produzida

Este endpoint retorna dados sobre a quantidade produzida para um determinado ano.

```plaintext
URL: https://apisidra.ibge.gov.br/values/t/5457/n6/all/v/214/p/{year}/c782/40124?formato=json
```

Parâmetros:  
year: Ano desejado para a consulta (ex: 2020)  

Exemplo de URL:

```plaintext
https://apisidra.ibge.gov.br/values/t/5457/n6/all/v/214/p/2020/c782/40124?formato=json
```
