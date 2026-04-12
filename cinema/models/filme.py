from datetime import datetime, timedelta, date
# ================================================================
#                           FILME
# ================================================================
class Movie:
    """
    Representa um filme cadastrado no sistema
    """
    _num_id = 0

    def __init__(self, titulo, duracao, sala, intervalo, dias_disponiveis_bool, data_inicial, data_final, horario_inicial, horario_final, filme_id = None, dias_disponiveis=None):
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
        if filme_id is not None:
            self.filme_id = filme_id
        else:
            self.filme_id = self.novo_id()

        if dias_disponiveis is not None:
            self.dias_disponiveis = dias_disponiveis
        else:
            self.dias_disponiveis = self._map_available_days()

        self.filme_id = self.novo_id()
        self.titulo = titulo
        self.duracao = duracao # Formato hh:mm:ss
        self.sala = sala
        self.intervalo = intervalo # Formato hh:mm:ss
        self.dias_disponiveis_bool = dias_disponiveis_bool # SEMANAL
        self.data_inicial = data_inicial
        self.data_final = data_final
        self.horario_inicial = horario_inicial
        self.horario_final = horario_final

        self.dias_disponiveis = self._map_available_days() # SEMANA / Pronto pro Weekday 
        self.horarios_disponiveis = self._available_showtime()
        self.exibicao_ids = self._map_showtime_id()


    @classmethod
    def novo_id(cls):
        cls._num_id += 1
        return cls._num_id
    
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
            'dias_disponiveis_bool': self.dias_disponiveis_bool,
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