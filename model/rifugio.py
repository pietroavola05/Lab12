from dataclasses import dataclass

@dataclass
class Rifugio:
    id: int
    nome: str
    localita: str
    altitudine : float
    capienza : int
    aperto: int


    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return f"{self.nome}"



