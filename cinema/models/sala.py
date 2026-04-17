# ================================================================
#                             SALA
# ================================================================

class Room:
    def __init__(self, numero, linhas = 5, colunas = 5, sala_id = None):
        self.id = sala_id
        self.numero = numero
        self.linhas = linhas
        self.colunas = colunas
        self.capacidade = self.capacity()


    @classmethod
    def from_dict(cls, data):
        return cls(
            numero=data['numero'],
            linhas=data['linhas'],
            colunas=data['colunas'],
            sala_id=data['id']
        )
    
# ----------------------------------------------------------------
#                   Converter para Dicionario
# ----------------------------------------------------------------
    def to_dict(self):
        """
        Converte um objeto Movie para dicionario

        Args:
            Objeto Movie
        
        Return:
            Dicionario
        """
        return {
            'sala_id': self.id,
            'numero': self.numero,
            'linhas': self.linhas,
            'colunas': self.colunas
            }

    
    def capacity(self):
        return self.linhas * self.colunas
    
    def create_map_seat(self):
        assentos = {}

        for i in range(self.linhas):
            letra = chr(65 + i)  # A, B, C...

            assentos[letra] = [False] * self.colunas
        print(assentos)
        return assentos
    
    def show_seats(self, assentos):
        print("\nMAPA DE ASSENTOS")

        print("   " + " ".join(str(i) for i in range(1, self.colunas + 1)))

        for i in range(self.linhas):
            letra = chr(65 + i)
            linha = []

            for j in range(1, self.colunas + 1):
                codigo = f"{letra}{j}"
                status = '[X]' if assentos.get(codigo) else '[O]'
                linha.append(status)

            print(f"{letra} " + " ".join(linha))

    def seat_exists(self, codigo):
        if len(codigo) < 2:
            return False

        letra = codigo[0]
        try:
            numero = int(codigo[1:])
        except:
            return False

        if letra < 'A' or letra >= chr(65 + self.linhas):
            return False

        if numero < 1 or numero > self.colunas:
            return False

        return True
