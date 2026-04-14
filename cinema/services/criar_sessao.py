from datetime import datetime, timedelta, date
from cinema.models.sessao import Section
import cinema.models.filme as fm

def create_section(filme: fm.Movie, salas, config):
    if not isinstance(filme, fm.Movie):
        raise TypeError("filme deve ser um objeto Movie")
    
    horarios = _generate_schedule(config)
    datas = _generate_dates(config, horarios)
    
    sessoes = []

    for sala in salas:
        for data in datas:
            for horario in horarios:
                data_hora = datetime.combine(data, horario)

                sessoes.append(Section(filme, sala, data_hora))

    return sessoes



# ----------------------------------------------------------------
#                           Movie ID
# ----------------------------------------------------------------
def _generate_dates(config, horarios):
    """
    Cria uma lista com todas as sessoes do filme, fornecendo um ID para cada uma.

    Return:
        exibicoes_ids: lista contendo o id de cada sessao disponivel do filme
    """
    datas= []

    data_atual = config.get('data_inicial')
    data_final = config.get('data_final')

    while data_atual <= data_final:
        datas.append(data_atual)
        data_atual += timedelta(days=1)

    return datas



# ----------------------------------------------------------------
#                   Horarios Disponiveis
# ----------------------------------------------------------------
def _generate_schedule(config):
    """
    Calcula todos os horarios disponiveis para a exibicao do filme em um dia.

    Args:
        Objeto Movie

    Return:
        horarios: lista com todos os horarios de inicio de exibicao do filme dentro de um dia.
    """
    horario_inicial = config.get('horario_inicial')
    horario_final = config.get('horario_final')
    intervalo = config.get('intervalo')
    duracao = config.get('duracao')

    atual = datetime.combine(date(2000, 1, 1), horario_inicial)
    limite = datetime.combine(date(2000, 1, 1), horario_final)
    duracao = duracao.hour * 60 + duracao.minute
    horarios = []

    while atual + timedelta(minutes = duracao) <= limite:
        horarios.append(atual.time())
        atual = atual + timedelta(minutes = duracao) + timedelta(minutes = intervalo.hour * 60 + intervalo.minute)

    return horarios