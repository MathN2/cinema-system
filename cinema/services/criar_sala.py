from cinema.models.sala import Room
from cinema.data.storage import load_rooms

def create_room(dados):
    # Definir valores
    salas = load_rooms()

    numero = dados['numero']
    linhas = dados['linhas']
    colunas = dados['colunas']

    # Validaçao
    for sala in salas:
        if sala.get('numero') == numero:
            return None
        
    # Chamar sala.Room()
    sala = Room(numero, linhas, colunas)
    return sala