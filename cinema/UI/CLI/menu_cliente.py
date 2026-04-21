import json

from cinema.UI.CLI import paginacao, menu_filmes
from cinema.services import sessao_services
from cinema.models import filme as fm, sessao
from cinema.data import loading_db, saving_db
import questionary

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


        dados_assentos = sessao_obj.assentos

        for linha, colunas in dados_assentos.items():
            dados_assentos[linha] = [
                sessao_obj._normalizar_cadeira(cadeira)
                for cadeira in colunas
                ]

        total_assentos = sum(linha.count('[O]') for linha in dados_assentos.values())

        while True:
            try:
                num_reservas = int(input('Digite quantos assentos deseja reservar: '))

                if not (1 <= num_reservas <= total_assentos):
                    print(f'Valor invalido. Tente um numero de 1 - {total_assentos}')
                    continue
                break
                    
            except ValueError:
                print(f'Valor invalido. Use um numero inteiro de 1 - {total_assentos}')
        
        n = 0
        while n < num_reservas:
            # Cordenadas do assento, sendo (x) a fileira[A B C D E] e (y) a coluna
            cordenadas = input("Digite o assento (ex: A1): ").upper().replace(" ", "")
            if len(cordenadas) < 2:
                print('Valor Invalido. Use o formato A1, B2, C3, etc.')
                continue

            success = sessao_obj.assign_seat(cordenadas)
            if not success:
                print('Assento invalido ou ja ocupado.')
                decision = questionary.select(
                    "Deseja tentar outro assento?",
                    choices = [
                        questionary.Choice("Sim", value=True),
                        questionary.Choice("Não", value=False)
                    ]
                ).ask()
                if decision:
                    continue
                else:
                    print('Abortando processo de reservas.')
                    break

            n += 1


        sessao_obj.show_seats(filme)

        saving_db.update_section_assentos(sessao_obj)

        # Divisoria
        print("\n" + "-" * 40 + "\n")
