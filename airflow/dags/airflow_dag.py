# airflow_dag.py
# Configuração do Airflow:
#   Instale o Airflow seguindo as instruções na documentação oficial.
#   Inicie o Airflow Scheduler e Web Server.
#   Certifique-se de que o DAG (airflow_dag.py) esteja no diretório de DAGs do Airflow ($AIRFLOW_HOME/dags).
# Execução do DAG:
#   No Airflow Web UI, ative o DAG update_data_dag.
#   O DAG será executado de acordo com o agendamento definido (semanalmente neste exemplo).

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from main import update_data_airflow, get_engine
from config import get_database_credentials

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def run_update_data():
    user, password, host, port, database = get_database_credentials()
    engine = get_engine(user, password, host, port, database)
    update_data_airflow(engine)

dag = DAG(
    'update_data_dag',
    default_args=default_args,
    description='DAG para atualizar os dados automaticamente',
    schedule_interval='@weekly',  # ou '0 0 * * 0' para rodar semanalmente
)

update_data_task = PythonOperator(
    task_id='update_data',
    python_callable=run_update_data,
    dag=dag,
)
