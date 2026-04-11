from datetime import datetime
from cinema.services import utils
from cinema.data import storage
import cinema.UI.CLI.coletar_dados_filme as coletar_dados_filme
from cinema.services import criar_filme, excluir_filme, atualizar_filme, criar_sessao

# ================================================================
#                     MENU PARA O ADMINISTRADOR
# ================================================================
def menu_adm():
    """
    Exibe a interface para administradores.
    Possibilita gerenciar os filmes e sessoes.

    Funcionabilidades:
        Exibir filmes cadastrados.
        Cadastrar novo filme.
        Remover filme.
        Alterar configuração de filme.
    """

    print("Acessando serviços de Administrador...")

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

        print("") # Apenas para criar um espaçamento
        if lista_filmes:
            for index, key in enumerate(lista_filmes):
                print(f"{index+1} - {key['titulo']}")
        else:
            print("Nenhum filme registrado.")
        print("") # Apenas para criar um espaçamento

    elif opcao == 2:
       dados = coletar_dados_filme.get_movie_data()
       filme = criar_filme.create_movie(dados)
       sessoes = criar_sessao.create_section(filme)

       for sessao in sessoes:
           storage.save_section(sessao)

       storage.save_new_movies(filme)

    elif opcao == 3:
        """
        Apaga um filme cadastrado no arquivo JSON.
        """
        nome_filme = input('Digite o nome do filme a ser apagado: ')
        nova_lista = excluir_filme.delete_movie(nome_filme)
        storage.save_movie_list(nova_lista)


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


    elif opcao == 0:
        # Volta para o Menu Principal
        print("Voltando para o menu...")