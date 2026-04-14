from cinema.services import utils
from cinema.data import storage
import cinema.UI.CLI.coletar_dados_filme as coletar_dados_filme
import cinema.UI.CLI.menu_salas as menu_salas
from cinema.services import criar_filme, excluir_filme, atualizar_filme, criar_sessao
from cinema.models.sala import Room

# ================================================================
#                     MENU PARA O ADMINISTRADOR
# ================================================================
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
        mensagem = """
1 - Exibir filmes cadastrados.
2 - Cadastrar novo filme.
3 - Remover filme.
4 - Alterar configuração de filme.
0 - Sair.\n"""
        opcao = utils.validar_int(0, 4, mensagem)


        if opcao == 1:
            # Exibe o titulo dos filmes já cadastrados.
            lista_filmes = storage.load_movies()

            print("\n" + "÷" * 40 + "\n")
            
            if lista_filmes:
                for index, key in enumerate(lista_filmes):
                    print(f"{index+1} - {key['titulo']}")
            else:
                print("Nenhum filme registrado.")
                
            print("\n" + "÷" * 40 + "\n")


        elif opcao == 2:
            dados = coletar_dados_filme.get_movie_data()
            filme = criar_filme.create_movie(dados)

            salas = ask_room()

            if salas is None:
                print("Uma sala deve existir para continuar.")
                break

            data_inicial, data_final = ask_dates()
            horario_inicial, horario_final = ask_schedule()

            config = {
            'data_inicial': data_inicial,
            'data_final': data_final,
            'horario_inicial': horario_inicial,
            'horario_final': horario_final,
            'intervalo': ask_break(),
            'duracao': filme.duracao
            }

            sessoes = criar_sessao.create_section(filme, salas, config)

            for sessao in sessoes:
                storage.save_section(sessao)

            storage.save_new_movies(filme)

            # Divisoria
            print("\n" + "-" * 40 + "\n")

        elif opcao == 3:
            """
            Apaga um filme cadastrado no arquivo JSON.
            """
            nome_filme = input('Digite o nome do filme a ser apagado: ')
            nova_lista = excluir_filme.delete_movie(nome_filme)
            storage.save_movie_list(nova_lista)

            # Divisoria
            print("\n" + "-" * 40 + "\n")

        elif opcao == 4:
            """
            Altera uma propriedade de um filme salvo no arquivo JSON
            """
            lista_filmes = storage.load_movies()

            filme = atualizar_filme.get_movie(lista_filmes)
            campo = atualizar_filme.get_movieattr(filme)
            valor = atualizar_filme.get_value(campo)

            filme_atualizado = atualizar_filme.update_movie(filme, campo, valor)

            storage.save_movies(filme_atualizado)

            # Divisoria
            print("\n" + "-" * 40 + "\n")

        elif opcao == 0:
            # Volta para o Menu Principal
            print("Voltando para o menu...")
            # Divisoria
            print("\n" + "-" * 40 + "\n")
            break



# SALA:
def ask_room():
    salas = storage.load_rooms()
    if not salas:
        print("Não existem salas.")
        return None
    
    salas_escolhidas = []

    while True:
        menu_salas._list_rooms()
        mensagem = "Digite a(s) sala(s) que o Filme estará disponivel: "
        mensagem_continuar = "Deseja adicionar outra sala? 1 - Sim | 2 - Não"

        escolha_sala = utils.validar_int(1, len(salas), mensagem)

        sala = Room(**salas[escolha_sala - 1])

        if not sala in salas_escolhidas:
            salas_escolhidas.append(sala)
        else:
            print("Sala já selecionada.")

        escolha_continuar = utils.validar_int(1, 2, mensagem_continuar)
        
        if escolha_continuar == 2:
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