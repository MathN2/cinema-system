import pytest
from datetime import date

'''
🧪 📁 tests/test_filme_services.py
'''

from cinema.services.filme_services import (
    create_movie,
    is_movie_active,
    update_movie
)

import cinema.models.filme as fm
'''
🔵 TEST: create_movie
'''
def test_create_movie_basic():
    dados = {
        "titulo": "Filme Teste",
        "duracao": 120,
        "dias_disponiveis": {
            "segunda": True
        }
    }

    filme = create_movie(dados)

    assert isinstance(filme, fm.Movie)
    assert filme.titulo == "Filme Teste"


'''
🔵 TEST: is_movie_active (sem sessão)
'''
def test_is_movie_active_no_sessions(monkeypatch):

    class FakeCursor:
        def execute(self, *args):
            pass

        def fetchone(self):
            return None

    class FakeConn:
        def cursor(self):
            return FakeCursor()

        def close(self):
            pass

    def fake_get_connection():
        return FakeConn()

    monkeypatch.setattr(
        "cinema.services.filme_services.get_connection",
        fake_get_connection
    )

    assert is_movie_active(1) is False

'''
🔵 TEST: is_movie_active (filme ativo)
'''
def test_is_movie_active_true(monkeypatch):

    hoje = date.today()

    class FakeCursor:
        def execute(self, *args):
            pass

        def fetchone(self):
            return (hoje, hoje)

    class FakeConn:
        def cursor(self):
            return FakeCursor()

        def close(self):
            pass

    def fake_get_connection():
        return FakeConn()

    monkeypatch.setattr(
        "cinema.services.filme_services.get_connection",
        fake_get_connection
    )

    assert is_movie_active(1) is True


'''
🔵 TEST: is_movie_active (fora do período)
'''
def test_is_movie_active_false_outside_range(monkeypatch):

    class FakeCursor:
        def execute(self, *args):
            pass

        def fetchone(self):
            return (date(2000, 1, 1), date(2000, 1, 2))

    class FakeConn:
        def cursor(self):
            return FakeCursor()

        def close(self):
            pass

    def fake_get_connection():
        return FakeConn()

    monkeypatch.setattr(
        "cinema.services.filme_services.get_connection",
        fake_get_connection
    )

    assert is_movie_active(1) is False


'''
🔵 TEST: update_movie
'''
def test_update_movie_executes_query(monkeypatch):

    executed = {}

    class FakeCursor:
        def execute(self, query, values):
            executed["query"] = query
            executed["values"] = values

    class FakeConn:
        def cursor(self):
            return FakeCursor()

        def commit(self):
            executed["committed"] = True

        def close(self):
            pass

    def fake_get_connection():
        return FakeConn()

    monkeypatch.setattr(
        "cinema.services.filme_services.get_connection",
        fake_get_connection
    )

    filme = {"id": 1}

    update_movie(filme, "titulo", "Novo")

    assert executed["values"] == ("Novo", 1)
    assert executed["committed"] is True
