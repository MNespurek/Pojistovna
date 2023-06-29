import sqlite3
from flask_sqlalchemy import SQLAlchemy

class Databaze:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()
    
    def vytvor_tabulku(self):
        tabulka_pojistenci = f"CREATE TABLE IF NOT EXISTS pojistenci (id_pojistenec INTEGER PRIMARY KEY AUTOINCREMENT, jmeno TEXT, prijmeni TEXT, ulice TEXT, email TEXT, telefon TEXT, mesto TEXT, psc TEXT)"

        tabulka_pojisteni = f"CREATE TABLE IF NOT EXISTS pojisteni (id_pojisteni INTEGER, id_pojistenec INTEGER, nazev TEXT, castka INTEGER, predmet TEXT, platnost_od TEXT, platnost_do TEXT, PRIMARY KEY (id_pojisteni AUTOINCREMENT), FOREIGN KEY (id_pojistenec) REFERENCES pojistenci(id_pojistenec) ON DELETE CASCADE)"

        tabulka_registrace = f"CREATE TABLE IF NOT EXISTS registrace (id_registrace INTEGER PRIMARY KEY AUTOINCREMENT, jmeno TEXT, prijmeni TEXT, hash_heslo TEXT, email TEXT)"
        
        self.cursor.execute("PRAGMA foreign_keys=ON")
        self.cursor.execute(tabulka_pojistenci)
        self.cursor.execute(tabulka_pojisteni)
        self.cursor.execute(tabulka_registrace)
        self.conn.commit()
        






    
