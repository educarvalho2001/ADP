from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os
import platform

load_dotenv('.env.app')

Base = declarative_base()

class Municipio(Base):
    __tablename__ = 'municipios'
    id_municipio_ibge = Column(Integer, primary_key=True, autoincrement=False)
    nm_municipio = Column(String(255))
    sg_uf = Column(String(2))
    id_uf_ibge = Column(Integer, index=True)

class AreaColhida(Base):
    __tablename__ = 'area_colhida'
    id = Column(Integer, primary_key=True)
    id_municipio_ibge = Column(Integer, ForeignKey('municipios.id_municipio_ibge'))
    ano = Column(Integer, index=True)
    valor = Column(Integer)

class QuantidadeProduzida(Base):
    __tablename__ = 'quantidade_produzida'
    id = Column(Integer, primary_key=True)
    id_municipio_ibge = Column(Integer, ForeignKey('municipios.id_municipio_ibge'))
    ano = Column(Integer, index=True)
    valor = Column(Integer)

def get_engine(user, password, host, port, database):
    """Retorna uma instância de engine do SQLAlchemy para o banco de dados MySQL."""
    connection_string = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}?charset=utf8"
    return create_engine(connection_string)


def create_tables(engine):
    Base.metadata.create_all(engine)
    create_productivity_view(engine)  # Adicionando a criação da view após a criação das tabelas

def insert_municipios_batch(engine, municipios_df):
    municipios_df.to_sql('municipios', engine, if_exists='append', index=False, chunksize=1000, method='multi')

def insert_area_colhida_data(engine, processed_area_colhida_data):
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        session.bulk_insert_mappings(AreaColhida, processed_area_colhida_data)
        session.commit()
        print("Dados de área colhida inseridos e confirmados.")
    except Exception as e:
        session.rollback()
        print(f"Erro ao inserir dados de área colhida: {e}")
    finally:
        session.close()

def insert_quantidade_produzida_data(engine, processed_quantidade_produzida_data):
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        session.bulk_insert_mappings(QuantidadeProduzida, processed_quantidade_produzida_data)
        session.commit()
        print("Dados de quantidade produzida inseridos e confirmados.")
    except Exception as e:
        session.rollback()
        print(f"Erro ao inserir dados de quantidade produzida: {e}")
    finally:
        session.close()

def delete_existing_data(engine, year, table_name):
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        if table_name == 'area_colhida':
            session.query(AreaColhida).filter(AreaColhida.ano == year).delete()
        elif table_name == 'quantidade_produzida':
            session.query(QuantidadeProduzida).filter(QuantidadeProduzida.ano == year).delete()
        session.commit()
        print(f"Dados para o ano {year} deletados da tabela {table_name}.")
    except Exception as e:
        session.rollback()
        print(f"Erro ao deletar dados existentes: {e}")
    finally:
        session.close()

def drop_tables(engine):
    with engine.connect() as conn:
        conn.execute(text("DROP VIEW IF EXISTS produtividade"))  # Remova a view primeiro, se existir
        conn.execute(text("DROP TABLE IF EXISTS area_colhida"))
        conn.execute(text("DROP TABLE IF EXISTS quantidade_produzida"))
        conn.execute(text("DROP TABLE IF EXISTS municipios"))
        print("Tabelas e view removidas.")

def count_rows(engine):
    if not check_tables_exist(engine):
        print("As tabelas necessárias não existem.")
        return

    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT 
            (SELECT COUNT(*) FROM area_colhida) AS qt_area_colhida, 
            (SELECT COUNT(*) FROM quantidade_produzida) AS qt_quantidade_produzida,
            (SELECT COUNT(*) FROM municipios) AS qt_municipios
        """))
        row = result.fetchone()
        print(f"Total de registros em area_colhida: {row[0]}")
        print(f"Total de registros em quantidade_produzida: {row[1]}")
        print(f"Total de registros em municipios: {row[2]}")

def delete_cache_files(engine=None):
    if platform.system() == "Windows":
        os.system('for /r %i in (*.pyc) do if not "%%~dpi"=="%CD%\\venv\\" del "%%i"')
        os.system('for /d /r %i in (venv) do (if not "%%~dpi"=="%CD%\\venv\\" rd /s /q "%%i")')
    else:
        os.system('find . -path ./venv -prune -o -name "*.pyc" -exec rm -f {} \\;')
        os.system('find . -path ./venv -prune -o -name "__pycache__" -exec rm -rf {} \\;')
    print("Arquivos de cache removidos.")

    
def is_table_empty(engine, table_name):
    try:
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
            count = result.scalar()
            return count == 0
    except Exception as e:
        if "doesn't exist" in str(e):
            return True  # A tabela não existe, portanto está "vazia"
        else:
            print(f"Erro ao verificar se a tabela '{table_name}' está vazia: {e}")
            raise

def check_tables_exist(engine):
    tables = ['municipios', 'area_colhida', 'quantidade_produzida']
    with engine.connect() as conn:
        for table in tables:
            try:
                conn.execute(text(f"SELECT 1 FROM {table} LIMIT 1"))
            except Exception as e:
                if "doesn't exist" in str(e):
                    print(f"Tabela '{table}' não existe.")
                    return False
    return True

def create_productivity_view(engine):
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE OR replace VIEW produtividade
            AS
            SELECT m.id_uf_ibge                            AS id_uf_ibge,
                    m.sg_uf                                AS sg_uf,
                    a.ano                                  AS ano,
                    SUM(q.valor) / Nullif(SUM(a.valor), 0) AS produtividade
            FROM   area_colhida a
                    join quantidade_produzida q
                    ON a.id_municipio_ibge = q.id_municipio_ibge
                        AND a.ano = q.ano
                    join municipios m
                    ON a.id_municipio_ibge = m.id_municipio_ibge
            GROUP  BY m.sg_uf,
                        m.sg_uf,
                        a.ano 
        """))
        #print("View de produtividade criada/atualizada.")
