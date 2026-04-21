from cinema.models import sala, filme
import json
from rich.table import Table
from rich.console import Console

console = Console()
# ================================================================
#                           SECTION
# ================================================================
class Section():
    """
    Representa uma sessao de cinema, com seu titulo, ID e mapa de assentos.
    """
    _num_id = 0

    def __init__(self, filme: filme.Movie, sala: sala.Room, data_hora, sessao_id = None):
        """
        Inicializa uma nova sessao.

        Args:
            filme: Objeto Movie contendo informacoes do filme
            section_id: Identificador Unico da sessao.
        """
        self.id = sessao_id
        self.filme_id= filme.id
        self.sala_id = sala.id
        self.titulo = filme.titulo
        self.data_hora = data_hora
        self.sala = sala
        self.assentos = sala.create_map_seat()


    @classmethod
    def from_dict(cls, dados):
        obj = cls.__new__(cls)  # cria sem chamar __init__

        obj.filme_id = dados['filme_id']
        obj.sala_id = dados['sala_id']
        obj.id = dados['id']
        obj.data_hora = dados['data_hora']

        dados_assentos = json.loads(dados['assentos'])
        
        obj.assentos = {
            linha: colunas  # já está correto vindo do JSON
            for linha, colunas in dados_assentos.items()
        }

        return obj
    
    @staticmethod
    def _normalizar_cadeira(cadeira):
        if cadeira in (0, "0", "[O]", True):
            return "[O]"
        return "[X]"
# ----------------------------------------------------------------
#                         Exibir Assentos
# ----------------------------------------------------------------
    def show_seats(self, filme):
        """
        Exibe o mapa de assentos da sessão no console.
        """
        console.print("=" * 40)
        console.print(f"[bold]Filme:[/bold] {filme.titulo}")
        console.print(f"[bold]Sessão:[/bold] {self.id}")
        console.print("=" * 40)

        if not self.assentos:
            console.print("[red]Nenhum assento disponível.[/red]")
            return

        table = Table(title="Mapa de Assentos", show_lines=True)

        dados_assentos = self.assentos

        for linha, colunas in dados_assentos.items():
            dados_assentos[linha] = [
                self._normalizar_cadeira(cadeira)
                for cadeira in colunas
                ]
            
        colunas = len(next(iter(dados_assentos.values())))

        print("  " + " ".join(f"{i+1:^3}" for i in range(colunas)))

        for linha, assentos in self.assentos.items():
            print(f"{linha} " + " ".join(f"{x:^3}" for x in assentos))
            
        # console.print(self.assentos)

        console.print("\n[green]O[/green] Disponível | [red]X[/red] Ocupado | [?] Inválido\n")

# ----------------------------------------------------------------
#                         Reservar Assentos
# ----------------------------------------------------------------
    # def assign_seat(self):
    #     """
    #     Permite ao usuario reservar assentos disponiveis.

    #     O metodo solicita a quantidade e as posicoes dos assentos.
    #     Valida as entradas e marca os assentos escolhidos como '[X]'.
    #     """
    #     while True:
    #         total_assentos = sum(linha.count('[O]') for linha in self.assentos.values())
    #         try:
    #             num_reservas = int(input('Digite quantos assentos deseja reservar: '))

    #             if not (1 <= num_reservas <= total_assentos):
    #                 print(f'Valor invalido. Tente um numero de 1 - {total_assentos}')
    #                 continue
    #             break
                    
    #         except ValueError:
    #             print(f'Valor invalido. Use um numero inteiro de 1 - {total_assentos}')
    #     n = 0

    #     while n < num_reservas:
    #         # Cordenadas do assento, sendo (x) a fileira[A B C D E] e (y) a coluna
    #         cordenadas = input("Digite o assento (ex: A1): ").upper().replace(" ", "")
    #         if len(cordenadas) < 2:
    #             print('Valor Invalido. Use o formato A1, B2, C3, etc.')
    #             continue
    #         x = cordenadas[0]
    #         y = cordenadas[1:]

    #         if not y.isdigit():
    #             print('Valor Invalido.')
    #             continue
    #         y = int(y) - 1 # Deve ser -1 para dar match com o index do dicionario
            
    #         if x not in self.assentos or not 0 <= y < len(self.assentos[x]):
    #             print('Esse assento nao existe.')
    #             continue
            
    #         if self.assentos[x][y] == '[X]':
    #             print('Esse assento nao esta disponivel.')
                
    #             while True:
    #                 decision = input('Deseja continuar? (S/N): ').upper()
    #                 if decision == 'S':
    #                     break
    #                 elif decision == 'N':
    #                     return
    #                 else:
    #                     print('Valor Invalido.')

    #         self.assentos[x][y] = '[X]'
    #         print("\nAssento(s) reservado(s) com sucesso!\n")
            
    #         n += 1

    def assign_seat(self, lugar):
        x = lugar[0]
        y = lugar[1:]

        if not y.isdigit():
            return False

        y = int(y) - 1

        # valida existência
        if x not in self.assentos or not 0 <= y < len(self.assentos[x]):
            return False

        # já ocupado
        if self.assentos[x][y] == '[X]':
            return False

        # marca como ocupado
        self.assentos[x][y] = '[X]'
        return True


# ----------------------------------------------------------------
#                Verificar disposição de Assento
# ----------------------------------------------------------------
    def is_available(self, lugar):
        x = lugar[0]
        y = int(lugar[1:]) - 1

        return self.assentos[x][y] == '[O]'