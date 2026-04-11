"""
Altera uma propriedade de um filme salvo no arquivo JSON
"""
import cinema.data.storage as storage
from cinema.services import utils
import cinema.UI.CLI.coletar_dados_filme as cdf


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
        if not key == 'filme_id':
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


def update_movie(filme, campo, valor):
    filme[campo] = valor

    if campo == 'dias_disponiveis':
        from cinema.models.filme import Movie

        novo_filme = Movie(**filme)
        return novo_filme
        
    return filme