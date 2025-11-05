# SALVAR E CARREGAR OS ARQUIVOS JSON COM INFORMAÇÕES DOS FILMES E SESSÕES

#  Salvar Filmes e Sessao em arquivos JSON [X]
#  Carregar arquivos JSON []
from datetime import datetime, date, time
import os
import json
import models

pasta_atual = os.path.dirname(os.path.abspath(__file__))

def save_movies(filme_modificado):
    arquivo = os.path.join(pasta_atual, '../data', 'filmes.json')
    os.makedirs(os.path.dirname(arquivo), exist_ok=True)
    filmes = load_movies()

    for i, f in enumerate(filmes):
        if f['id'] == filme_modificado.id:
            print(filme_modificado.__dict__)
            filmes[i] = filme_modificado
            break
    
    for i, dados in enumerate(filmes):
        # print(type(dados))
        if isinstance(dados, models.Filme):
            filmes[i] = dados.to_dict()
        else:
            for chave, valores in filmes[i].items():
                if isinstance(valores, date):
                    filmes[i][chave] = valores.strftime("%Y-%m-%d")
                elif isinstance(valores, time):
                    filmes[i][chave] = valores.strftime("%H:%M:%S")

    with open(arquivo, "w", encoding='utf-8') as f:
        json.dump(filmes, f, indent=4, ensure_ascii=False)

def save_new_movies(filme):
    arquivo = os.path.join(pasta_atual, '../data', 'filmes.json')
    os.makedirs(os.path.dirname(arquivo), exist_ok=True)

    if os.path.exists(arquivo):
        with open(arquivo, 'r', encoding='utf-8') as f:
            dados = json.load(f)
    else:
        dados = []

    novo_filme = filme.to_dict()
        
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

    if isinstance(dados, dict):
        dados = [dados]
    else:
        for dado in dados:
            dado['duracao'] = datetime.strptime(dado['duracao'], "%H:%M:%S").time()
            dado['intervalo'] = datetime.strptime(dado['intervalo'], "%H:%M:%S").time()
            dado['data_inicial'] = datetime.strptime(dado['data_inicial'], "%Y-%m-%d").date()
            dado['data_final'] = datetime.strptime(dado['data_final'], "%Y-%m-%d").date()
            dado['horario_inicial'] = datetime.strptime(dado['horario_inicial'], "%H:%M:%S").time()
            dado['horario_final'] = datetime.strptime(dado['horario_final'], "%H:%M:%S").time()

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
    section = models.Section(dados['filme'], dados['section_id'])

    section.assentos = {
        linha: ['[O]' if cadeira == 0 else 1 for cadeira in colunas]
        for linha, colunas in dados["assentos"].items()
    }

    return section