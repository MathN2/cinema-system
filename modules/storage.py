# SALVAR E CARREGAR OS ARQUIVOS JSON COM INFORMAÇÕES DOS FILMES E SESSÕES

#  Salvar Filmes e Sessao em arquivos JSON [X]
#  Carregar arquivos JSON []
import os
import json
from models import Section

pasta_atual = os.path.dirname(os.path.abspath(__file__))

def save_movies(filme):
    arquivo = os.path.join(pasta_atual, '../data', 'filmes.json')
    os.makedirs(os.path.dirname(arquivo), exist_ok=True)

    dados = filme

    with open(arquivo, "w", encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def save_new_movies(filme):
    arquivo = os.path.join(pasta_atual, '../data', 'filmes.json')
    os.makedirs(os.path.dirname(arquivo), exist_ok=True)

    if os.path.exists(arquivo):
        with open(arquivo, 'r', encoding='utf-8') as f:
            dados = json.load(f)
    else:
        dados = []

    novo_filme = {'titulo': filme.titulo,
            'duracao': filme.duracao,
            'sala': filme.sala,
            'intervalo': filme.intervalo,
            'dias_disponiveis': filme.dias_disponiveis,
            'horario_inicial': filme.horario_inicial,
            'horario_final': filme.horario_final,}
        
    dados.append(novo_filme)

    with open(arquivo, "w", encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


def save_section(section):
    arquivo = os.path.join(pasta_atual, f'../dados/{section.titulo}.json')
    os.makedirs(os.path.dirname(arquivo), exist_ok=True)
    
    assentos = {
        linha: [0 if a == '[O]' else 1 for a in section.assentos]
        for linha, colunas in section.assentos.items()
    }

    dados = {
        "filme": section.titulo,
        "section_id": section.id,
        "assentos": assentos
    }
    
    if os.path.exists(arquivo):
        with open(arquivo, 'r', encoding='utf-8') as f:
            conteudo = json.load(f)
    else:
        conteudo = {'sessoes': {}}

    conteudo['sessoes'][str(section.id)] = dados

    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(conteudo, f, indent=4, ensure_ascii=False)


def load_movies():
    arquivo = os.path.join(pasta_atual, '..', 'data', 'filmes.json')
    if not os.path.exists(arquivo):
        print('Nenhum filme encontrado.')
        return None

    with open(arquivo, 'r', encoding='utf-8') as f:
        dados = json.load(f)

    return dados


def load_section(filme, section_id):
    arquivo = os.path.join(pasta_atual, f'../data/{filme}.json')
    if not os.path.exists(arquivo):
        print('Nenhum filme encontrado.')
        return None

    with open(arquivo, 'r', encoding='utf-8') as f:
        conteudo = json.load(f)

    if str(section_id) not in conteudo['sessoes']:
        return None
    
    dados = conteudo['sessoes'][str(section_id)]
    section = Section(dados['filme'], dados['section_id'])

    section.assentos = {
        linha: ['[O]' if cadeira == 0 else 1 for cadeira in colunas]
        for linha, colunas in dados["assentos"].items()
    }

    return section