from cinema.data.loading_db import load_movies, load_sections, load_rooms
from cinema.models.sala import Room
from cinema.data.db import get_connection


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


def delete_room(sala_id):
    if room_in_use(sala_id):
        return "used"

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM salas WHERE id = %s", (sala_id,))
    sala = cursor.fetchone()

    if sala is None:
        conn.close()
        return "notfound"

    cursor.execute("DELETE FROM salas WHERE id = %s", (sala_id,))
    conn.commit()
    conn.close()
    return "ok"
    


def room_in_use(sala_id):
    filmes = load_movies()

    if filmes is None:
        return False
    
    for filme in filmes:
        sessoes = load_sections(filme.get('id'))

        if not sessoes:
            continue
        
        for sessao in sessoes:
            if sessao.get('sala_id') == sala_id:
                return True
    
    return False


def room_in_use_logic(sala_id, filmes, secoes_por_filme):
    if not filmes:
        return False

    for filme in filmes:
        sessoes = secoes_por_filme.get(filme.get('id'))

        if not sessoes:
            continue

        for sessao in sessoes:
            if sessao.get('sala_id') == sala_id:
                return True

    return False