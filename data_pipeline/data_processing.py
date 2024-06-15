import pandas as pd

def process_data(data):
    processed_data = []
    
    # Verificando se o data é uma lista e possui elementos
    if isinstance(data, list) and len(data) > 1:
        headers = data[0]  # O primeiro elemento contém os cabeçalhos
        for item in data[1:]:
            valor = item['V']
            try:
                valor_int = int(valor)
            except ValueError:
                # print(f"Ignorando registro com valor inválido '{valor}' para id_municipio_ibge: {item['D1C']}")
                continue
            
            processed_item = {
                'id_municipio_ibge': item['D1C'],
                'ano': item['D3C'],
                'valor': valor_int
            }
            processed_data.append(processed_item)
    else:
        print("Os dados estão em um formato desconhecido")
    
    return processed_data

def load_municipios_data(file_path):
    df = pd.read_csv(file_path, encoding='latin1', delimiter=';')
    df.columns = df.columns.str.strip()
    return df
