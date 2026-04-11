# ⋯⋯⋯⋯ Explicacao ⋯⋯⋯⋯
#   Modulo responsavel pelos Objetos, metodos e funcões gerais


# ⋯⋯⋯⋯ To Do ⋯⋯⋯⋯
#  Criar a estrutura de filmes disponíveis [X]
#  Criar sessões por filme (com horários e dias, se decidir incluir) [X]
#  Criar mapa de assentos (ocupados e disponíveis) [X]
#  Implementar a escolha de assento pelo usuário [X]
#  Permitir reserva de assentos [X]


# ================================================================
#                      ENTITIES MODULES
#   Contem as classes principais do sistema:
#   - Section: representa a sessao e o mapa de assentos
#   - Movie: representa o filme e sua logica de exibicao
#   - Funcoes auxiliares: converter_data e converter_tempo
# ================================================================


from datetime import datetime, timedelta, date

# ================================================================
#                           SECTION
# ================================================================
class Section:
    """
    Representa uma sessao de cinema, com seu titulo, ID e mapa de assentos.
    """
    def __init__(self, section_id, filme):
        """
        Inicializa uma nova sessao.

        Args:
            filme: Objeto Movie contendo informacoes do filme
            section_id: Identificador Unico da sessao.
        """
        self.sessao_id = section_id
        self.titulo = filme.titulo
        self.assentos = {
            'A': ['[O]'] * 5,
            'B': ['[O]'] * 5,
            'C': ['[O]'] * 5,
            'D': ['[O]'] * 5,
            'E': ['[O]'] * 5,
        }

# ----------------------------------------------------------------
#                         Exibir Assentos
# ----------------------------------------------------------------
    def show_seats(self):
        """
        Exibe o mapa de assentos da sessao no console.
        """
        print('   1  2  3  4  5')
        for linha, lugares in self.assentos.items():
            print(f'{linha} {"".join(lugares)}')

# ----------------------------------------------------------------
#                         Reservar Assentos
# ----------------------------------------------------------------
    def assign_seat(self):
        """
        Permite ao usuario reservar assentos disponiveis.

        O metodo solicita a quantidade e as posicoes dos assentos.
        Valida as entradas e marca os assentos escolhidos como '[X]'.
        """
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


