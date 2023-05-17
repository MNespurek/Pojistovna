
from pojisteni import Pojisteni
class Osoba:

    
    def __init__(self, jmeno, prijmeni, telefonni_cislo, vek):
        self.jmeno = jmeno
        self.prijmeni = prijmeni
        self.telefonni_cislo = telefonni_cislo
        self.vek = vek
        



    def __str__(self):
        return "{0}\t{1}\t{2}\t{3}\t{4}".format(self.id, self.jmeno, self.prijmeni, self.telefonni_cislo, self.vek)
    
    def vypis_osobu(self):
        return "{0}\t{1}\t{2}\t{3}\t{4}".format(self.id, self.jmeno, self.prijmeni, self.telefonni_cislo, self.vek)
    
    # def pridej_pojisteni(self, nazev, castka, predmet, platnost_od, platnost_do):
        # pojisteni = Pojisteni(nazev, castka, predmet, platnost_od, platnost_do)
        # self.seznam_pojisteni.append(pojisteni)
        
    
    def vypis_pojisteni(self):
        vypsane_pojisteni = ""
        for pojisteni in self.seznam_pojisteni:
            vypsane_pojisteni = vypsane_pojisteni + "\n" + pojisteni.vrat_nazev_pojisteni()
        return "{0}".format(vypsane_pojisteni)

