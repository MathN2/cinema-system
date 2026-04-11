# Cria Objeto Movie com os dados coletados e salva no arquivo JSON.
from cinema.data import storage
from cinema.models import filme as fm, sessao

def create_movie(dados):

    titulo = dados['titulo']
    duracao = dados['duracao']
    sala = dados['sala']
    intervalo = dados['intervalo']
    dias_disponiveis = dados['dias_disponiveis']
    data_inicial = dados['data_inicial']
    data_final = dados['data_final']
    horario_inicial = dados['horario_inicial']
    horario_final = dados['horario_final']

    filme = fm.Movie(titulo, duracao, sala, intervalo, dias_disponiveis, data_inicial, data_final, horario_inicial, horario_final)
    return filme