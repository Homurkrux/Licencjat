from dataclasses import dataclass

#klasa s�owa NAWL
@dataclass
class NAWLWord:
    word: str
    happ: float
    ang: float
    sad: float
    fear: float
    disg: float
    val: float
    arou: float
    #konstruktor klasy
    def __init__(self,word: str, happ: float, ang: float, sad: float, fear: float, disg: float, val: float, arou: float):
        self.word = word
        self.happ = happ
        self.ang = ang
        self.sad = sad
        self.fear = fear
        self.disg = disg
        self.val = val
        self.arou = arou
    #metoda parsuj�ca obiekt klasy na s�ownik
    def as_dict(self):
        return {'word': self.word,
               'happ': self.happ,
               'ang': self.ang,
               'sad': self.sad,
               'fear': self.fear,
               'disg': self.disg,
               'val' : self.val,
               'arou': self.arou}