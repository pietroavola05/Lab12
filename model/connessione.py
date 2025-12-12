import datetime
from dataclasses import dataclass
from model.rifugio import Rifugio


@dataclass
class Connessione:
    id_connessione :int
    id_rifugio1: Rifugio
    id_rifugio2: Rifugio
    distanza: float
    fattore_difficolta: float
    durata: datetime.time #l'ora; .datetime ci da l'ora e la data; .date solo la data
    anno: int

    def __hash__(self):
        return hash(self.id_connessione)

    def __eq__(self, other):
        return self.id_connessione == other.id_connessione

    def __str__(self):
        return f"Connessione tra {self.id_rifugio1} e {self.id_rifugio2}"

    def calcola_peso(self):
        peso = float(self.distanza) * float(self.fattore_difficolta)
        return peso

