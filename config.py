from dotenv import load_dotenv
import os

def load_env(env_file):
    load_dotenv(env_file)

def get_app_env():
    load_dotenv('.env')
    return os.getenv('APP_ENV')

def get_database_credentials(app=True):
    app_env = get_app_env()

    print(f"Credencial: {app_env}")
    if app:
        if app_env == 'app_dba':
            load_env('.env.app_dba')
        elif app_env == 'app_operator':
            load_env('.env.app_operator')
        user = os.getenv('DB_USER_APP')
        password = os.getenv('DB_PASSWORD_APP')
        host = os.getenv('DB_HOST_APP')
        port = os.getenv('DB_PORT_APP')
        database = os.getenv('DB_NAME_APP')
    else:
        load_env('.env.api')
        user = os.getenv('DB_USER_API')
        password = os.getenv('DB_PASSWORD_API')
        host = os.getenv('DB_HOST_API')
        port = os.getenv('DB_PORT_API')
        database = os.getenv('DB_NAME_API')

    return user, password, host, port, database
