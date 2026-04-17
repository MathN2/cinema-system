from cinema.services import sala_services
from cinema.UI.CLI import coletar_dados_sala
from cinema.data import saving_db, loading_db
import questionary

def menu_salas():
    print("=" * 50)
    print("Salas".center(50))
    print("=" * 50)

    while True:

        choices = [
            questionary.Choice("Criar sala", value=1),
            questionary.Choice("Listar salas", value=2),
            questionary.Choice("Remover sala", value=3),
            questionary.Choice("Sair", value=0)
        ]

        opcao = questionary.select(
            "Escolha:",
            choices= choices
        ).ask()

        #================================
        #          Criar Sala
        #================================
        if opcao == 1:
            print('-' * 50)
            print('Criar Sala'.center(50))
            print('-' * 50)

            dados = coletar_dados_sala.get_room_data()
            sala = sala_services.create_room(dados)

            if sala is None:
                print("Essa sala já existe.\nTente outro número para a sala.")
                continue
            
            sala_id = saving_db.save_room_db(sala)
            sala.id = sala_id

            print("Sala criada com sucesso.")
            print('-' * 50)
        

        #================================
        #         Listar Salas
        #================================
        if opcao == 2:
            print('-' * 50)
            print('Lista de salas'.center(50))
            print('-' * 50)
            _list_rooms()


        #================================
        #         Excluir Sala
        #================================
        if opcao == 3:
            salas = loading_db.load_rooms()

            if not salas:
                print("Nenhuma sala cadastrada.")
                return

            print('-' * 50)
            print('Excluir Sala'.center(50))
            print('-' * 50)

            choices = []

            for index, sala in enumerate(salas):
                label = get_room_label(sala)
                choices.append(
                    questionary.Choice(
                        f'{index + 1} - sala {sala['numero']} ({label})',
                        value=index
                    )
                )
            
            choices.append(questionary.Separator())
            choices.append(questionary.Choice("Cancelar", value=0))

            escolha = questionary.select(
                "Escolha o número da sala a ser excluida:",
                choices=choices
            ).ask()

            if escolha == 0:
                continue

            sala_id = salas[escolha]['id']
            resultado = sala_services.delete_room(sala_id)

            if resultado == "used":
                print("Não é possível excluir: existem sessões usando esta sala.")

            elif resultado == "notfound":
                print("Sala não encontrada.")

            elif resultado == "ok":
                print("Sala removida com sucesso.")


        if opcao == 0:
            print('-' * 50)
            print('Saindo do gerenciamento de Salas...'.center(50))
            print('-' * 50)
            break


def _list_rooms():
    salas = loading_db.load_rooms()

    for index, sala in enumerate(salas):
        label = get_room_label(sala)
        
        print(f'{index + 1} - sala {sala['numero']} ({label})')
    
    print('-' * 50)


def get_room_label(sala):
    if is_room_occupied(sala["id"]):
        return "🔴 OCUPADA"
    return "🟢 DISPONÍVEL"


def is_room_occupied(sala_id):
    filmes = loading_db.load_movies()

    if not filmes:
        return False

    for filme in filmes:
        sessoes = loading_db.load_sections(filme.get('id'))

        if not sessoes:
            continue
        
        for sessao in sessoes:
            if sessao.get('sala_id') == sala_id:
                return True

    return False