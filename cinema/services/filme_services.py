from typing import cast
from cinema.data.db import get_connection
from datetime import date
from cinema.services import utils
import cinema.UI.CLI.coletar_dados_filme as cdf
from cinema.models import filme as fm

# Cria Objeto Movie com os dados coletados
def create_movie(dados):

    titulo = dados['titulo']
    duracao = dados['duracao']
    dias_disponiveis_bool = dados['dias_disponiveis']

    filme = fm.Movie(titulo, duracao, dias_disponiveis_bool)
    return filme


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



"""
Altera uma propriedade de um filme salvo no arquivo JSON
"""

def update_movie(filme, campo, valor):
    conn = get_connection()
    cursor = conn.cursor()

    filme_id = filme['id']

    query = f"""
        UPDATE filmes
        SET {campo} = %s
        WHERE id = %s
    """
    cursor.execute(query, (valor, filme_id))
        
    conn.commit()
    conn.close()


def get_movie(lista_filmes):
    if lista_filmes:
        print("Qual filme deseja alterar?")
        for index, key in enumerate(lista_filmes):
            print(f'{index + 1} - {key["titulo"]}')

        filme_selecionado = utils.validar_int(1, len(lista_filmes))
        filme_selecionado = lista_filmes[filme_selecionado - 1]

        return filme_selecionado

# Escolhendo uma propriedade do filme para fazer a alteração
def get_movieattr(filme_selecionado):
    print("Escolha a propriedade que deseja alterar:")
    for index, key in enumerate(filme_selecionado):
        if not key == 'id':
            print(f'{index} - {key}')

    # Convertendo o index para o nome da propriedade
    propriedade_selecionada = utils.validar_int(1, len(filme_selecionado))
    for index, (key, valor) in enumerate(filme_selecionado.items()):
        if index == propriedade_selecionada:
            propriedade_selecionada = key
    
    return propriedade_selecionada

def get_value(campo):
    print(campo)
    if campo in ['duracao', 'intervalo']:
        print("Digite no formato hh:mm (ex: 02:30)")
        return utils.to_time()

    elif campo in ['data_inicial', 'data_final']:
        print("Digite no formato yyyy-mm-dd (ex: 2025-12-31)")
        return utils.to_date()

    elif campo in ['horario_inicial', 'horario_final']:
        print("Digite no formato hh:mm (ex: 18:00)")
        return utils.to_time()

    elif campo == 'dias_disponiveis':
        return cdf.ask_weekdays()
    
    elif campo == 'titulo':
        return input('Digite o novo titulo: ')

    else:
        return input("Digite o novo valor: ")