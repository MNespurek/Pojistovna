from osoba import Osoba

class Pojistenci():
  
    seznam_pojistencu = []
    

    def pridej_pojistnika(self, jmeno, prijmeni, telefonni_cislo, vek):
        osoba = Osoba(jmeno, prijmeni, telefonni_cislo, vek)
        return self.seznam_pojistencu.append(osoba)

    def pridej_pojisteni_pojistnika(self, zadane_id, nazev, castka, predmet, platnost_od, platnost_do):
        for osoba in self.seznam_pojistencu:
            if osoba.id == int(zadane_id):
                return osoba.pridej_pojisteni(nazev, castka, predmet, platnost_od, platnost_do)
        else:
            print("Zadané ID nebylo nalezeno")    

    def vypis_pojisteni_pojistnika(self, zadane_id):
        for osoba in self.seznam_pojistencu:
            if osoba.id == int(zadane_id):
                return osoba.vypis_pojisteni()
        else:
            print("Zadané ID nebylo nalezeno")    

    def vypis_pojistnika(self):
        vypis_pojistencu = ""
        for osoba in self.seznam_pojistencu:
            vypis_pojistencu = vypis_pojistencu + "\n" + osoba.vypis_osobu()
        return vypis_pojistencu

    def hledej_pojistnika(self, jmeno, prijmeni):
        hledany_pojistenec = ""
        for osoba in self.seznam_pojistencu:
            if osoba.jmeno == jmeno and osoba.prijmeni == prijmeni:
                hledany_pojistenec = hledany_pojistenec + "\n" + osoba.vypis_osobu()
        return hledany_pojistenec
            
    def vymaz_pojistnika(self, vymaz_id):
        for osoba in self.seznam_pojistencu:
            if osoba.id == vymaz_id:
                self.seznam_pojistencu.remove(osoba)
                return "Osoba s ID {0} {1} {2} byla vymazána ze seznamu".format(osoba.id, osoba.jmeno, osoba.prijmeni)
        else:
            return "Zadaná osoba nebyla nalezena"
            

    def edituj_pojistnika(self, editace_id):
        for osoba in self.seznam_pojistencu:
            if osoba.id == editace_id:
                osoba.jmeno = input("Zadejte nové jméno pojištěného\n")
                osoba.prijmeni = input("Zadejte nové příjmení pojištěného\n")
                return "Jméno a příjmení osoby bylo úspěšně aktualizováno"
        else:
            return "Zadané ID nebylo nalezeno"
