from cinema.services import utils, criar_sala, excluir_sala
from cinema.UI.CLI import coletar_dados_sala
from cinema.data import storage

def menu_salas():
    print("=" * 50)
    print("Salas".center(50))
    print("=" * 50)

    while True:

        mensagem = '''
1 - Criar sala
2 - Listar salas
3 - Remover sala
0 - Sair
'''

        opcao = utils.validar_int(0, 3, mensagem)

        #================================
        #          Criar Sala
        #================================
        if opcao == 1:
            print('-' * 50)
            print('Criar Sala'.center(50))
            print('-' * 50)

            dados = coletar_dados_sala.get_room_data()
            sala = criar_sala.create_room(dados)

            if sala is None:
                print("Essa sala já existe.\nTente outro número para a sala.")
                continue

            storage.save_room(sala)
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


        if opcao == 3:
            salas = storage.load_rooms()

            if not salas:
                print("Nenhuma sala cadastrada.")
                return

            print('-' * 50)
            print('Excluir Sala'.center(50))
            print('-' * 50)

            _list_rooms()

            mensagem = "Escolha o número da sala a ser excluida: "
            escolha = utils.validar_int(1, len(salas), mensagem)

            sala_id = salas[escolha - 1]['sala_id']
            resultado = excluir_sala.delete_room(sala_id)

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
    salas = storage.load_rooms()

    for index, sala in enumerate(salas):
        print(f'{index + 1} - sala {sala['numero']}')
    
    print('-' * 50)