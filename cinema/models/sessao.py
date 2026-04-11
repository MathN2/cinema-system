from datetime import datetime, timedelta, date
# ================================================================
#                           SECTION
# ================================================================
class Section():
    """
    Representa uma sessao de cinema, com seu titulo, ID e mapa de assentos.
    """
    _num_id = 0

    def __init__(self, titulo, data_hora):
        """
        Inicializa uma nova sessao.

        Args:
            filme: Objeto Movie contendo informacoes do filme
            section_id: Identificador Unico da sessao.
        """
        self.sessao_id = self.novo_id()
        self.titulo = titulo
        self.data_hora = data_hora
        self.assentos = {
            'A': ['[O]'] * 5,
            'B': ['[O]'] * 5,
            'C': ['[O]'] * 5,
            'D': ['[O]'] * 5,
            'E': ['[O]'] * 5,
        }


    @classmethod
    def novo_id(cls):
        cls._num_id += 1    
        return cls._num_id
# ----------------------------------------------------------------
#                         Exibir Assentos
# ----------------------------------------------------------------
    def show_seats(self):
        """
        Exibe o mapa de assentos da sessao no console.
        """
        print('   1  2  3  4  5')
        for linha, lugares in self.assentos.items():
            print(f'{linha} {"".join(lugares)}')

# ----------------------------------------------------------------
#                         Reservar Assentos
# ----------------------------------------------------------------
    def assign_seat(self):
        """
        Permite ao usuario reservar assentos disponiveis.

        O metodo solicita a quantidade e as posicoes dos assentos.
        Valida as entradas e marca os assentos escolhidos como '[X]'.
        """
        while True:
            total_assentos = sum(linha.count('[O]') for linha in self.assentos.values())
            try:
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