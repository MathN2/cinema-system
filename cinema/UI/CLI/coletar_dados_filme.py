from cinema.services import utils
from cinema.data import loading_db
import json
import questionary
"""
Cadastra um novo filme e salva no arquivo JSON.

Requirements:
    filme_id (int): Identificacao Unica do filme.
    titulo (str): Nome do filme.
    duracao (time): Duracao de cada exibicao do filme.
    sala (ainda n definido):
    intervalo (time): Tempo entre uma sessao e outra.
    dias_disponiveis (dict): Dias da semana disponiveis (bools).
    data_inicial (date): Data de inicio das exibicoes.
    data_final (date): Data final das exibicoes.
    horario_inicial (time): Horario da primeira sessao desse filme no dia.
    horario_final (time): Horario limite para iniciar uma sessao.
""" 

lista_filmes = loading_db.load_movies()

def get_movie_data():
    return {
        'titulo': ask_title(),
        'duracao': ask_duration(),
        'dias_disponiveis': ask_weekdays(),

    }



# FILME_ID: DB vai proporcionar

# TITULO:
def ask_title():
    return input("Digite o Título do Filme: ")

# DURACAO:
def ask_duration():
    print("Digite a duração do filme (formato hh:mm): ")
    return utils.to_time() # Converte para datetime.time

# DIAS_DISPONIVEIS:
def ask_weekdays():

    # Defini lista com os dias da semana.
    dias = [
        'segunda',
        'terca',
        'quarta',
        'quinta',
        'sexta',
        'sabado',
        'domingo'
    ]

    while True:

        choices = [
            questionary.Choice(dia, checked=True)
            for dia in dias
        ]

        selecionados = questionary.checkbox(
            "Escolha os dias da semana que esse filme estará disponivel: ",
            choices=choices
        ).ask()

        confirmar = questionary.confirm(
            "Deseja confirmar os dias selecionados?"
        ).ask()

        # converte para dicionario
        dias_disponiveis_bool = {
            dia: dia in selecionados
            for dia in dias
        }

        if confirmar:
            return dias_disponiveis_bool
        elif not confirmar:
            continue
        else:
            print('Valor invalido.')
            continue