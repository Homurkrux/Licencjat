from dataclasses import dataclass



@dataclass
class Token:
    token: str
    happ: float
    ang: float
    sad: float
    fear: float
    disg: float

    def __init__(self,token: str, happ: float, ang: float, sad: float, fear: float, disg: float):
        self.token = token
        self.happ = happ
        self.ang = ang
        self.sad = sad
        self.fear = fear
        self.disg = disg

    def as_dict(self):
        return {'token': self.token,
               'happ': self.happ,
               'ang': self.ang,
               'sad': self.sad,
               'fear': self.fear,
               'disg': self.disg}
    
