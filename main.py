import os
import signal
import sys
from data_pipeline.db_operations import (
    get_engine, create_tables, insert_municipios_batch, 
    insert_area_colhida_data, insert_quantidade_produzida_data,
    delete_existing_data, drop_tables, count_rows, delete_cache_files, 
    is_table_empty, check_tables_exist, create_productivity_view
)
from data_pipeline.api_requests import get_area_colhida, get_quantidade_produzida, test_area_colhida, test_produtividade, test_quantidade_produzida
from data_pipeline.data_processing import process_data, load_municipios_data
from config import get_database_credentials
from datetime import datetime

def clear_screen():
    """Limpa a tela do console."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_header():
    """Exibe o cabeçalho do programa."""
    print("\n============================================================")
    print("Bem-vindo ao Sistema de Atualização dos Dados de Plantio-ADP")
    print("                     Veeries - Inteligência em Agronegócio")
    print("Engenheiro de dados: Eduardo Alves de Carvalho")
    print("Contato:             eduardo@e-setorial.com.br")
    print("============================================================\n")

def create_structure(engine):
    """Cria a estrutura do banco de dados e carrega dados dos municípios, se não já estiver presente."""
    if is_table_empty(engine, 'municipios'):
        create_tables(engine)
        municipios_df = load_municipios_data('data/dct_municipio_uf.csv')
        insert_municipios_batch(engine, municipios_df)
        print(f"Total de {len(municipios_df)} municípios inseridos.")
        print("Estrutura do banco de dados criada.")
    else:
        print("A tabela de municípios já contém dados. Pulando criação de estrutura.")

def get_valid_year():
    """Solicita ao usuário que insira um ano válido entre 2018 e o ano atual."""
    current_year = datetime.now().year
    while True:
        try:
            year = int(input(f"Digite o ano (entre 2018 e {current_year}): "))
            if 2018 <= year <= current_year:
                return year
            else:
                print(f"Por favor, digite um ano válido entre 2018 e {current_year}.")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número.")

def get_valid_years():
    """Solicita ao usuário que insira um ou mais anos válidos entre 2018 e o ano atual."""
    current_year = datetime.now().year
    while True:
        try:
            years_input = input(f"Digite os anos separados por vírgula (entre 2018 e {current_year}): ")
            years = [int(year.strip()) for year in years_input.split(',')]
            if all(2018 <= year <= current_year for year in years):
                return years
            else:
                print(f"Por favor, digite anos válidos entre 2018 e {current_year}.")
        except ValueError:
            print("Entrada inválida. Por favor, digite números separados por vírgula.")

def insert_or_update(year: int, **kwargs):
    """Busca e insere os dados referentes a um ano informado."""
    engine = kwargs.get('engine')

    if not check_tables_exist(engine):
        print("As tabelas necessárias não existem. Por favor, crie a estrutura do banco de dados primeiro.")
        return

    # Deletar dados existentes para o ano especificado
    delete_existing_data(engine, year, 'area_colhida')
    delete_existing_data(engine, year, 'quantidade_produzida')

    # Chamar API e processar os dados de 'area colhida'
    area_colhida_data = get_area_colhida(year)
    processed_area_colhida_data = process_data(area_colhida_data)
    insert_area_colhida_data(engine, processed_area_colhida_data)
    print(f"Total de {len(processed_area_colhida_data)} registros de Área Colhida inseridos.")

    # Chamar API e processar os dados de 'quantidade produzida'
    quantidade_produzida_data = get_quantidade_produzida(year)
    processed_quantidade_produzida_data = process_data(quantidade_produzida_data)
    insert_quantidade_produzida_data(engine, processed_quantidade_produzida_data)
    print(f"Total de {len(processed_quantidade_produzida_data)} registros de Quantidade Produzida inseridos.")

    # Criar ou atualizar a view de produtividade - pode ser Útil caso tenhamos que mudar o fonte da view e nao queiramos apagar os dados
    # create_productivity_view(engine)
    # print("View de produtividade criada/atualizada.")

def update_data(engine):
    """Atualiza os dados para um ano específico chamando a API e processando os dados."""
    year = get_valid_year()
    insert_or_update(year, engine=engine)

def update_data_airflow(engine):
    """Atualiza os dados para o ano atual chamando a API e processando os dados."""
    current_year = datetime.now().year
    insert_or_update(current_year, engine=engine)

def delete(year: int, **kwargs):
    """Apaga os dados referentes a um ano informado."""
    engine = kwargs.get('engine')

    # Deletar dados existentes para o ano especificado
    delete_existing_data(engine, year, 'area_colhida')
    delete_existing_data(engine, year, 'quantidade_produzida')

def delete_data_by_year(engine):
    """Apaga os dados para um ano específico."""
    year = get_valid_year()
    delete(year, engine=engine)

def test_endpoints(engine):
    """Função para testar os endpoints."""
    endpoints = {
        1: "Área Colhida",
        2: "Produtividade",
        3: "Quantidade Produzida"
    }

    print("\nEscolha o endpoint para testar:")
    for key, value in endpoints.items():
        print(f"{key}. {value}")
    choice = int(input("Escolha uma opção: "))

    if choice == 1:
        municipio_id = input("Digite o ID do município: ")
        year = get_valid_year()
        result = test_area_colhida(municipio_id, year)
    elif choice == 2:
        estados = input("Digite os estados (separados por vírgula): ")
        year = get_valid_year()
        result = test_produtividade(estados.split(','), year)
    elif choice == 3:
        municipios = input("Digite os IDs dos municípios (separados por vírgula): ")
        anos = get_valid_years()
        result = test_quantidade_produzida(municipios.split(','), anos)
    else:
        print("Opção inválida.")
        return

    print("Resultado da chamada ao endpoint:")
    print(result)

def start_flask(*args):
    """Inicia o Flask em segundo plano, se não estiver já em execução."""
    # Verifica se o Flask já está em execução
    if os.path.isfile("flask.pid"):
        with open("flask.pid", "r") as f:
            pid = int(f.read().strip())
        try:
            # Verifica se o processo está em execução
            os.kill(pid, 0)
            print(f"O Flask já está em execução com PID {pid}.")
            return
        except OSError:
            print("Arquivo PID encontrado, mas o processo não está em execução. Removendo PID antigo.")
            os.remove("flask.pid")

    # Executa o script para iniciar o Flask
    os.system('./setup_and_run_api.sh')

def stop_flask(*args):
    """Para o Flask que foi iniciado em segundo plano."""
    if os.path.isfile("flask.pid"):
        with open("flask.pid", "r") as f:
            pid = int(f.read().strip())
        
        try:
            os.kill(pid, signal.SIGTERM)
            os.remove("flask.pid")
            print("Flask foi parado.")
        except ProcessLookupError:
            print("O processo Flask não está em execução.")
            os.remove("flask.pid")

def exit_program(engine):
    """Encerra o programa e fecha a conexão com o banco de dados."""
    print("Saindo do programa. Fechando conexão com o banco de dados.")
    engine.dispose()
    exit()

def main():
    """Função principal para executar o aplicativo com menu."""
    clear_screen()
    display_header()

    user, password, host, port, database = get_database_credentials()

    try:
        engine = get_engine(user, password, host, port, database)
        with engine.connect() as conn:
            pass
        print("Conexão com o banco de dados estabelecida.")
    except Exception as e:
        print(f"Erro ao conectar com o banco de dados: {e}")
        sys.exit(1)

    # Define as opções do menu e as funções correspondentes
    options = {
        1: create_structure,
        2: update_data,
        3: delete_data_by_year,
        4: count_rows,
        5: delete_cache_files,
        6: drop_tables,
        7: start_flask,
        8: test_endpoints,
        9: stop_flask,
        10: exit_program
    }

    # Exibe o menu e lida com a escolha do usuário
    while True:
        print("\nMENU:")
        print("1. Criar estrutura do banco de dados")
        print("2. Atualizar dados para um ano específico")
        print("3. Apagar dados para um ano específico")
        print("4. Contar registros nas tabelas")
        print("5. Remover arquivos de cache do Python")
        print("6. Remover tabelas  - DROP TABLES")
        print("7. Iniciar Flask")
        print("8. Testar endpoints - Visão do cliente")
        print("9. Parar Flask")
        print("10. Sair")
        choice = int(input("Escolha uma opção: "))
        if choice in options:
            options[choice](engine)
        else:
            print("Opção inválida. Por favor, escolha novamente.")

if __name__ == "__main__":
    main()
