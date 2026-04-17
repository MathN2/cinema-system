from datetime import datetime, time, date, timedelta
import pytest

from cinema.services.sessao_services import (
    create_section,
    _generate_dates,
    _generate_schedule
)

import cinema.models.filme as fm


# --------------------------------------------------
# 🔵 helpers
# --------------------------------------------------

class DummySala:
    def __init__(self, id):
        self.id = id

    def create_map_seat(self):
        return {
            'A': ['O'] * 10
        }


# --------------------------------------------------
# 🔵 TEST: generate_dates
# --------------------------------------------------

def test_generate_dates_range():
    config = {
        "data_inicial": date(2025, 1, 1),
        "data_final": date(2025, 1, 3)
    }

    datas = _generate_dates(config, [])

    assert len(datas) == 3
    assert datas[0] == date(2025, 1, 1)
    assert datas[-1] == date(2025, 1, 3)


# --------------------------------------------------
# 🔵 TEST: generate_schedule
# --------------------------------------------------

def test_generate_schedule_basic():
    config = {
        "horario_inicial": time(10, 0),
        "horario_final": time(14, 0),
        "intervalo": time(0, 30),
        "duracao": time(1, 0)  # 1h
    }

    horarios = _generate_schedule(config)

    assert len(horarios) > 0
    assert horarios[0] == time(10, 0)


def test_generate_schedule_respects_limit():
    config = {
        "horario_inicial": time(10, 0),
        "horario_final": time(11, 0),
        "intervalo": time(0, 0),
        "duracao": time(1, 0)
    }

    horarios = _generate_schedule(config)

    # só cabe uma sessão
    assert len(horarios) == 1


# --------------------------------------------------
# 🔵 TEST: create_section
# --------------------------------------------------

def test_create_section_basic():
    filme = fm.Movie(
        id=1,
        titulo="Teste",
        duracao=120,
        dias_disponiveis_bool={}
    )

    salas = [DummySala(1), DummySala(2)]

    config = {
        "data_inicial": date(2025, 1, 1),
        "data_final": date(2025, 1, 1),
        "horario_inicial": time(10, 0),
        "horario_final": time(12, 0),
        "intervalo": time(0, 0),
        "duracao": time(1, 0)
    }

    sessoes = create_section(filme, salas, config)

    assert len(sessoes) > 0


def test_create_section_invalid_movie():
    salas = [DummySala(1)]

    config = {
        "data_inicial": date(2025, 1, 1),
        "data_final": date(2025, 1, 1),
        "horario_inicial": time(10, 0),
        "horario_final": time(12, 0),
        "intervalo": time(0, 0),
        "duracao": time(1, 0)
    }

    with pytest.raises(TypeError):
        create_section("filme_errado", salas, config) # type: ignore