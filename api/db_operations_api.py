from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# Carregar as variáveis de ambiente do arquivo .env.api
load_dotenv('.env.api')

def get_engine():
    user = os.getenv('DB_USER_API')
    password = os.getenv('DB_PASSWORD_API')
    host = os.getenv('DB_HOST_API')
    port = os.getenv('DB_PORT_API')
    database = os.getenv('DB_NAME_API')
    return create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}?charset=utf8')

    # Debug prints para verificar os valores
    print(f"DB_USER_APIWWxxx: {user}")
    print(f"DB_PASSWORD_API: {password}")
    print(f"DB_HOST_API: {host}")
    print(f"DB_PORT_API: {port}")
    print(f"DB_NAME_API: {database}")

def fetch_area_colhida(engine, municipio_id, year):
    query = text("""
        SELECT  m.nm_municipio,
                m.sg_uf,
                m.id_uf_ibge,
                ac.valor AS area_colhida
        FROM    area_colhida ac
        JOIN    municipios m ON ac.id_municipio_ibge = m.id_municipio_ibge
        WHERE   ac.id_municipio_ibge = :municipio_id
            AND ac.ano = :year
    """).bindparams(municipio_id=municipio_id, year=year)
    
    with engine.connect() as conn:
        result = conn.execute(query).fetchone()
        if result:
            return {
                "municipio_id": municipio_id,
                "year": year,
                "area_colhida": result._mapping["area_colhida"],
                "nm_municipio": result._mapping["nm_municipio"],
                "sg_uf": result._mapping["sg_uf"],
                "id_uf_ibge": result._mapping["id_uf_ibge"]
            }
        else:
            return None

def fetch_produtividade(engine, estados, year):
    # Converter a tupla de estados em uma string separada por vírgulas
    estados_str = ', '.join([f"'{estado}'" for estado in estados])
    
    query = text(f"""
        SELECT  p.sg_uf,
                p.produtividade
        FROM    produtividade p
        WHERE   p.sg_uf IN ({estados_str})
            AND p.ano = :year
    """).bindparams(year=year)
    
    with engine.connect() as conn:
        result = conn.execute(query).fetchall()
        if result:
            return [
                {
                    "estado": row._mapping["sg_uf"],
                    "year": year,
                    "produtividade": row._mapping["produtividade"]
                } for row in result
            ]
        else:
            return None


def fetch_quantidade_produzida(engine, municipios, anos):
    # Converter as listas de municípios e anos em strings separadas por vírgulas
    municipios_str = ', '.join([f"'{municipio}'" for municipio in municipios])
    anos_str = ', '.join([f"'{ano}'" for ano in anos])
    
    query = text(f"""
        SELECT  qp.id_municipio_ibge,
                qp.ano,
                qp.valor AS quantidade_produzida
        FROM    quantidade_produzida qp
        WHERE   qp.id_municipio_ibge IN ({municipios_str})
            AND qp.ano IN ({anos_str})
    """)
    
    with engine.connect() as conn:
        result = conn.execute(query).fetchall()
        
        # Verificar se o número total de dados retornados excede 100
        if len(result) > 100:
            return {
                "error": "A solicitação excede o limite de 100 linhas. Por favor, refine sua consulta."
            }
        else:
            return [
                {
                    "municipio_id": row._mapping["id_municipio_ibge"],
                    "year": row._mapping["ano"],
                    "quantidade_produzida": row._mapping["quantidade_produzida"]
                } for row in result
            ]

