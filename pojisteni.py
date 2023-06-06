import flask_paginate
print(flask_paginate.__version__)

class Pojisteni:
    
    def __init__(self, id_pojisteni, id_pojistenec, nazev, castka, predmet, platnost_od, platnost_do):
        self.id_pojisteni = id_pojisteni
        self.id_pojistenec = id_pojistenec
        self.nazev = nazev
        self.castka = castka
        self.predmet = predmet
        self.platnost_od = platnost_od
        self.platnost_do = platnost_do
        
class PojisteniId:
    def __init__(self, id_pojisteni, nazev, castka):
        self.id_pojisteni = id_pojisteni
        self.nazev = nazev
        self.castka = castka
