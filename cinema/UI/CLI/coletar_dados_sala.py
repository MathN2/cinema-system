from cinema.services import utils

def get_room_data():
    return {
        'numero': ask_num(),
        'linhas': ask_lines(),
        'colunas': ask_columns()
    }

def ask_num():
    mensagem = "Digite o número da sala: "
    num = utils.validar_int(1, None, mensagem)
    
    return num

def ask_lines():
    mensagem = "Digite a quantidade de fileiras: "
    fileiras = utils.validar_int(1, None, mensagem)

    return fileiras

def ask_columns():
    mensagem = "Digite a quantidade de colunas: "
    colunas = utils.validar_int(1, None, mensagem)

    return colunas