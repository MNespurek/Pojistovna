
class Osoba:

    def __init__(self, jmeno, prijmeni, ulice, email, telefon, mesto, psc):
        self.jmeno = jmeno
        self.prijmeni = prijmeni
        self.ulice = ulice
        self.email = email
        self.telefon = telefon
        self.mesto = mesto
        self.psc = psc

class OsobaId:
    def __init__(self, id_pojistenec, jmeno, prijmeni, ulice, email, telefon, mesto, psc):
        self.id_pojistenec = id_pojistenec
        self.jmeno = jmeno
        self.prijmeni = prijmeni
        self.ulice = ulice
        self.email = email
        self.telefon = telefon
        self.mesto = mesto
        self.psc = psc

class OsobaVypis:
    def __init__(self, id_pojistenec, jmeno, prijmeni, mesto):
        self.id_pojistenec = id_pojistenec
        self.jmeno = jmeno
        self.prijmeni = prijmeni
        self.mesto = mesto