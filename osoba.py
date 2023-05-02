class Osoba:
    dalsi_id = 1
    
    def __init__(self, jmeno, prijmeni, telefonni_cislo, vek):
        self.jmeno = jmeno
        self.prijmeni = prijmeni
        self.telefonni_cislo = telefonni_cislo
        self.vek = vek
        self.id = Osoba.dalsi_id
        Osoba.dalsi_id += 1

    def __str__(self):
        return "{0}\t{1}\t{2}\t{3}\t{4}".format(self.id, self.jmeno, self.prijmeni, self.telefonni_cislo, self.vek)
    
    def vypis_osobu(self):
        return "{0}\t{1}\t{2}\t{3}\t{4}".format(self.id, self.jmeno, self.prijmeni, self.telefonni_cislo, self.vek)
