from cinema.data.db import get_connection
from cinema.services.filme_services import is_movie_active
"""
Apaga um filme cadastrado no arquivo JSON.
"""

def delete_movie(filme_id):
    conn = get_connection()
    cursor = conn.cursor()

    if not is_movie_active(filme_id):
        cursor.execute("""
            DELETE FROM sessoes
            WHERE filme_id = %s
        """, (filme_id,))
        
        cursor.execute("""
            DELETE FROM filmes
            WHERE id = %s
        """, (filme_id,))


        conn.commit()
        conn.close()
    
    else:
        print("Não foi possivel excluir o filme: Filme está ativo no momento.")