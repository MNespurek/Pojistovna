class Pojisteni:
    dalsi_id = 1
    
    def __init__(self, nazev, castka, predmet, platnost_od, platnost_do):
        self.nazev = nazev
        self.castka = castka
        self.predmet = predmet
        self.platnost_od = platnost_od
        self.platnost_do = platnost_do
        self.id = Pojisteni.dalsi_id
        Pojisteni.dalsi_id += 1

    def __str__(self):
        return "{0}\t{1}\t{2}\t{3}\t{4}\t{5}".format(self.id, self.nazev, self.castka, self.predmet, self.platnost_od, self.platnost_do)


    def vrat_nazev_pojisteni(self):
        return "ID:{0} nazev:{1} částka:{2} predmet:{3} platnost od: {4} platnost do: {5}".format(self.id, self.nazev, self.castka, self.predmet, self.platnost_od, self.platnost_do)