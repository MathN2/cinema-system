# ================================================================
#                       FUNCOES GERAIS
# ================================================================

from datetime import datetime

# ----------------------------------------------------------------
#                    Converter para time()
# ----------------------------------------------------------------
def to_time():
    """
    Solicita uma str do usuario, faz uma validacao para o formato correto e converte para datetime.time

    Return:
        tempo: valor convertido para datetime.time
    """
    while True:
        entrada = input()
        try:
            tempo = datetime.strptime(entrada, "%H:%M").time()
            return tempo
        except ValueError:
            print('Formato inválido. Use o padrão hh:mm.')


# ----------------------------------------------------------------
#                    Converter para date()
# ----------------------------------------------------------------
def to_date():
    """
    Solicita uma str do usuario, faz uma validacao para o formato correto e converte para datetime.date

    Return:
        data: valor convertido para datetime.date
    """
    while True:
        entrada = input()
        try:
            data = datetime.strptime(entrada, "%Y-%m-%d").date()
            return data
        except ValueError:
            print('Formato inválido. Use o padrão yyyy-mm-dd.')


# ----------------------------------------------------------------
#                       Validar Inteiro
# ----------------------------------------------------------------
def validar_int(inicio=None, fim=None, mensagem_entrada="Digite um número: ", mensagem_erro="Valor inválido. Tente um número."):
    """
    Pede e valida um numero inteiro.

    Args:
        inicio: limita o escopo minimo do numero a ser escolhido. (Caso esse parametro n seja recebido entao inicio = None)
        fim: limita o escopo maximo do numero a ser escolhiudo. (Caso esse parametro n seja recebido entao inicio = None)
        mensagem_entrada: Uma forma de personalizar a mensagem de entrada para o usuario.
        mensagem_erro: Uma forma de personalizar a mensagem de erro para o usuario.

    Return:
        entrada: valor, escolhido pelo usuario, após validação (int).
    """
    while True:
        entrada = input(mensagem_entrada)
        try:
            entrada = int(entrada)
            if inicio is None or fim is None:
                return entrada
            elif inicio <= entrada <= fim:
                return entrada
            else:
                print(mensagem_erro)
        except ValueError:
            print(mensagem_erro)