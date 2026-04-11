from datetime import datetime
import models
from data import storage

# ================================================================
#                     MENU PARA O CLIENTE
# ================================================================
def menu_client():
    """
    Mostra os filmes em exibicao e permite o usuario escolher o filme, sessao, assentos para comprar.

    *EM PROGRESSO*
    """
    print('*' * 50)
    print('BEM-VINDO'.center(50, ' '))
    print('*' * 50)

    lista_filmes = storage.load_movies()

    print("Filmes em cartaz:")
    for index, item in enumerate(lista_filmes):
        print(f"{index+1} {item['titulo']}")
    
    mensagem = "Escolha o filme que deseja assistir: /n"
    opcao = models.validar_int(1, len(lista_filmes, mensagem))

    filme = models.Filme(**lista_filmes[opcao-1])

    
    dia_selecionado = int(input("Escolha um dia para assistir o filme:"))

    # self, filme, section_id
    sessao_filme = models.Section(filme, filme.movie_id)
    print(sessao_filme.__dict__)