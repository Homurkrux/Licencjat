from dataclasses import dataclass
from Token import Token
import datetime


@dataclass
class Tweet:
    dataCzas: datetime.datetime
    tekstTweeta: str
    plecAutoraTweeta: str
    debata: str
    tokeny: [Token]
    
    def __init__(self, data: datetime.datetime, tekst: str, plecAutoraTweeta: str, debata: str):
        self.dataCzas = data
        self.tekstTweeta = tekst
        self.plecAutoraTweeta = plecAutoraTweeta
        self.debata = debata
        self.tokeny = []

    def as_dict(self):
        return {'dataCzas': self.dataCzas,
               'tekstTweeta': self.tekstTweeta,
               'plecAutoraTweeta': self.plecAutoraTweeta,
               'debata': self.debata,
               'tokeny': [x.as_dict() for x in self.tokeny]}
