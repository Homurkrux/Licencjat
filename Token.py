from dataclasses import dataclass


#klasa tokenu słowa z wartościami z bazy NAWL_BE
@dataclass
class Token:
    token: str
    happ: float
    ang: float
    sad: float
    fear: float
    disg: float
    val: float
    arou: float
    #konstruktor klasy
    def __init__(self,token: str, happ: float, ang: float, sad: float, fear: float, disg: float, val: float, arou: float):
        self.token = token
        self.happ = happ
        self.ang = ang
        self.sad = sad
        self.fear = fear
        self.disg = disg
        self.val = val
        self.arou = arou
    #metoda parsująca obiekt klasy na słownik
    def as_dict(self):
        return {'token': self.token,
               'happ': self.happ,
               'ang': self.ang,
               'sad': self.sad,
               'fear': self.fear,
               'disg': self.disg,
               'val' : self.val,
               'arou': self.arou}
    
