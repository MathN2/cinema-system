from cinema.data.storage import load_movies, load_sections, load_rooms, save_rooms

def delete_room(sala_id):
    if room_in_use(sala_id):
        return "used"
    
    salas = load_rooms()

    novas_salas = [s for s in salas if s['sala_id'] != sala_id]

    if len(novas_salas) == len(salas):
        return "notfound"

    save_rooms(novas_salas)
    return "ok"
    


def room_in_use(sala_id):
    filmes = load_movies()

    if filmes is None:
        return False
    
    for filme in filmes:
        sessoes = load_sections(filme.get('titulo'))

        if not sessoes:
            continue
        
        for sessao in sessoes['sessoes'].values():
            if sessao.get('sala_id') == sala_id:
                return True
    
    return False