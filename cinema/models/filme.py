from datetime import datetime, timedelta, date
# ================================================================
#                           FILME
# ================================================================
class Movie:
    """
    Representa um filme cadastrado no sistema
    """
    _num_id = 0

    def __init__(self, titulo, duracao, dias_disponiveis_bool, filme_id = None, dias_disponiveis=None):
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

        self.titulo = titulo
        self.duracao = duracao # Formato hh:mm:ss
        self.dias_disponiveis_bool = dias_disponiveis_bool # SEMANAL

        if dias_disponiveis is not None:
            self.dias_disponiveis = dias_disponiveis
        else:
            self.dias_disponiveis = self._map_available_days() # SEMANA / Pronto pro Weekday 


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
            'dias_disponiveis_bool': self.dias_disponiveis_bool,
            'dias_disponiveis': self.dias_disponiveis
            }


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