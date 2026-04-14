# ⋯⋯⋯⋯ Explicacao ⋯⋯⋯⋯
#     Modulo responsavel por salvar e carregar os arquivos JSON com informacoes dos filmes e sessoes.


# ⋯⋯⋯⋯ To Do ⋯⋯⋯⋯
#     Salvar Filmes e Sessao em arquivos JSON [X]
#     Carregar arquivos JSON [X]


import os
import json
from datetime import datetime, date, time
from cinema.models import filme as fm, sessao, sala

# Caminho base do diretorio atual (para construir caminhos relativos)
pasta_atual = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# ================================================================
#                         SALVAR FILMES
# ================================================================

def serializar_filme(filme):
    filme_serializado = filme.copy()

    for chave, valor in filme_serializado.items():
        if isinstance(valor, date):
            filme_serializado[chave] = valor.strftime("%Y-%m-%d")
        elif isinstance(valor, time):
            filme_serializado[chave] = valor.strftime("%H:%M:%S")

    return filme_serializado

def save_movie_list(lista):
    caminho_arquivo = os.path.join(pasta_atual, 'data', 'filmes.json')

    os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)
    lista = lista or []

    lista_serializada = [serializar_filme(filme) for filme in lista]

    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        json.dump(lista_serializada, f, indent=4, ensure_ascii=False)

def save_movies(filme_modificado):
    """
    Atualiza um filme existente no arquivo JSON.

    Args:
        filme_modificado (models.Filme): objeto Filme atualizado.
    """

    caminho_arquivo = os.path.join(pasta_atual, 'data', 'filmes.json')

    os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)
    filmes = load_movies() or []

    # Substitui filme com mesmo ID
    for i, f in enumerate(filmes):
        if f['filme_id'] == filme_modificado.filme_id:
            filmes[i] = filme_modificado
            break
    
    # Converte objetos Filme e tipos de data/hora para formatos serializaveis
    for i, filme in enumerate(filmes):
        if isinstance(filme, fm.Movie):
            filmes[i] = filme.to_dict()
        else:
            for chave, valores in filmes[i].items():
                if isinstance(valores, date):
                    filmes[i][chave] = valores.strftime("%Y-%m-%d")
                elif isinstance(valores, time):
                    filmes[i][chave] = valores.strftime("%H:%M:%S")

    with open(caminho_arquivo, "w", encoding='utf-8') as f:
        json.dump(filmes, f, indent=4, ensure_ascii=False)


# ================================================================
#                         SALVAR NOVO FILME
# ================================================================
def save_new_movies(filme):
    """
    Adiciona um novo filme ao arquivo JSON.
    Cria o arquivo se ele ainda não existir.
    """
    caminho_arquivo = os.path.join(pasta_atual, 'data', 'filmes.json')
    
    os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)

    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            dados_filme = json.load(f)
    else:
        dados_filme = []

    novo_filme = filme.to_dict()
        
    dados_filme.append(novo_filme)

    with open(caminho_arquivo, "w", encoding='utf-8') as f:
        json.dump(dados_filme, f, indent=4, ensure_ascii=False)



# ================================================================
#                         CARREGAR FILMES
# ================================================================
def load_movies():
    """
    Carrega todos os filmes do arquivo JSON,

    Returns:
        list[dict] | None: Lista de dicionarios com os filmes ou None se nao houver dados.
    """
    caminho_arquivo = os.path.join(pasta_atual, 'data', 'filmes.json')
    if not os.path.exists(caminho_arquivo):
        print('Nenhum filme encontrado.')
        return None

    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        dados = json.load(f)

    if isinstance(dados, dict):
        dados = [dados]
    
    for filme in dados:
        filme['duracao'] = datetime.strptime(filme['duracao'], "%H:%M:%S").time()

    return dados



# ================================================================
#                         SALVAR SESSAO
# ================================================================
def save_section(sessao: sessao.Section):
    """
    Salva os dados de uma sessao (assentos, filme, ID) em um arquivo JSON separado.

    Args:
        sessao (models.Section): objeto contendo os dados da sessao
    """
    caminho_arquivo = os.path.join(pasta_atual, f'data/{sessao.titulo}.json')

    os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)
    
    # Converte assentos para formato numerico (0 = disponivel, 1 = ocupado)
    assentos = {
        linha: [1 if cadeira else 0 for cadeira in colunas]
        for linha, colunas in sessao.assentos.items()
    }

    dados_sessao = {
        "sessao_id": sessao.sessao_id,
        "sala_id": sessao.sala_id,
        "filme": sessao.titulo,
        "data_hora": sessao.data_hora.strftime("%Y-%m-%d_%H:%M"),
        "assentos": assentos
    }
    
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            conteudo = json.load(f)
    else:
        conteudo = {'sessoes': {}}

    conteudo['sessoes'][str(sessao.sessao_id)] = dados_sessao

    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        json.dump(conteudo, f, indent=4, ensure_ascii=False)


# ================================================================
#                          CARREGAR SESSAO
# ================================================================
def load_section(filme, sessao_id):
    """
    Carrega os dados de uma sessao especifica de um filme.

    Args:
        filme_titulo (str): Titulo do filme (nome do arquivo JSON).
        sessao_id (int): ID da sessao.

    Returns:
        models.Section | None: objeto Section ou None se nao existir.
    """
    caminho_arquivo = os.path.join(pasta_atual, f'data/{filme}.json')
    if not os.path.exists(caminho_arquivo):
        print('Nenhum filme encontrado.')
        return None

    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        conteudo = json.load(f)

    if str(sessao_id) not in conteudo['sessoes']:
        return None
    
    dados = conteudo['sessoes'][str(sessao_id)]
    section = sessao.Section(dados['filme'], dados['sala_id'], dados['sessao_id'])

    section.assentos = {
        linha: ['[O]' if cadeira == 0 else '[X]' for cadeira in colunas]
        for linha, colunas in dados["assentos"].items()
    }

    return section


# ================================================================
#                        CARREGAR SESSOES
# ================================================================

def load_sections(filme):
    caminho_arquivo = os.path.join(pasta_atual, f'data/{filme}.json')
    if not os.path.exists(caminho_arquivo):
        print('Nenhum filme encontrado.')
        return None
    
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        conteudo = json.load(f)

    return conteudo


# ================================================================
#                         SALVAR SALA
# ================================================================
def save_room(sala: sala.Room):
    caminho_arquivo = os.path.join(pasta_atual, f'data/salas.json')

    os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)

    salas = load_rooms()
    salas.append(sala.to_dict())

    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        json.dump(salas, f, indent=4, ensure_ascii=False)


# ================================================================
#                         SALVAR SALAS
# ================================================================
def save_rooms(salas):
    caminho_arquivo = os.path.join(pasta_atual, f'data/salas.json')

    os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)

    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        json.dump(salas, f, indent=4, ensure_ascii=False)


# ================================================================
#                        CARREGAR SALAS
# ================================================================
def load_rooms():
    caminho_arquivo = os.path.join(pasta_atual, f'data/salas.json')

    if not os.path.exists(caminho_arquivo):
        return []
    
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []