# MENU PARA INTERAÇÃO DO USUARIO

#  Definir valores de ingresso (inteira e meia) []
#  Exibir resumo da compra (assento, filme, horário, valor) []
#  Calcular valor total da compra []
#  Login de ADM e login de cliente []
#  Interface de texto (inicial) []
#  (Futuramente) Adicionar interface gráfica []

from datetime import datetime
import models
import storage
from time import sleep


def menu_adm():
    movies = storage.load_movies()

    print("Acessando serviços de Administrador...")
    # sleep(0.3)

    print("""
            1 - Exibir filmes cadastrados.
            2 - Cadastrar novo filme.
            3 - Remover filme.
            4 - Alterar configuração de filme.
            5 - Sair.
            """)
    opt = input("")#Validar
    if opt == '1':
        print("")
        for i, t in enumerate(movies):
            print(f"{i+1} - {t['titulo']}")

    elif opt == '2':
        titulo = input("Digite o Título do Filme: ")

        print("Digite a duração do filme (formato hh:mm): ")
        duracao = models.converter_tempo()

        sala = input("Digite a(s) sala(s) que o Filme estará disponivel: ")#Validar e Melhorar

        print("Digite o tempo de intervalo do filme (formato hh:mm): ")
        intervalo = models.converter_tempo()

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
            switch = input()
            if switch in ('1', '2', '3', '4', '5', '6', '7'):
                switch = int(switch)-1
                chave = list(dias_disponiveis_bool.keys())[switch]
                
                if dias_disponiveis_bool[chave] == True:
                    dias_disponiveis_bool[chave] = False

                elif dias_disponiveis_bool[chave] == False:
                    dias_disponiveis_bool[chave] = True
            
            elif switch == '0':
                break

            else:
                print('Valor invalido.')
                continue

        print('Digite a data inicial para o filme (formato yyyy-mm-dd):')
        data_inicial = models.converter_data()

        print('Digite a data final para o filme (formato yyyy-mm-dd):')
        data_final = models.converter_data()
        
        print("Digite o horario da primeira sessão desse filme no dia (formato hh:mm): ")
        horario_inicial = models.converter_tempo()

        print("Digite o horario da ultima sessão desse filme no dia (formato hh:mm): ")
        horario_final = models.converter_tempo()

        filme = models.Filme(titulo, duracao, sala, intervalo, dias_disponiveis_bool, data_inicial, data_final, horario_inicial, horario_final)
        storage.save_new_movies(filme)


    elif opt == '3':
        nome_filme = input('Digite o nome do filme a ser apagado: ')

        for index, filme in enumerate(movies):
            if filme["titulo"].lower() == nome_filme.lower():
                print(filme['titulo'], nome_filme)
                del movies[index]
                break

        storage.save_movies(movies)


    elif opt == '4':
        # Escolhendo um filme para fazer a alteração
        print("Qual filme deseja alterar?")
        for index, filme in enumerate(movies):
            print(f'{index + 1} - {filme["titulo"]}')
        
        movie_chosen = int(input()) - 1
        movie_chosen = movies[movie_chosen]

        # Escolhendo uma propriedade do filme para fazer a alteração
        print("Escolha a propriedade que deseja alterar:")
        for index, chave in enumerate(movie_chosen):
            if not chave == 'id':
                print(f'{index} - {chave}')
        
        # Convertendo o index para o nome da propriedade
        property_chosen = int(input()) #Validar
        for index, (chave, valor) in enumerate(movie_chosen.items()):
            if not chave == 'id':
                print(index, chave)
            if index == property_chosen:
                property_chosen = chave 

        #Propriedades dos filmes(titulo, duracao, sala, intervalo, dias_disponiveis, data_inicial, data_final, horario_inicial, horario_final)
        # Alterar Titulo do Filme
        if property_chosen == 'titulo':
            movie_chosen['titulo'] = input('Digite o novo TITULO para o filme: ')

        # Alterar Duracao do Filme
        elif property_chosen == 'duracao':
            print("Digite a nova duração do filme (formato hh:mm): ")
            movie_chosen['duracao'] = models.converter_tempo()

        # Alterar Salas do Filme
        elif property_chosen == 'sala': # Ainda vou definir o formato das salas
            movie_chosen['sala'] = input()

        # Alterar Intervalo entre sessoes do Filme
        elif property_chosen == 'intervalo':
            print('Digite o novo tempo de intervalo do filme (formato hh:mm): ')
            movie_chosen['intervalo'] = models.converter_tempo()

        # Interface dos dias da semana disponivel, caso essa seja a alteração do usuario
        elif property_chosen == 'dias_disponiveis_bool':
            print("Escolha os dias da semana que esse filme estará disponivel: ")
            dias_disponiveis_bool = movie_chosen['dias_disponiveis_bool']
            while True:
                for index, (dia, valor) in enumerate(dias_disponiveis_bool.items()):
                    print(f"{index+1} - {dia.center(8, ' ')} : {valor}")
                    print("0 - Concluir")

                switch = input() #Validar
                if switch in ('1', '2', '3', '4', '5', '6', '7'):
                    switch = int(switch)-1
                    chave = list(dias_disponiveis_bool.keys())[switch]
                    
                    if dias_disponiveis_bool[chave] == True:
                        dias_disponiveis_bool[chave] = False

                    elif dias_disponiveis_bool[chave] == False:
                        dias_disponiveis_bool[chave] = True
                
                elif switch == '0':
                    break

                else:
                    print('Valor invalido.')
                    continue

        # Alterar data que indica primeiro dia de exibicao do filme
        elif property_chosen == 'data_inicial':
            print('Digite a nova data inicial para o filme (formato yyyy-mm-dd):')
            movie_chosen['data_inicial'] = models.converter_data()

        # Alterar data que indica ultimo dia de exibicao do filme
        elif property_chosen == 'data_final':
            print('Digite a nova data final para o filme (formato yyyy-mm-dd):')
            movie_chosen['data_final'] = models.converter_data()

        # Alterar horario da primeira exibicao do dia
        elif property_chosen == 'horario_inicial':
            print("Digite o horario da primeira sessão desse filme no dia (formato hh:mm): ")
            movie_chosen['horario_inicial'] = models.converter_tempo()

        # Alterar horario ultimo possivel para exibicao do dia
        elif property_chosen == 'horario_final':
            print("Digite o horario da ultima sessão desse filme no dia (formato hh:mm): ")
            movie_chosen['horario_final'] = models.converter_tempo()

        else:
            new_value = input(f"Digite o novo valor para a propriedade ({property_chosen}) do filme ({movie_chosen['titulo']}): ")
            movie_chosen[property_chosen] = new_value
        
        movie_chosen = models.Filme(**movie_chosen)
        storage.save_movies(movie_chosen)



    elif opt == '5':
        print("Voltando para o menu...")
        sleep(0.3)



def menu_client():
    print('*' * 50)
    print('BEM-VINDO'.center(50, ' '))
    print('*' * 50)

    movies = storage.load_movies()

    print("Filmes em cartaz:")
    for index, item in enumerate(movies):
        print(f"{index+1} {item['titulo']}")
    
    opt = int(input("Escolha o filme que deseja assistir: /n")) #Validar

    filme = models.Filme(**movies[opt-1])

    
    user_day = int(input("Escolha um dia para assistir o filme:"))

    # self, filme, section_id)
    filme_section = models.Section(filme, filme.movie_id)
    print(filme_section.__dict__)



def Menu():
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
Menu()