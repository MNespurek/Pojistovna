import sqlite3

class Databaze:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()
    
    def vytvor_tabulku(self):
        tabulka_pojistenci = f"CREATE TABLE IF NOT EXISTS pojistenci (id_pojistenec INTEGER PRIMARY KEY AUTOINCREMENT, jmeno TEXT, prijmeni TEXT, telefonni_cislo TEXT, vek INTEGER)"

        tabulka_pojisteni = f"CREATE TABLE IF NOT EXISTS pojisteni (id_pojisteni INTEGER PRIMARY KEY AUTOINCREMENT, nazev TEXT, castka INTEGER, predmet TEXT, platnost_od TEXT, platnost_do TEXT)"
        self.cursor.execute(tabulka_pojistenci)
        self.cursor.execute(tabulka_pojisteni)
        self.conn.commit()
        






    
