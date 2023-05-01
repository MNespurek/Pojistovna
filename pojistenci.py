from osoba import Osoba
class Pojistenci():
    
  
   
    seznam_pojistencu = []


  
    def pridej_pojistnika(self, jmeno, prijmeni, telefonni_cislo, vek):
        osoba = Osoba(jmeno, prijmeni, telefonni_cislo, vek)
        return self.seznam_pojistencu.append(osoba)
    
    def vypis_pojistnika(self):
        vypis_pojistencu = ""
        for osoba in self.seznam_pojistencu:
            vypis_pojistencu = vypis_pojistencu + "\n" + osoba.vypis_osobu()
        return vypis_pojistencu

    def hledej_pojistnika(self, jmeno, prijmeni):
        for osoba in self.seznam_pojistencu:
            if osoba.jmeno == jmeno and osoba.prijmeni == prijmeni:
                return osoba.vypis_osobu()
        else:
            return "Zadaná osoba nebyla nalezena"        
            
        
            
    def vymaz_pojistnika(self, jmeno, prijmeni):
        for osoba in self.seznam_pojistencu:
            if osoba.jmeno == jmeno and osoba.prijmeni == prijmeni:
                self.seznam_pojistencu.remove(osoba)
                return "Osoba byla vymazána ze seznamu"
        else:
            return "Zadaná osoba nebyla nalezena"
            
      
    def edituj_pojistnika(self, jmeno, prijmeni):
        for osoba in self.seznam_pojistencu:
            if osoba.jmeno == jmeno and osoba.prijmeni == prijmeni:
                osoba.jmeno = input("Zadejte nové jméno pojištěného\n")
                osoba.prijmeni = input("Zadejte nové příjmení pojištěného\n")
                return f"osoba s ID: {osoba.id} byla editována"
        else:
            return "Zadaná osoba nebyla nalezena"        
        

            
