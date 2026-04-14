"""
Apaga um filme cadastrado no arquivo JSON.
"""
import cinema.data.storage as storage
import cinema.services.criar_filme as criar_filme
lista_filmes = storage.load_movies()

def delete_movie(nome_filme):
    if lista_filmes is None:
        return None

    for index, key in enumerate(lista_filmes):
        if key["titulo"].lower() == nome_filme.lower():
            print(key['titulo'], nome_filme)
            del lista_filmes[index]
            break
    return lista_filmes