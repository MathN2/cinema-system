from cinema.data.db import get_connection
import json

def save_movie_db(filme):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    INSERT INTO filmes (titulo, duracao, dias_disponiveis_bool)
    VALUES (%s, %s, %s)
    """
    dias_disponiveis = json.dumps(filme.dias_disponiveis_bool)
    cursor.execute(sql, (filme.titulo, filme.duracao, dias_disponiveis))
    conn.commit()

    filme_id = cursor.lastrowid

    conn.close()
    return filme_id

def save_section_db(sessao):
    conn = get_connection()
    cursor = conn.cursor()

    assentos = {
        linha: [
            1 if cadeira == "[X]" else 0
            for cadeira in colunas
        ]   
        for linha, colunas in sessao.assentos.items()
    }

    assentos_json = json.dumps(assentos)
    data_hora = sessao.data_hora.strftime("%Y-%m-%d %H:%M:%S")

    if getattr(sessao, "id", None) is not None:
        sql = """
        UPDATE sessoes
        SET filme_id = %s, sala_id = %s, data_hora = %s, assentos = %s
        WHERE id = %s
        """
        cursor.execute(
            sql,
            (sessao.filme_id, sessao.sala_id, data_hora, assentos_json, sessao.id)
        )
        sessao_id = sessao.id
    else:
        sql = """
        INSERT INTO sessoes (filme_id, sala_id, data_hora, assentos)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (sessao.filme_id, sessao.sala_id, data_hora, assentos_json))
        sessao_id = cursor.lastrowid

    conn.commit()

    conn.close()
    return sessao_id


def save_room_db(sala):
    conn = get_connection()
    cursor = conn.cursor()


    sql = """
    INSERT INTO salas (numero, linhas, colunas, capacidade)
    VALUES (%s, %s, %s, %s)
    """


    cursor.execute(sql, (sala.numero, sala.linhas, sala.colunas, sala.capacidade))
    conn.commit()

    sala_id = cursor.lastrowid

    conn.close()
    return sala_id
