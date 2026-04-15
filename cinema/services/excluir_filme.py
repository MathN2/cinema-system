from cinema.data.db import get_connection
"""
Apaga um filme cadastrado no arquivo JSON.
"""

def delete_movie(filme_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM filmes
        WHERE titulo = %s
    """, (filme_id,))

    conn.commit()
    conn.close()