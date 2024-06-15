import requests

# Entrada de dados
def get_area_colhida(year):
    url = f"https://apisidra.ibge.gov.br/values/t/5457/n6/all/v/216/p/{year}/c782/40124?formato=json"
    response = requests.get(url)
    return response.json()

def get_quantidade_produzida(year):
    url = f"https://apisidra.ibge.gov.br/values/t/5457/n6/all/v/214/p/{year}/c782/40124?formato=json"
    response = requests.get(url)
    return response.json()

# Saída de dados via API
def get_token():
    url = "http://localhost:5000/login"
    payload = {"username": "admin", "password": "admin"}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    return response.json().get("access_token")

def call_endpoint(endpoint, params, token):
    base_url = "http://localhost:5000"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{base_url}/{endpoint}", params=params, headers=headers)
    return response.json()

def test_area_colhida(municipio_id, year):
    token = get_token()
    params = {"municipio_id": municipio_id, "year": year}
    return call_endpoint("area_colhida", params, token)

def test_produtividade(estados, year):
    token = get_token()
    params = {"estado": estados, "year": year}
    return call_endpoint("produtividade", params, token)

def test_quantidade_produzida(municipios, anos):
    token = get_token()
    params = {"municipio": municipios, "ano": anos}
    return call_endpoint("quantidade_produzida", params, token)
