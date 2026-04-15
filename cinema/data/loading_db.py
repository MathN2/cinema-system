from cinema.data.db import get_connection
from typing import cast

def load_movies():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM filmes")

    filmes = cast(list[dict[str, object]], cursor.fetchall())
    conn.close()

    return filmes


def load_sections(filme_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
                   SELECT * FROM sessoes
                   WHERE filme_id = %s
                   """, (filme_id,))


    sessoes = cast(list[dict[str, object]], cursor.fetchall())
    conn.close()
    
    return sessoes


def load_rooms():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM salas")
    salas = cast(list[dict[str, object]], cursor.fetchall())

    conn.close()
    
    return salas