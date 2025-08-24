#  Criar a estrutura de filmes disponíveis [X]
#  Criar sessões por filme (com horários e dias, se decidir incluir) [X]
#  Criar mapa de assentos (ocupados e disponíveis) [X]
#  Implementar a escolha de assento pelo usuário [X]
#  Definir valores de ingresso (inteira e meia) []
#  Calcular valor total da compra []
#  Permitir reserva de assentos [X]
#  Exibir resumo da compra (assento, filme, horário, valor) []
#  Login de ADM e login de cliente []
#  Salvar Filmes e Sessao em arquivos JSON [X]
#  Carregar arquivos JSON []
#  Interface de texto (inicial) []
#  (Futuramente) Adicionar interface gráfica []

#Imports↴
import os
import json

class Sessao:
    def __init__(self, filme):
        self.titulo = filme
        self.id = 2
        self.assentos = {
            'A': ['[O]'] * 5,
            'B': ['[O]'] * 5,
            'C': ['[O]'] * 5,
            'D': ['[O]'] * 5,
            'E': ['[O]'] * 5,
        }

    def exibir_assentos(self):
        print('   1  2  3  4  5')
        for index, linha in enumerate(self.assentos):
            print(f'{linha} {"".join(self.assentos[linha])}')

    def reservar_assento(self):
        while True:
            try:
                total_assentos = sum(linha.count('[O]') for linha in self.assentos.values())
                num_reservas = int(input('Digite quantos assentos deseja reservar: '))

                if not (1 <= num_reservas <= total_assentos):
                    print(f'Valor invalido. Tente um numero de 1 - {total_assentos}')
                    continue
                break
                    
            except ValueError:
                print(f'Valor invalido. Use um numero inteiro de 1 - {total_assentos}')
        n = 0

        while n < num_reservas:
            # Cordenadas do assento, sendo (x) a fileira[A B C D E] e (y) a coluna
            cordenadas = input('Digite o assento que deseja reservar: ').upper().replace(" ", "")
            if len(cordenadas) < 2:
                print('Valor Invalido. Use o formato A1, B2, C3, etc.')
                continue
            x = cordenadas[0]
            y = cordenadas[1:]

            if not y.isdigit():
                print('Valor Invalido.')
                continue
            y = int(y) - 1 # Deve ser -1 para dar match com o index do dicionario
            
            if x not in self.assentos or not 0 <= y < len(self.assentos[x]):
                print('Esse assento nao existe.')
                continue
            
            if self.assentos[x][y] == '[X]':
                print('Esse assento nao esta disponivel.')
                
                while True:
                    decision = input('Deseja continuar? (S/N): ').upper()
                    if decision == 'S':
                        break
                    elif decision == 'N':
                        return
                    else:
                        print('Valor Invalido.')

            self.assentos[x][y] = '[X]'
            
            n += 1

# sessao1 = Sessao('Harry potter')
# sessao1.exibir_assentos()
# sessao1.reservar_assento()
# sessao1.exibir_assentos()

class Filme: #ADM
    def __init__(self, titulo, duracao, sala, intervalo, dias_disponiveis, horario_inicial="13:00", horario_final="22:00"):
        self.titulo = titulo
        self.duracao = self.converter_horarios(duracao) # EM MINUTOS
        self.sala = sala
        self.intervalo = self.converter_horarios(intervalo) #EM MINUTOS
        self.dias_disponiveis = dias_disponiveis # SEMANA
        self.horario_inicial = horario_inicial
        self.horario_final = horario_final
        self.horarios_disponiveis = self.Horarios_Disponiveis()

    def converter_horarios(self, tempo):
        tempo = tempo.lower().replace(" ", "").replace("min", "").replace("m", "")

        if ':' in tempo:
            partes = tempo.split(":")
            horas = int(partes[0])
            minutos = int(partes[1])
            return horas * 60 + minutos
        
        if 'h' in tempo:
            partes = tempo.split("h")
            horas = int(partes[0]) if partes[0] else 0
            minutos = int(partes[1]) if len(partes) > 1 and partes[1] else 0
            return horas * 60 + minutos
        
        return int(tempo)

    def Horarios_Disponiveis(self):
        from datetime import datetime, timedelta

        atual = datetime.strptime(self.horario_inicial, "%H:%M")
        limite = datetime.strptime(self.horario_final, "%H:%M")
        horarios_disponiveis = []

        while atual + timedelta(minutes=self.duracao) <= limite:
            horarios_disponiveis.append(atual.strftime("%H:%M"))
            atual = atual + timedelta(minutes=self.duracao) + timedelta(minutes=self.intervalo)

        return horarios_disponiveis
        
# filme1 = Filme("Putz, a coisa ta feia", "1:30", 1, "15", 5)
# print(filme1.horarios_disponiveis)

def save_sessao(sessao):
    os.makedirs('dados', exist_ok=True)
    
    arquivo = f'dados/{sessao.titulo}.json'
    assentos = {
        linha: [0 if a == '[O]' else 1 for a in sessao.assentos]
        for linha, colunas in sessao.assentos.items()
    }

    dados = {
        "filme": sessao.titulo,
        "sessao_id": sessao.id,
        "assentos": assentos
    }
    
    if os.path.exists(arquivo):
        with open(arquivo, 'r', encoding='utf-8') as f:
            conteudo = json.load(f)
    else:
        conteudo = {'sessoes': {}}

    conteudo['sessoes'][str(sessao.id)] = dados

    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(conteudo, f, indent=4, ensure_ascii=False)


def load_sessao(filme, sessao_id):
    arquivo = f'data/{filme}.json'
    if not os.path.exists(arquivo):
        return None

    with open(arquivo, 'r', encoding='utf-8') as f:
        conteudo = json.load(f)

    if str(sessao_id) not in conteudo['sessoes']:
        return None
    
    dados = conteudo['sessoes'][str(sessao_id)]
    sessao = Sessao(dados['filme'])
    sessao.id = dados["sessao_id"]

    sessao.assentos = {
        linha: ['[O]' if cadeira == 0 else 1 for cadeira in colunas]
        for linha, colunas in dados["assentos"].items()
    }

    return sessao


def Menu():
    print('*' * 50)
    print('BEM-VINDO'.center(50, ' '))
    print('*' * 50)

    print('')

Menu()