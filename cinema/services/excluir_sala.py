from cinema.data.loading_db import load_movies, load_sections
from cinema.data.db import get_connection


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
        sessoes = load_sections(filme.get('titulo'))

        if not sessoes:
            continue
        
        for sessao in sessoes:
            if sessao.get('sala_id') == sala_id:
                return True
    
    return False