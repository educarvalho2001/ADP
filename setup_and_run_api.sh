#!/bin/bash
# chmod 755 setup_and_run_api.sh
#clear

# Passo 1: Criar um ambiente virtual e instalar as dependências
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# Verificar se o Flask está instalado
if ! pip show Flask > /dev/null 2>&1; then
    echo "Flask não está instalado. Instalando Flask..."
    pip install -r requirements.txt
fi


# Exibir o ambiente virtual para depuração
echo "Ambiente virtual ativado: $(which python)"

# Passo 2: Verificar se já existe um PID e se o processo ainda está em execução
if [ -f flask.pid ]; then
    PID=$(cat flask.pid)
    if ps -p $PID > /dev/null; then
        echo "Flask já está em execução com PID $PID"
        exit 1
    else
        echo "PID $PID encontrado, mas o processo não está em execução. Removendo PID antigo."
        rm flask.pid
    fi
fi

# Passo 3: Carregar as variáveis de ambiente do arquivo .env.api
if [ -f ".env.api" ]; then
    export $(grep -v '^#' .env.api | xargs)
else
    echo "Arquivo .env.api não encontrado!"
    exit 1
fi

# Passo 4: Executar a API
export FLASK_APP=api
export FLASK_ENV=development

nohup flask run > flask.log 2>&1 & echo $! > flask.pid

# Esperar um pouco para garantir que o Flask inicie
sleep 5

# Verificar se o Flask ainda está em execução
PID=$(cat flask.pid)
if ps -p $PID > /dev/null; then
    echo "Flask iniciado com sucesso em segundo plano com PID $PID"
else
    echo "Flask falhou ao iniciar. Verifique o arquivo flask.log para mais detalhes."
    tail -n 20 flask.log
    exit 1
fi
