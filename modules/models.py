# OBJETOS E METODOS PRINCIPAIS

#  Criar a estrutura de filmes disponíveis [X]
#  Criar sessões por filme (com horários e dias, se decidir incluir) [X]
#  Criar mapa de assentos (ocupados e disponíveis) [X]
#  Implementar a escolha de assento pelo usuário [X]
#  Permitir reserva de assentos [X]

from datetime import datetime, timedelta, date

class Section:
    def __init__(self, filme, section_id):
        self.titulo = filme
        self.id = section_id
        self.assentos = {
            'A': ['[O]'] * 5,
            'B': ['[O]'] * 5,
            'C': ['[O]'] * 5,
            'D': ['[O]'] * 5,
            'E': ['[O]'] * 5,
        }

    def exibir_assentos(self):
        print('   1  2  3  4  5')
        for index, linha in enumerate(self.assentos):
            print(f'{linha} {"".join(self.assentos[linha])}')

    def reservar_assento(self):
        while True:
            try:
                total_assentos = sum(linha.count('[O]') for linha in self.assentos.values())
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
            cordenadas = input('Digite o assento que deseja reservar: ').upper().replace(" ", "")
            if len(cordenadas) < 2:
                print('Valor Invalido. Use o formato A1, B2, C3, etc.')
                continue
            x = cordenadas[0]
            y = cordenadas[1:]

            if not y.isdigit():
                print('Valor Invalido.')
                continue
            y = int(y) - 1 # Deve ser -1 para dar match com o index do dicionario
            
            if x not in self.assentos or not 0 <= y < len(self.assentos[x]):
                print('Esse assento nao existe.')
                continue
            
            if self.assentos[x][y] == '[X]':
                print('Esse assento nao esta disponivel.')
                
                while True:
                    decision = input('Deseja continuar? (S/N): ').upper()
                    if decision == 'S':
                        break
                    elif decision == 'N':
                        return
                    else:
                        print('Valor Invalido.')

            self.assentos[x][y] = '[X]'
            
            n += 1

# section1 = Section('Harry potter')
# section1.exibir_assentos()
# section1.reservar_assento()
# section1.exibir_assentos()

class Filme: #ADM
    def __init__(self, id, titulo, duracao, sala, intervalo, dias_disponiveis, data_inicial, data_final, horario_inicial, horario_final):
        # Validar horarios. duracao >= horario_inicial - horario_final
        self.id = id
        self.titulo = titulo
        self.duracao = duracao # Formato hh:mm
        self.sala = sala
        self.intervalo = intervalo # Formato hh:mm
        self.dias_bool = dias_disponiveis # SEMANA
        self.dias_disponiveis = self.filtrar_dias() # SEMANA / Pronto pro Weekday 
        self.data_inicial = data_inicial
        self.data_final = data_final
        self.horario_inicial = horario_inicial
        self.horario_final = horario_final
        self.horarios_disponiveis = self.horarios_disponiveis()
        self.movie_id = self.movie_id()

    
    def to_dict(self):
        return {'id': self.id,
            'titulo': self.titulo,
            'duracao': self.duracao.strftime("%H:%M:%S"),
            'sala': self.sala,
            'intervalo': self.intervalo.strftime("%H:%M:%S"),
            'dias_disponiveis': self.dias_disponiveis,
            'data_inicial': self.data_inicial.strftime("%Y-%m-%d"),
            'data_final': self.data_final.strftime("%Y-%m-%d"),
            'horario_inicial': self.horario_inicial.strftime("%H:%M:%S"),
            'horario_final': self.horario_final.strftime("%H:%M:%S"),}


    def filtrar_dias(self):
        # Filtrando e Tratando Dias Disponiveis
        dias_disponiveis = {}
        for indice, (dia, valor) in enumerate(self.dias_bool.items()):
            if valor:
                dias_disponiveis[dia] = indice
        
        return dias_disponiveis


    def horarios_disponiveis(self):
        atual = datetime.combine(date(2000, 1, 1), self.horario_inicial)
        limite = datetime.combine(date(2000, 1, 1), self.horario_final)
        duracao = self.duracao.hour * 60 + self.duracao.minute
        horarios_disponiveis = []

        while atual + timedelta(minutes = duracao) <= limite:
            horarios_disponiveis.append(atual.time())
            atual = atual + timedelta(minutes = duracao) + timedelta(minutes = self.intervalo.hour * 60 + self.intervalo.minute)

        return horarios_disponiveis
    

    def movie_id(self):
        movie_id = []
        data_atual = self.data_inicial

        while data_atual <= self.data_final:
            for hora in self.horarios_disponiveis:
                 movie_id.append(datetime.combine(data_atual, hora).strftime("%Y-%m-%d_%H:%M"))
            data_atual += timedelta(days=1)

        return movie_id
    

def converter_tempo():
    while True:
        entrada = input()
        try:
            duracao = datetime.strptime(entrada, "%H:%M").time()
            return duracao
        except ValueError:
            print('Formato inválido. Use o padrão hh:mm.')

def converter_data():
    while True:
        entrada = input()
        try:
            data = datetime.strptime(entrada, "%Y-%m-%d").date()
            return data
        except ValueError:
            print('Formato inválido. Use o padrão yyyy-mm-dd.')