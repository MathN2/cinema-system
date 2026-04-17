from cinema.services.sala_services import room_in_use_logic

def test_room_in_use_true():
    filmes = [{"id": 1}]
    secoes = {1: [{"sala_id": 1}]}

    assert room_in_use_logic(1, filmes, secoes) is True


def test_room_in_use_false():
    filmes = [{"id": 1}]
    secoes = {1: [{"sala_id": 2}]}

    assert room_in_use_logic(1, filmes, secoes) is False