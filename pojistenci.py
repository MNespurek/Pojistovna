
from osoba import Osoba
from databaze import Databaze
from pojisteni import Pojisteni

class Pojistenci():



    # seznam_pojistencu = []
    


    def vytvor_uloz_pojistnika(self, jmeno, prijmeni, telefonni_cislo, vek, databaze_pojistovna):        
        osoba = Osoba(jmeno, prijmeni, telefonni_cislo, vek)
        uloz = f"INSERT INTO pojistenci (jmeno, prijmeni, telefonni_cislo, vek) VALUES (?, ?, ?, ?);"
        data = (osoba.jmeno, osoba.prijmeni, osoba.telefonni_cislo, osoba.vek)
        databaze_pojistovna.cursor.execute(uloz, data)
        databaze_pojistovna.conn.commit()
        

    def vypis_vsech_pojistniku(self, databaze_pojistovna):
        for row in databaze_pojistovna.conn.execute('SELECT * FROM pojistenci;'):
            print(f"ID: {row[0]} jméno: {row[1]} prijmeni: {row[2]} telefonní číslo: {row[3]} věk: {row[4]}")
        
    def hledej_pojistnika(self, id, databaze_pojistovna):
        for row in databaze_pojistovna.conn.execute(f"SELECT * FROM pojistenci WHERE id = {id};"):
            print(f"ID: {row[0]} jméno: {row[1]} prijmeni: {row[2]} telefonní číslo: {row[3]} věk: {row[4]}")

    def pridej_pojisteni_pojistnika(self, zadane_id, nazev, castka, predmet, platnost_od, platnost_do, databaze_pojistovna):
        for row in databaze_pojistovna.conn.execute(f'SELECT * FROM pojistenci WHERE id = {zadane_id}'):
            pojisteni = Pojisteni(nazev, castka, predmet, platnost_od, platnost_do)
            pridej_pojisteni = f"INSERT INTO pojisteni (nazev, castka, predmet, platnost_od, platnost_do) VALUES (?, ?, ?, ?, ?)"
            data = (pojisteni.nazev, pojisteni.castka, pojisteni.predmet, pojisteni.platnost_od, pojisteni.platnost_do)
            databaze_pojistovna.cursor.execute(pridej_pojisteni, data)
            databaze_pojistovna.conn.commit()
            return f"Osobě s ID {zadane_id} byl o přidáno pojištění s názvem {pojisteni.nazev}"
        else:
            print("Zadané ID nebylo nalezeno")    

    
    def vypis_pojisteni_pojistnika(self, zadane_id):
        for osoba in self.seznam_pojistencu:
            if osoba.id == int(zadane_id):
                return osoba.vypis_pojisteni()
        else:
            print("Zadané ID nebylo nalezeno")    

            
    def vymaz_pojistnika(self, vymaz_id, databaze_pojistovna):
        for row in databaze_pojistovna.conn.execute(f'SELECT * FROM pojistenci WHERE id = {vymaz_id}'):
            vymaz = f"DELETE FROM pojistenci WHERE id = {vymaz_id}"
            databaze_pojistovna.cursor.execute(vymaz)
            databaze_pojistovna.conn.commit()
            return f"Osoba s ID {vymaz_id} byla vymazána"
                #+ na to vytvořím cizí klíč, který vymaže všechna pojištění            

        else:
            return "Zadaná osoba nebyla nalezena"
       
    def edituj_pojistnika(self, editace_id, databaze_pojistovna):
        for row in databaze_pojistovna.conn.execute(f'SELECT * FROM pojistenci WHERE id_pojistenec = {editace_id}'):
            print(row[1])
            jmeno = input("Zadejte nové jméno:\n")
            prijmeni = input("Zadejte nové příjmení:\n")
            telefonni_cislo = input("Zadejte nové telefonní číslo")
            vek = input("Zadejte nový věk:\n")
            edituj = f"UPDATE pojistenci SET jmeno = ?, prijmeni = ?, telefonni_cislo = ?, vek = ? WHERE id_pojistenec = {editace_id};"
            data = (jmeno, prijmeni, telefonni_cislo, vek)
            databaze_pojistovna.cursor.execute(edituj, data)
            databaze_pojistovna.conn.commit()
            return f"Osoba s ID {editace_id} byla editována"
        else:
            return "Zadané ID nebylo nalezeno"
        
