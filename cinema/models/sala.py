# ================================================================
#                             SALA
# ================================================================

class Sala:
    _num_id = 0  # contador da classe

    def __init__(self):
        self.id = self.novo_id()  # pega o valor atual do contador

    @classmethod
    def novo_id(cls):
        cls._num_id += 1    
        return cls._num_id

obj = Sala()
obj2 = Sala()
obj3 = Sala()
obj4 = Sala()
print(obj.id)
print(obj2.id)
print(obj3.id)
print(obj4.id)