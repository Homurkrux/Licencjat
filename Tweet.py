from dataclasses import dataclass
from Token import Token
import datetime

#klasa Tweeta po odsianiu niepotrzebnych wartości
@dataclass
class Tweet:
    dataCzas: datetime.datetime
    tekstTweeta: str
    plecAutoraTweeta: str
    debata: str
    slowaEmotywne: int
    tokeny: [Token]
    #konstruktor klasy
    def __init__(self, data: datetime.datetime, tekst: str, plecAutoraTweeta: str, debata: str):
        self.dataCzas = data
        self.tekstTweeta = tekst
        self.plecAutoraTweeta = plecAutoraTweeta
        self.debata = debata
        self.tokeny = []
    #metoda parsująca obiekt klasy na słownik
    def as_dict(self):
        return {'dataCzas': self.dataCzas,
               'tekstTweeta': self.tekstTweeta,
               'plecAutoraTweeta': self.plecAutoraTweeta,
               'debata': self.debata,
               'tokeny': [x.as_dict() for x in self.tokeny]}
