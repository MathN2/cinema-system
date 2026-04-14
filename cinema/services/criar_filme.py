# Cria Objeto Movie com os dados coletados e salva no arquivo JSON.
from cinema.data import storage
from cinema.models import filme as fm, sessao

def create_movie(dados):

    titulo = dados['titulo']
    duracao = dados['duracao']
    dias_disponiveis_bool = dados['dias_disponiveis']

    filme = fm.Movie(titulo, duracao, dias_disponiveis_bool)
    return filme