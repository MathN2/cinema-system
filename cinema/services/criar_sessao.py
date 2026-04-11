from cinema.models.sessao import Section
import cinema.models.filme as fm

def create_section(filme: fm.Movie):
    if not isinstance(filme, fm.Movie):
        raise TypeError("filme deve ser um objeto Movie")
    
    sessoes = []

    for exibicao in filme.exibicao_ids:
        sessao = Section(filme.titulo, exibicao)
        sessoes.append(sessao)

    return sessoes