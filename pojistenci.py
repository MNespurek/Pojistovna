
from osoba import Osoba
from pojisteni import Pojisteni

class Pojistenci():
#1
    def vytvor_uloz_pojistnika(self, jmeno, prijmeni, telefonni_cislo, vek, databaze_pojistovna):        
        osoba = Osoba(jmeno, prijmeni, telefonni_cislo, vek)
        uloz = f"INSERT INTO pojistenci (jmeno, prijmeni, telefonni_cislo, vek) VALUES (?, ?, ?, ?);"
        data = (osoba.jmeno, osoba.prijmeni, osoba.telefonni_cislo, osoba.vek)
        databaze_pojistovna.cursor.execute(uloz, data)
        databaze_pojistovna.conn.commit()
#2        
    def pridej_pojisteni_pojistnika(self, zadane_id, nazev, castka, predmet, platnost_od, platnost_do, databaze_pojistovna):
        for row in databaze_pojistovna.conn.execute(f'SELECT * FROM pojistenci WHERE id_pojistenec = {zadane_id}'):
            pojisteni = Pojisteni(nazev, castka, predmet, platnost_od, platnost_do)
            
            pridej_pojisteni = f"INSERT INTO pojisteni (id_pojistenec, nazev, castka, predmet, platnost_od, platnost_do) VALUES (?, ?, ?, ?, ?, ?)"
            data = (zadane_id, pojisteni.nazev, pojisteni.castka, pojisteni.predmet, pojisteni.platnost_od, pojisteni.platnost_do)
            databaze_pojistovna.cursor.execute(pridej_pojisteni, data)
            databaze_pojistovna.conn.commit()
            return f"Osobě s ID {zadane_id} byl o přidáno pojištění s názvem {pojisteni.nazev}"
        else:
            print("Zadané ID nebylo nalezeno")    


#3 = hledej_pojistnika + vypis_pojisteni_pojistnika
         
    def hledej_pojistnika(self, id, databaze_pojistovna):
        for row in databaze_pojistovna.conn.execute(f"SELECT * FROM pojistenci WHERE id_pojistenec = {id};"):
            print(f"ID: {row[0]} jméno: {row[1]} prijmeni: {row[2]} telefonní číslo: {row[3]} věk: {row[4]}")
 
#4           
#4       
    def vypis_pojisteni_pojistnika(self, zadane_id, databaze_pojistovna):
        seznam_pojisteni = ""
        for row in databaze_pojistovna.conn.execute(f'SELECT * FROM pojisteni WHERE id_pojistenec = {zadane_id}'):
            seznam_pojisteni = seznam_pojisteni + f"ID pojištění: {row[0]} ID pojištěnce: {row[1]} název: {row[2]} částka {row[3]} předmět: {row[4]} platnost od: {row[5]} platnost do: {row[6]}\n"
        return seznam_pojisteni
        # else:
        #     print("Zadané ID nebylo nalezeno")  
#5
    def vypis_vsech_pojistniku(self, databaze_pojistovna):
        for row in databaze_pojistovna.conn.execute('SELECT * FROM pojistenci;'):
            print(f"ID: {row[0]} jméno: {row[1]} prijmeni: {row[2]} telefonní číslo: {row[3]} věk: {row[4]}")
#6
    def vymaz_pojistnika(self, vymaz_id, databaze_pojistovna):
        for row in databaze_pojistovna.conn.execute(f'SELECT * FROM pojistenci WHERE id_pojistenec = {vymaz_id}'):
            vymaz = f"DELETE FROM pojistenci WHERE id_pojistenec = {vymaz_id}"
            databaze_pojistovna.cursor.execute(vymaz)
            databaze_pojistovna.conn.commit()
            return f"Osoba s ID {vymaz_id} byla vymazána"
                #+ na to vytvořím cizí klíč, který vymaže všechna pojištění            
        else:
            return "Zadaná osoba nebyla nalezena"
#7        
    def vymaz_pojisteni_pojistnika(self, vymazat_id, databaze_pojistovna):
        for row in databaze_pojistovna.conn.execute(f'SELECT * FROM pojisteni WHERE id_pojisteni = {vymazat_id}'):
            vymaz_pojisteni = f"DELETE FROM pojisteni WHERE id_pojisteni = {vymazat_id}"
            databaze_pojistovna.cursor.execute(vymaz_pojisteni)
            databaze_pojistovna.conn.commit()
            return f"Pojištění s ID {vymazat_id} bylo vymazáno"
        else:
            print("Zadané ID nebylo nalezeno")    
#8
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
#9        
    def edituj_pojisteni(self, editace_id, databaze_pojistovna):
        for row in databaze_pojistovna.conn.execute(f'SELECT * FROM pojisteni WHERE id_pojisteni = {editace_id}'):
            print(row[1])
            nazev = input("Zadejte nový název:\n")
            castka = input("Zadejte novou částku:\n")
            predmet = input("Zadejte nový předmět:\n")
            platnost_od = input("Zadejte platnost od:\n")
            platnost_do = input("Zadejte platnost do:\n")
            edituj = f"UPDATE pojisteni SET nazev = ?, castka = ?, predmet = ?, platnost_od = ?, platnost_do = ? WHERE id_pojisteni = {editace_id};"
            data = (nazev, castka, predmet, platnost_od, platnost_do)
            databaze_pojistovna.cursor.execute(edituj, data)
            databaze_pojistovna.conn.commit()
            return f"Pojisteni s ID {editace_id} bylo upraveno"
        else:
            return "Zadané ID nebylo nalezeno"
