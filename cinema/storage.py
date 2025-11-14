# ⋯⋯⋯⋯ Explicacao ⋯⋯⋯⋯
#     Modulo responsavel por salvar e carregar os arquivos JSON com informacoes dos filmes e sessoes.


# ⋯⋯⋯⋯ To Do ⋯⋯⋯⋯
#     Salvar Filmes e Sessao em arquivos JSON [X]
#     Carregar arquivos JSON [X]


import os
import json
from datetime import datetime, date, time
import models

# Caminho base do diretorio atual (para construir caminhos relativos)
pasta_atual = os.path.dirname(os.path.abspath(__file__))

# ================================================================
#                         SALVAR FILMES
# ================================================================
def save_movies(filme_modificado):
    """
    Atualiza um filme existente no arquivo JSON.

    Args:
        filme_modificado (models.Filme): objeto Filme atualizado.
    """

    caminho_arquivo = os.path.join(pasta_atual, '../data', 'filmes.json')

    os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)
    filmes = load_movies() or []

    # Substitui filme com mesmo ID
    for i, f in enumerate(filmes):
        if f['filme_id'] == filme_modificado.filme_id:
            filmes[i] = filme_modificado
            break
    
    # Converte objetos Filme e tipos de data/hora para formatos serializaveis
    for i, filme in enumerate(filmes):
        if isinstance(filme, models.Movie):
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
    caminho_arquivo = os.path.join(pasta_atual, '../data', 'filmes.json')
    
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
#                         SALVAR SESSAO
# ================================================================
def save_section(sessao):
    """
    Salva os dados de uma sessao (assentos, filme, ID) em um arquivo JSON separado.

    Args:
        sessao (models.Section): objeto contendo os dados da sessao
    """
    caminho_arquivo = os.path.join(pasta_atual, f'../data/{sessao.titulo}.json')

    os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)
    
    # Converte assentos para formato numerico (0 = disponivel, 1 = ocupado)
    assentos = {
        linha: [0 if a == '[O]' else 1 for a in sessao.assentos]
        for linha, colunas in sessao.assentos.items()
    }

    dados_sessao = {
        "filme": sessao.titulo,
        "sessao_id": sessao.sessao_id,
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
#                         CARREGAR FILMES
# ================================================================
def load_movies():
    """
    Carrega todos os filmes do arquivo JSON,

    Returns:
        list[dict] | None: Lista de dicionarios com os filmes ou None se nao houver dados.
    """
    caminho_arquivo = os.path.join(pasta_atual, '..', 'data', 'filmes.json')
    if not os.path.exists(caminho_arquivo):
        print('Nenhum filme encontrado.')
        return None

    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        dados = json.load(f)

    if isinstance(dados, dict):
        dados = [dados]
    
    for filme in dados:
        filme['duracao'] = datetime.strptime(filme['duracao'], "%H:%M:%S").time()
        filme['intervalo'] = datetime.strptime(filme['intervalo'], "%H:%M:%S").time()
        filme['data_inicial'] = datetime.strptime(filme['data_inicial'], "%Y-%m-%d").date()
        filme['data_final'] = datetime.strptime(filme['data_final'], "%Y-%m-%d").date()
        filme['horario_inicial'] = datetime.strptime(filme['horario_inicial'], "%H:%M:%S").time()
        filme['horario_final'] = datetime.strptime(filme['horario_final'], "%H:%M:%S").time()

    return dados


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
    caminho_arquivo = os.path.join(pasta_atual, f'../data/{filme}.json')
    if not os.path.exists(caminho_arquivo):
        print('Nenhum filme encontrado.')
        return None

    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        conteudo = json.load(f)

    if str(sessao_id) not in conteudo['sessoes']:
        return None
    
    dados = conteudo['sessoes'][str(sessao_id)]
    section = models.Section(dados['filme'], dados['sessao_id'])

    section.assentos = {
        linha: ['[O]' if cadeira == 0 else 1 for cadeira in colunas]
        for linha, colunas in dados["assentos"].items()
    }

    return section