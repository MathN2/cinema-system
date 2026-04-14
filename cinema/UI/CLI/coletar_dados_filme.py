from cinema.services import utils
from cinema.data import storage
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

lista_filmes = storage.load_movies()

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

    # Defini dicionario com os dias da semana.
    dias_disponiveis_bool = {
                    'segunda': True,
                    'terca': True,
                    'quarta': True,
                    'quinta': True,
                    'sexta': True,
                    'sabado': True,
                    'domingo': True
                    }

    print("Escolha os dias da semana que esse filme estará disponivel: ")
    while True:
        for index, (dia, valor) in enumerate(dias_disponiveis_bool.items()):
            print(f"{index+1} - {dia.center(8, ' ')} : {valor}")
        print("0 - Concluir")

        # Possibilita o administrador escolher quais dias o filme estará disponivel (mudando dias_disponiveis_bool entre True e False)
        alternar_dia = input()
        if alternar_dia in ('1', '2', '3', '4', '5', '6', '7'):
            alternar_dia = int(alternar_dia)-1
            chave = list(dias_disponiveis_bool.keys())[alternar_dia]
            
            dias_disponiveis_bool[chave] = not dias_disponiveis_bool[chave]
        
        elif alternar_dia == '0':
            return dias_disponiveis_bool

        else:
            print('Valor invalido.')
            continue