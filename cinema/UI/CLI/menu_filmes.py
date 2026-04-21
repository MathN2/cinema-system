from cinema.services import utils
from cinema.data import saving_db, loading_db
import cinema.UI.CLI.coletar_dados_filme as coletar_dados_filme
import cinema.UI.CLI.menu_salas as menu_salas
from cinema.services import filme_services, sessao_services
from cinema.models.sala import Room
from rich.console import Console
from rich.table import Table
import questionary

# ================================================================
#                     MENU PARA O ADMINISTRADOR
# ================================================================
console = Console()

def menu_filmes():
    """
    Exibe a interface para administradores.
    Possibilita gerenciar os filmes e sessoes.

    Funcionabilidades:
        Exibir filmes cadastrados.
        Cadastrar novo filme.
        Remover filme.
        Alterar configuração de filme.
    """

    print("=" * 50)
    print("Filmes".center(50))
    print("=" * 50)
    
    while True:
        choices = [
            questionary.Choice("Cadastrar novo filme", value=1),
            questionary.Choice("Exibir filmes cadastrados", value=2),
            questionary.Choice("Remover filme", value=3),
            questionary.Choice("Alterar configuração de filme", value=4),
            questionary.Separator(),
            questionary.Choice("Sair", value=0)
        ]

        opcao = questionary.select(
            "Escolha:",
            choices=choices
        ).ask()

#         mensagem = """
# 1 - Cadastrar novo filme.
# 2 - Exibir filmes cadastrados.
# 3 - Remover filme.
# 4 - Alterar configuração de filme.
# 0 - Sair.\n"""
#         opcao = utils.validar_int(0, 4, mensagem)


        if opcao == 1:
            dados = coletar_dados_filme.get_movie_data()
            filme = filme_services.create_movie(dados)


            salas = ask_room()

            if salas is None:
                print("Uma sala deve existir para continuar.")
                continue
            if salas == 'canc':
                continue

            data_inicial, data_final = ask_dates()
            horario_inicial, horario_final = ask_schedule()

            filme_id = saving_db.save_movie_db(filme)
            filme.id = filme_id

            config = {
            'data_inicial': data_inicial,
            'data_final': data_final,
            'horario_inicial': horario_inicial,
            'horario_final': horario_final,
            'intervalo': ask_break(),
            'duracao': filme.duracao
            }

            sessoes = sessao_services.create_section(filme, salas, config)

            for sessao in sessoes:
                saving_db.save_section_db(sessao)

            # Divisoria
            print("\n" + "-" * 40 + "\n")


        elif opcao == 2:
            list_movies()


        elif opcao == 3:
            """
            Apaga um filme cadastrado no arquivo JSON.
            """
            filmes = loading_db.load_movies()

            choices = []
            if filmes:
                for index, filme in enumerate(filmes):
                    choices.append(
                        questionary.Choice(
                            f'({filme['titulo']})',
                            value = index
                        )
                    )
            mensagem = "Escolha o filme a ser apagado."
            
            filme_num = questionary.select(
                mensagem,
                choices=choices
            ).ask()

            # list_movies()

            # filme_num = utils.validar_int(1, len(filmes), mensagem)

            filme_id = filmes[filme_num]['id']
            filme_services.delete_movie(filme_id)

            # Divisoria
            print("\n" + "-" * 40 + "\n")

        elif opcao == 4:
            """
            Altera uma propriedade de um filme salvo no arquivo JSON
            """
            lista_filmes = loading_db.load_movies()

            if not lista_filmes:
                console.print("[red]Nenhum filme registrado.[/red]")
                continue

            filme = filme_services.get_movie(lista_filmes)
            campo = filme_services.get_movieattr(filme)
            valor = filme_services.get_value(campo)

            filme_services.update_movie(filme, campo, valor)

            # Divisoria
            print("\n" + "-" * 40 + "\n")

        elif opcao == 0:
            # Volta para o Menu Principal
            print("Voltando para o menu...")
            # Divisoria
            print("\n" + "-" * 40 + "\n")
            break



# Listar Filmes
def list_movies():
    lista_filmes = loading_db.load_movies()
    
    if lista_filmes:
        table = Table(title="Filmes:")

        table.add_column("Nº", justify="right")
        table.add_column("Título", justify="left")


        
        for index, filme in enumerate(lista_filmes):
            table.add_row(
                str(index + 1),
                str(filme['titulo'])
            )

        console.print(table)

    else:
        console.print("[red]Nenhum filme registrado.[/red]")


# SALA:
def ask_room():
    salas = loading_db.load_rooms()
    if not salas:
        print("Não existem salas.")
        return None
    
    salas_escolhidas = []

    while True:
        choices = []

        for index, sala in enumerate(salas):
            label = menu_salas.get_room_label(sala)
            choices.append(
                questionary.Choice(
                    f'sala {sala['numero']} ({label})',
                    value=index
                )
            )

        choices.append(questionary.Separator())
        choices.append(questionary.Choice(
            "Cancelar",
            value="canc"
        ))


        mensagem = "Escolha a(s) sala(s) que o Filme estará disponivel: "

        escolha_sala = questionary.select(
            mensagem,
            choices=choices
        ).ask()

        if escolha_sala == "canc":
            return 'canc'

        sala = Room.from_dict(salas[escolha_sala])

        if menu_salas.is_room_occupied(sala.id):
            print("Sala ocupada. Escolha outra.")
            continue

        if not sala in salas_escolhidas:
            salas_escolhidas.append(sala)
        else:
            print("Sala já selecionada.")

        continuar = questionary.confirm(
            "Deseja adicionar outra sala?"
        ).ask()
        
        if not continuar:
            return salas_escolhidas

# INTERVALO:
def ask_break():
    print("Digite o tempo de intervalo do filme (formato hh:mm): ")
    return utils.to_time() # Converte para datetime.time


# DATAS
def ask_dates():
# DATA INICIAL:
    print('Digite a data inicial para o filme (formato yyyy-mm-dd):')
    data_inicial = utils.to_date()

    # DATA FINAL:
    print('Digite a data final para o filme (formato yyyy-mm-dd):')
    data_final = utils.to_date()

    return data_inicial, data_final

# HORARIOS
def ask_schedule():
    # HORARIO INICIAL:
    print("Digite o horario da primeira sessão desse filme no dia (formato hh:mm): ")
    horario_inicial = utils.to_time()

    # HORARIO FINAL: 
    print("Digite o horario da ultima sessão desse filme no dia (formato hh:mm): ")
    horario_final = utils.to_time()

    return horario_inicial, horario_final

