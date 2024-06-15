# ADP
Atualização dos Dados de Plantio-ADP

# Tela da aplicação
============================================================
Bem-vindo ao Sistema de Atualização dos Dados de Plantio-ADP
                     Veeries - Inteligência em Agronegócio
Engenheiro de dados: Eduardo Alves de Carvalho
Contato:             eduardo@e-setorial.com.br
============================================================

Credencial: app_dba
Conexão com o banco de dados estabelecida.

MENU:
1. Criar estrutura do banco de dados
2. Atualizar dados para um ano específico
3. Apagar dados para um ano específico
4. Contar registros nas tabelas
5. Remover arquivos de cache do Python
6. Remover tabelas  - DROP TABLES
7. Iniciar Flask
8. Testar endpoints - Visão do cliente
9. Parar Flask
10. Sair
Escolha uma opção: 

# Estrutura de arquivos
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

# Configure estes arquivos .env* para ter acesso ao banco de dados
.env
# Ajuste o valor de APP_ENV para app_operator ou app_dba conforme deseje utilizar uma ou outra credencial
APP_ENV=app_operator
#APP_ENV=app_dba

.env.api
# Usuário WebService - Grant de Select
DB_USER_API='insira-seu-usuario'
DB_PASSWORD_API='insira-sua-senha'
DB_HOST_API='insira-seu-host'
DB_PORT_API=3306
DB_NAME_API='insira-seu-banco-de-dados'
JWT_SECRET_KEY='insira-sua-secret-key'
# String_de_conexao_MySQL = "mysql+mysqlconnector://insira-seu-usuario:insira-sua-senha@insira-seu-host:3306/insira-seu-banco-de-dados?charset=utf8"

.env.app_dba
# Usuário DBA
DB_USER_APP='insira-seu-usuario'
DB_PASSWORD_APP='insira-sua-senha'
DB_HOST_APP='insira-seu-host'
DB_PORT_APP=3306
DB_NAME_APP='insira-seu-banco-de-dados'
# String_de_conexao_MySQL = "mysql+mysqlconnector://insira-seu-usuario:insira-sua-senha@insira-seu-host:3306/insira-seu-banco-de-dados?charset=utf8"

.env.app_operator
# Usuário Operador - Não Dropa nem Recria as tabelas
DB_USER_APP='insira-seu-usuario'
DB_PASSWORD_APP='insira-sua-senha'
DB_HOST_APP='insira-seu-host'
DB_PORT_APP=3306
DB_NAME_APP='insira-seu-banco-de-dados'
# String_de_conexao_MySQL = "mysql+mysqlconnector://insira-seu-usuario:insira-sua-senha@insira-seu-host:3306/insira-seu-banco-de-dados?charset=utf8"


Para testar os endpoints protegidos, você precisa primeiro obter um token de acesso. Vamos usar o endpoint /login para isso:

sh
Copiar código
curl -X POST http://localhost:5000/login -H "Content-Type: application/json" -d '{"username": "admin", "password": "admin"}'
Isso deve retornar um token JWT:

json
Copiar código
{
  "success": true,
  "access_token": "seu-token-jwt"
}
Agora, você pode usar esse token para acessar os endpoints protegidos.

Endpoints da API
1. Área Colhida

Endpoint: /area_colhida
Método: GET

Parâmetros Obrigatórios:

municipio_id: Código do município (IBGE)
year: Ano desejado
Exemplo de URL:

arduino
Copiar código
http://127.0.0.1:5000/area_colhida?municipio_id=1100049&year=2020
Descrição:
Esse endpoint retorna a área colhida para o município e ano especificados.

Exemplo de Resposta de Sucesso:

json
Copiar código
{
  "success": true,
  "data": [...],
  "message": "Dados recuperados com sucesso"
}
Exemplo de Resposta de Erro:

json
Copiar código
{
  "success": false,
  "data": null,
  "message": "Parâmetros obrigatórios: municipio_id, year"
}
2. Produtividade

Endpoint: /produtividade
Método: GET

Parâmetros Obrigatórios:

estado: Lista de estados brasileiros (UF)
year: Ano desejado
Exemplo de URL:

arduino
Copiar código
http://127.0.0.1:5000/produtividade?estado=SP&estado=RJ&year=2020
Descrição:
Esse endpoint retorna a produtividade para os estados e ano especificados.

Exemplo de Resposta de Sucesso:

json
Copiar código
{
  "success": true,
  "data": [...],
  "message": "Dados recuperados com sucesso"
}
Exemplo de Resposta de Erro:

json
Copiar código
{
  "success": false,
  "data": null,
  "message": "Parâmetros obrigatórios: estado, year"
}
3. Quantidade Produzida

Endpoint: /quantidade_produzida
Método: GET

Parâmetros Obrigatórios:

municipio: Lista de códigos de municípios (IBGE)
ano: Lista de anos desejados
Exemplo de URL:

arduino
Copiar código
http://127.0.0.1:5000/quantidade_produzida?municipio=1100049&municipio=1100148&ano=2020&ano=2021
Descrição:
Esse endpoint retorna a quantidade produzida para os municípios e anos especificados.

Exemplo de Resposta de Sucesso:

json
Copiar código
{
  "success": true,
  "data": [...],
  "message": "Dados recuperados com sucesso"
}
Exemplo de Resposta de Erro:

json
Copiar código
{
  "success": false,
  "data": null,
  "message": "Parâmetros obrigatórios: municipio, ano"
}
Exemplo de Resposta de Erro (Excesso de Dados):

json
Copiar código
{
  "success": false,
  "data": null,
  "message": "Número de dados solicitados excede o limite de 100"
}
Exemplo de Chamada da API com curl
Para obter o token:

sh
Copiar código
curl -X POST "http://localhost:5000/login" -H "Content-Type: application/json" -d '{"username":"admin","password":"admin"}'
Para consultar a área colhida:

sh
Copiar código
curl -X GET "http://localhost:5000/area_colhida?municipio_id=1100049&year=2020" -H "Authorization: Bearer <YOUR_TOKEN>"
Para consultar a produtividade:

sh
Copiar código
curl -X GET "http://localhost:5000/produtividade?estado=SP&estado=RJ&year=2020" -H "Authorization: Bearer <YOUR_TOKEN>"
Para consultar a quantidade produzida:

sh
Copiar código
curl -X GET "http://localhost:5000/quantidade_produzida?municipio=1100049&municipio=1100130&ano=2020&ano=2021" -H "Authorization: Bearer <YOUR_TOKEN>"