# ================================================================
#                           FILME
# ================================================================
class Movie:
    """
    Representa um filme cadastrado no sistema
    """
    def __init__(self, filme_id, titulo, duracao, sala, intervalo, dias_disponiveis, data_inicial, data_final, horario_inicial, horario_final):
        # Validar horarios. duracao >= horario_inicial - horario_final
        """
        Inicializa um filme com suas informacoes e horarios disponiveis

        Args:
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
        self.filme_id = filme_id
        self.titulo = titulo
        self.duracao = duracao # Formato hh:mm:ss
        self.sala = sala
        self.intervalo = intervalo # Formato hh:mm:ss
        self.dias_disponiveis_bool = dias_disponiveis # SEMANAL
        self.data_inicial = data_inicial
        self.data_final = data_final
        self.horario_inicial = horario_inicial
        self.horario_final = horario_final

        self.dias_disponiveis = self._map_available_days() # SEMANA / Pronto pro Weekday 
        self.horarios_disponiveis = self._available_showtime()
        self.exibicao_ids = self._map_showtime_id()


# ----------------------------------------------------------------
#                   Converter para Dicionario
# ----------------------------------------------------------------
    def to_dict(self):
        """
        Converte um objeto Movie para dicionario

        Args:
            Objeto Movie
        
        Return:
            Dicionario
        """
        return {'filme_id': self.filme_id,
            'titulo': self.titulo,
            'duracao': self.duracao.strftime("%H:%M:%S"),
            'sala': self.sala,
            'intervalo': self.intervalo.strftime("%H:%M:%S"),
            'dias_disponiveis': self.dias_disponiveis,
            'data_inicial': self.data_inicial.strftime("%Y-%m-%d"),
            'data_final': self.data_final.strftime("%Y-%m-%d"),
            'horario_inicial': self.horario_inicial.strftime("%H:%M:%S"),
            'horario_final': self.horario_final.strftime("%H:%M:%S"),}


# ----------------------------------------------------------------
#                   Mapear Dias Disponiveis
# ----------------------------------------------------------------
    def _map_available_days(self):
        """
        Pega Movie.dias_disponiveis_bool e guarda apenas os valores verdadeiros (True)
        Atribui um valor de 0 a 6 aos dias da semana (0 = segunda, 6 = domingo)

        Args:
            Objeto Movie
        
        Return:
            dias_disponiveis: dicionario com o nome dos dias da semana que o filme sera exibido (key) e sua representação numerica (int)
        """
        dias_disponiveis = {}
        for indice, (dia, valor) in enumerate(self.dias_disponiveis_bool.items()):
            if valor:
                dias_disponiveis[dia] = indice
        
        return dias_disponiveis


# ----------------------------------------------------------------
#                   Horarios Disponiveis
# ----------------------------------------------------------------
    def _available_showtime(self):
        """
        Calcula todos os horarios disponiveis para a exibicao do filme em um dia.

        Args:
            Objeto Movie

        Return:
            horarios_disponiveis: lista com todos os horarios de inicio de exibicao do filme dentro de um dia.
        """
        atual = datetime.combine(date(2000, 1, 1), self.horario_inicial)
        limite = datetime.combine(date(2000, 1, 1), self.horario_final)
        duracao = self.duracao.hour * 60 + self.duracao.minute
        horarios_disponiveis = []

        while atual + timedelta(minutes = duracao) <= limite:
            horarios_disponiveis.append(atual.time())
            atual = atual + timedelta(minutes = duracao) + timedelta(minutes = self.intervalo.hour * 60 + self.intervalo.minute)

        return horarios_disponiveis
    

# ----------------------------------------------------------------
#                           Movie ID
# ----------------------------------------------------------------
    def _map_showtime_id(self):
        """
        Cria uma lista com todas as sessoes do filme, fornecendo um ID para cada uma.

        Return:
            exibicoes_ids: lista contendo o id de cada sessao disponivel do filme
        """
        exibicao_ids = []
        data_atual = self.data_inicial

        while data_atual <= self.data_final:
            for hora in self.horarios_disponiveis:
                 exibicao_ids.append(datetime.combine(data_atual, hora).strftime("%Y-%m-%d_%H:%M"))
            data_atual += timedelta(days=1)

        return exibicao_ids
    

# ================================================================
#                       FUNCOES GERAIS
# ================================================================

# ----------------------------------------------------------------
#                    Converter para time()
# ----------------------------------------------------------------
def to_time():
    """
    Solicita uma str do usuario, faz uma validacao para o formato correto e converte para datetime.time

    Return:
        tempo: valor convertido para datetime.time
    """
    while True:
        entrada = input()
        try:
            tempo = datetime.strptime(entrada, "%H:%M").time()
            return tempo
        except ValueError:
            print('Formato inválido. Use o padrão hh:mm.')


# ----------------------------------------------------------------
#                    Converter para date()
# ----------------------------------------------------------------
def to_date():
    """
    Solicita uma str do usuario, faz uma validacao para o formato correto e converte para datetime.date

    Return:
        data: valor convertido para datetime.date
    """
    while True:
        entrada = input()
        try:
            data = datetime.strptime(entrada, "%Y-%m-%d").date()
            return data
        except ValueError:
            print('Formato inválido. Use o padrão yyyy-mm-dd.')


# ----------------------------------------------------------------
#                       Validar Inteiro
# ----------------------------------------------------------------
def validar_int(inicio=None, fim=None, mensagem_entrada="Digite um número: ", mensagem_erro="Valor inválido. Tente um número."):
    """
    Pede e valida um numero inteiro.

    Args:
        inicio: limita o escopo minimo do numero a ser escolhido. (Caso esse parametro n seja recebido entao inicio = None)
        fim: limita o escopo maximo do numero a ser escolhiudo. (Caso esse parametro n seja recebido entao inicio = None)
        mensagem_entrada: Uma forma de personalizar a mensagem de entrada para o usuario.
        mensagem_erro: Uma forma de personalizar a mensagem de erro para o usuario.

    Return:
        entrada: valor, escolhido pelo usuario, após validação (int).
    """
    while True:
        entrada = input(mensagem_entrada)
        try:
            entrada = int(entrada)
            if inicio is None or fim is None:
                return entrada
            elif inicio <= entrada <= fim:
                return entrada
            else:
                print(mensagem_erro)
        except ValueError:
            print(mensagem_erro)