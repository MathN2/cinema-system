from cinema.models.sala import Room
from cinema.data import loading_db

def create_room(dados):
    # Definir valores
    salas = loading_db.load_rooms()

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