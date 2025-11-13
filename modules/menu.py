# ⋯⋯⋯⋯ Explicacao ⋯⋯⋯⋯
#     Interface no terminal para interacao direta com o usuario (Administrador ou Cliente).


# ⋯⋯⋯⋯ To Do ⋯⋯⋯⋯
#     Definir valores de ingresso (inteira e meia) []
#     Exibir resumo da compra (assento, filme, horário, valor) []
#     Calcular valor total da compra []
#     Login de ADM e login de cliente []
#     Interface de texto (inicial) []
#     (Futuramente) Adicionar interface gráfica []


from datetime import datetime
import models
import storage


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

    lista_filmes = storage.load_movies()

    print("Acessando serviços de Administrador...")

    mensagem = """
            1 - Exibir filmes cadastrados.
            2 - Cadastrar novo filme.
            3 - Remover filme.
            4 - Alterar configuração de filme.
            0 - Sair.\n"""
    opcao = models.validar_int(0, 4, mensagem)

    if opcao == 1:
        # Exibe o titulo dos filmes já cadastrados.

        print("") # Apenas para criar um espaçamento
        for index, key in enumerate(lista_filmes):
            print(f"{index+1} - {key['titulo']}")
        print("") # Apenas para criar um espaçamento

    elif opcao == 2:
        """
        Cadastra um novo filme e salva no arquivo JSON.

        Requirements:
            filme_id (int): Identificacao Unica do filme.
            titulo (str): Nome do filme.
            duracao (time): Duracao de cada exibicao do filme.
            sala (ainda n definido):
            intervalo (time): Tempo entre uma sessao e outra.
            dias_disponiveis (dict): Dias da semana disponiveis (bools).
            data_inicial (date): Data de inicio das exibicoes.
            data_final (date): Data final das exibicoes.
            horario_inicial (time): Horario da primeira sessao desse filme no dia.
            horario_final (time): Horario limite para iniciar uma sessao.
        """ 
        # FILME_ID:
        filme_id = len(lista_filmes)

        # TITULO:
        titulo = input("Digite o Título do Filme: ")

        # DURACAO:
        print("Digite a duração do filme (formato hh:mm): ")
        duracao = models.converter_tempo() # Converte para datetime.time

        # SALA:
        sala = input("Digite a(s) sala(s) que o Filme estará disponivel: ")#Validar e Melhorar

        # INTERVALO:
        print("Digite o tempo de intervalo do filme (formato hh:mm): ")
        intervalo = models.converter_tempo() # Converte para datetime.time

        # DIAS_DISPONIVEIS:
        
        # Defini dicionario com os dias da semana.
        dias_disponiveis_bool = {
                            'segunda': True,
                            'terca': True,
                            'quarta': True,
                            'quinta': True,
                            'sexta': True,
                            'sabado': True,
                            'domingo': True
                            }
        
        print("Escolha os dias da semana que esse filme estará disponivel: ")
        while True:
            for index, (dia, valor) in enumerate(dias_disponiveis_bool.items()):
                print(f"{index+1} - {dia.center(8, ' ')} : {valor}")
            print("0 - Concluir")

            # Possibilita o administrador escolher quais dias o filme estará disponivel (mudando dias_disponiveis_bool entre True e False)
            alternar_dia = input()
            if alternar_dia in ('1', '2', '3', '4', '5', '6', '7'):
                alternar_dia = int(alternar_dia)-1
                chave = list(dias_disponiveis_bool.keys())[alternar_dia]
                
                if dias_disponiveis_bool[chave] == True:
                    dias_disponiveis_bool[chave] = False

                elif dias_disponiveis_bool[chave] == False:
                    dias_disponiveis_bool[chave] = True
            
            elif alternar_dia == '0':
                break

            else:
                print('Valor invalido.')
                continue
        
        # DATA INICIAL:
        print('Digite a data inicial para o filme (formato yyyy-mm-dd):')
        data_inicial = models.converter_data()

        # DATA FINAL:
        print('Digite a data final para o filme (formato yyyy-mm-dd):')
        data_final = models.converter_data()
        
        # HORARIO INICIAL:
        print("Digite o horario da primeira sessão desse filme no dia (formato hh:mm): ")
        horario_inicial = models.converter_tempo()

        # HORARIO FINAL: 
        print("Digite o horario da ultima sessão desse filme no dia (formato hh:mm): ")
        horario_final = models.converter_tempo()

        # Cria Objeto Movie com os dados coletados e salva no arquivo JSON.
        filme = models.Filme(filme_id, titulo, duracao, sala, intervalo, dias_disponiveis_bool, data_inicial, data_final, horario_inicial, horario_final)
        storage.save_new_movies(filme)


    elif opcao == 3:
        """
        Apaga um filme cadastrado no arquivo JSON.
        """
        nome_filme = input('Digite o nome do filme a ser apagado: ')

        for index, key in enumerate(lista_filmes):
            if key["titulo"].lower() == nome_filme.lower():
                print(key['titulo'], nome_filme)
                del lista_filmes[index]
                break

        storage.save_movies(lista_filmes)


    elif opcao == 4:
        """
        Altera uma propriedade de um filme salvo no arquivo JSON
        """
        print("Qual filme deseja alterar?")
        for index, key in enumerate(lista_filmes):
            print(f'{index + 1} - {key["titulo"]}')
        
        filme_selecionado = int(input()) - 1
        filme_selecionado = lista_filmes[filme_selecionado]

        # Escolhendo uma propriedade do filme para fazer a alteração
        print("Escolha a propriedade que deseja alterar:")
        for index, key in enumerate(filme_selecionado):
            if not key == 'id':
                print(f'{index} - {key}')
        
        # Convertendo o index para o nome da propriedade
        propriedade_selecionada = models.validar_int(1, len(filme_selecionado))
        for index, (key, valor) in enumerate(filme_selecionado.items()):
            if not key == 'id':
                print(index, key)
            if index == propriedade_selecionada:
                propriedade_selecionada = key 

        #Propriedades dos filmes(titulo, duracao, sala, intervalo, dias_disponiveis, data_inicial, data_final, horario_inicial, horario_final)
        # Alterar Titulo do Filme
        if propriedade_selecionada == 'titulo':
            filme_selecionado['titulo'] = input('Digite o novo TITULO para o filme: ')

        # Alterar Duracao do Filme
        elif propriedade_selecionada == 'duracao':
            print("Digite a nova duração do filme (formato hh:mm): ")
            filme_selecionado['duracao'] = models.converter_tempo()

        # Alterar Salas do Filme
        elif propriedade_selecionada == 'sala': # Ainda vou definir o formato das salas
            filme_selecionado['sala'] = input()

        # Alterar Intervalo entre sessoes do Filme
        elif propriedade_selecionada == 'intervalo':
            print('Digite o novo tempo de intervalo do filme (formato hh:mm): ')
            filme_selecionado['intervalo'] = models.converter_tempo()

        # Interface dos dias da semana disponivel, caso essa seja a alteração do usuario
        elif propriedade_selecionada == 'dias_disponiveis_bool':
            print("Escolha os dias da semana que esse filme estará disponivel: ")
            dias_disponiveis_bool = filme_selecionado['dias_disponiveis_bool']
            while True:
                for index, (dia, valor) in enumerate(dias_disponiveis_bool.items()):
                    print(f"{index+1} - {dia.center(8, ' ')} : {valor}")
                    print("0 - Concluir")

                alternar_dia = input()
                if alternar_dia in ('1', '2', '3', '4', '5', '6', '7'):
                    alternar_dia = int(alternar_dia)-1
                    key = list(dias_disponiveis_bool.keys())[alternar_dia]
                    
                    if dias_disponiveis_bool[key] == True:
                        dias_disponiveis_bool[key] = False

                    elif dias_disponiveis_bool[key] == False:
                        dias_disponiveis_bool[key] = True
                
                elif alternar_dia == '0':
                    break

                else:
                    print('Valor invalido.')
                    continue

        # Alterar data que indica primeiro dia de exibicao do filme
        elif propriedade_selecionada == 'data_inicial':
            print('Digite a nova data inicial para o filme (formato yyyy-mm-dd):')
            filme_selecionado['data_inicial'] = models.converter_data()

        # Alterar data que indica ultimo dia de exibicao do filme
        elif propriedade_selecionada == 'data_final':
            print('Digite a nova data final para o filme (formato yyyy-mm-dd):')
            filme_selecionado['data_final'] = models.converter_data()

        # Alterar horario da primeira exibicao do dia
        elif propriedade_selecionada == 'horario_inicial':
            print("Digite o horario da primeira sessão desse filme no dia (formato hh:mm): ")
            filme_selecionado['horario_inicial'] = models.converter_tempo()

        # Alterar horario ultimo possivel para exibicao do dia
        elif propriedade_selecionada == 'horario_final':
            print("Digite o horario da ultima sessão desse filme no dia (formato hh:mm): ")
            filme_selecionado['horario_final'] = models.converter_tempo()

        else:
            new_value = input(f"Digite o novo valor para a propriedade ({propriedade_selecionada}) do filme ({filme_selecionado['titulo']}): ")
            filme_selecionado[propriedade_selecionada] = new_value
        
        filme_selecionado = models.Filme(**filme_selecionado)
        storage.save_movies(filme_selecionado)


    elif opcao == 0:
        # Volta para o Menu Principal
        print("Voltando para o menu...")



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
    opcao = models.validar_int(1, len(lista_filmes))

    filme = models.Filme(**lista_filmes[opcao-1])

    
    dia_selecionado = int(input("Escolha um dia para assistir o filme:"))

    # self, filme, section_id
    sessao_filme = models.Section(filme, filme.movie_id)
    print(sessao_filme.__dict__)



# ================================================================
#                       MENU PRINCIPAL
# ================================================================
def menu_principal():
    """
    Mostra o menu principal, permitindo o usuario escolher o tipo de Login fazer (Administrador ou Cliente).

    *EM PROGRESSO*
    """
    print("Iniciando Sistema Cinema")
    while True:
        print('LOGN IN')
        #Melhorar
        adm = input('1 - ADMINISTRADOR\n2 - CLIENTE\n')
        adm = True if adm == '1' else False

        if adm == True:
            menu_adm()
            
        else:
            menu_client()
menu_principal()