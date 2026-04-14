from cinema.UI.CLI import paginacao
from cinema.services import utils, criar_sessao, sessao_services
from cinema.models import filme as fm, sessao
from cinema.data import storage

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

        lista_filmes = storage.load_movies()
        if lista_filmes:
            print("Filmes em cartaz:")
            for index, item in enumerate(lista_filmes):
                print(f"{index+1} - {item['titulo']}")
        
            mensagem = "Escolha o filme que deseja assistir: "
            opcao = utils.validar_int(1, len(lista_filmes), mensagem)

            filme = fm.Movie(**lista_filmes[opcao-1])

            # Divisoria
            print("\n" + "-" * 40 + "\n")

            datas = sessao_services.get_section_by_date_hour(filme)

            print("Escolha um dia para assistir o filme: ")
            data_escolhida = paginacao.pagination(datas)

            if data_escolhida is None:
                continue

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

            sessao_obj.show_seats()
            sessao_obj.assign_seat()
            sessao_obj.show_seats()
            storage.save_section(sessao_obj)

            # Divisoria
            print("\n" + "-" * 40 + "\n")
