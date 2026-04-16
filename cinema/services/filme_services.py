from typing import cast
from cinema.data.db import get_connection
from datetime import date

def is_movie_active(filme_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT MIN(DATE(data_hora)),
        MAX(DATE(data_hora))
        FROM sessoes
        WHERE filme_id = %s               
    """, (filme_id,))

    resultado = cast(tuple [date | None, date | None] | None, cursor.fetchone())
    conn.close()

    if not resultado or resultado[0] is None:
        return False
    
    data_inicial, data_final = resultado

    hoje = date.today()

    if data_inicial is None or data_final is None:
        return False
    
    return data_inicial <= hoje <= data_final