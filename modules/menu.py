# MENU PARA INTERAÇÃO DO USUARIO

#  Definir valores de ingresso (inteira e meia) []
#  Exibir resumo da compra (assento, filme, horário, valor) []
#  Calcular valor total da compra []
#  Login de ADM e login de cliente []
#  Interface de texto (inicial) []
#  (Futuramente) Adicionar interface gráfica []

import models
import storage
from time import sleep


def menu_adm():
    movies = storage.load_movies()

    print("Acessando serviços de Administrador...")
    sleep(1)

    print("""
            1 - Exibir filmes cadastrados.
            2 - Cadastrar novo filme.
            3 - Remover filme.
            4 - Alterar configuração de filme.
            5 - Sair.
            """)
    opt = input("")
    if opt == '1':
        print("")
        for i, t in enumerate(movies):
            print(f"{i+1} - {t['titulo']}")

    elif opt == '2':
        titulo = input("Digite o Título do Filme: ")
        duracao = input("Digite a duração do Filme (em minutos): ")
        sala = input("Digite a(s) sala(s) que o Filme estará disponivel: ")
        intervalo = input("Digite o tempo de intervalo entre uma sessão e outra: ")

        dias_disponiveis = {'domingo': True,
                            'segunda': True,
                            'terca': True,
                            'quarta': True,
                            'quinta': True,
                            'sexta': True,
                            'sabado': True,}
        print("Escolha os dias da semana que esse filme estará disponivel: ")
        while True:
            for index, (dia, valor) in enumerate(dias_disponiveis.items()):
                print(f"{index+1} - {dia.center(8, ' ')} : {valor}")

            print("0 - Concluir")
            switch = input()
            if switch in ('1', '2', '3', '4', '5', '6', '7'):
                switch = int(switch)-1
                chave = list(dias_disponiveis.keys())[switch]
                
                if dias_disponiveis[chave] == True:
                    dias_disponiveis[chave] = False

                elif dias_disponiveis[chave] == False:
                    dias_disponiveis[chave] = True
            
            elif switch == '0':
                break

            else:
                print('Valor invalido.')
                continue

        horario_inicial = input("Digite o horario da primeira sessão desse filme no dia: ")
        horario_final = input("Digite o horario da ultima sessão desse filme no dia: ")

        filme = models.Filme(titulo, duracao, sala, intervalo, dias_disponiveis, horario_inicial, horario_final)
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
            print(f'{index + 1} - {chave}')
        
        # Convertendo o index para o nome da propriedade
        property_chosen = int(input()) - 1
        for index, (chave, valor) in enumerate(movie_chosen.items()):
            print(index, chave)
            if index == property_chosen:
                property_chosen = chave 

        # Interface dos dias da semana disponivel, caso essa seja a alteração do usuario
        if property_chosen == 'dias_disponiveis':
            print("Escolha os dias da semana que esse filme estará disponivel: ")
            dias_disponiveis = movie_chosen['dias_disponiveis']
            while True:
                for index, (dia, valor) in enumerate(dias_disponiveis.items()):
                    print(f"{index+1} - {dia.center(8, ' ')} : {valor}")
                    print("0 - Concluir")

                switch = input()
                if switch in ('1', '2', '3', '4', '5', '6', '7'):
                    switch = int(switch)-1
                    chave = list(dias_disponiveis.keys())[switch]
                    
                    if dias_disponiveis[chave] == True:
                        dias_disponiveis[chave] = False

                    elif dias_disponiveis[chave] == False:
                        dias_disponiveis[chave] = True
                
                elif switch == '0':
                    break

                else:
                    print('Valor invalido.')
                    continue
        
        else:
            new_value = input(f"Digite o novo valor para a propriedade ({property_chosen}) do filme ({movie_chosen['titulo']}): ")
            movie_chosen[property_chosen] = new_value
            
        storage.save_movies(movies)

            

    # elif opt == '5':



def menu_client():
    print('*' * 50)
    print('BEM-VINDO'.center(50, ' '))
    print('*' * 50)

    print("Filmes em cartaz:")
    

def Menu():
    print("Iniciando Sistema Cinema")

    print('LOGN IN')
    adm = input('1 - ADMINISTRADOR\n2 - CLIENTE\n')
    adm = True if adm == '1' else False

    if adm == True:
        menu_adm()
        
    else:
        menu_client()
Menu()