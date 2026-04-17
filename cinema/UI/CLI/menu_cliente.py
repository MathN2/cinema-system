from cinema.UI.CLI import paginacao, menu_filmes
from cinema.services import utils, sessao_services
from cinema.models import filme as fm, sessao
from cinema.data import loading_db, saving_db
import questionary
from rich import table

# ================================================================
#                     MENU PARA O CLIENTE
# ================================================================
def menu_client():
    """
    Mostra os filmes em exibicao e permite o usuario escolher o filme, sessao, assentos para comprar.

    *EM PROGRESSO*
    """
    while True:
        print('*' * 50)
        print('BEM-VINDO'.center(50, ' '))
        print('*' * 50)

        lista_filmes = loading_db.load_movies()
        if not lista_filmes:
            print("Nenhum filme em cartaz.")
            break

        menu_filmes.list_movies()
        
        escolhas = []

        for index, item in enumerate(lista_filmes):
            escolhas.append(
                questionary.Choice(
                    f"{index+1} - {item['titulo']}",
                    value = index
                )
            )
        
    
        mensagem = "Escolha o filme que deseja assistir: "

        opcao = questionary.select(
            mensagem,
            choices = escolhas
        ).ask()

        if opcao is None:
            return

        filme = fm.Movie(**lista_filmes[opcao])

        # Divisoria
        print("\n" + "-" * 40 + "\n")

        datas = sessao_services.get_section_by_date_hour(filme)

        print("Escolha um dia para assistir o filme: ")
        data_escolhida = paginacao.pagination(datas)

        if data_escolhida is None:
            break

        # Divisoria
        print("\n" + "-" * 40 + "\n")
        
        print("Escolha um horario: ")
        horarios = data_escolhida['horarios']
        horario_escolhido = paginacao.pagination(
                [{"label": h} for h in horarios]
            )
        
        if horario_escolhido is None:
            continue


        data_hora = f"{data_escolhida['data']}_{horario_escolhido['label']}"
        dados_sessao = sessao_services.get_section(filme, data_hora)

        if dados_sessao is None:
            continue

        sessao_obj = sessao.Section.from_dict(dados_sessao)

        sessao_obj.show_seats(filme)
        sessao_obj.assign_seat()
        sessao_obj.show_seats(filme)

        saving_db.save_section_db(sessao_obj)

        # Divisoria
        print("\n" + "-" * 40 + "\n")
