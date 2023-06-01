from flask import Flask, url_for, render_template, request, redirect
from databaze import Databaze
from osoba import Osoba
from osoba import Osoba_id
import pickle
import sqlite3

app = Flask(__name__)
#vytváří se databáze
databaze_pojistovna = Databaze('databaze_pojistovna.db')
databaze_pojistovna.vytvor_tabulku()

#hlavní stránka
@app.route('/')
def index():
    return render_template('index.html')

# vyspání všech pojištěnců
@app.route('/pojistenci.html')
def pojistenci():
    conn = sqlite3.connect('databaze_pojistovna.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pojistenci')
    print("data vybrána z databáze")
    data = cursor.fetchall()
    return render_template('pojistenci.html', data = data)

#převod na stránku nového pojištěnce
@app.route('/novy_pojistenec.html')
def novy_pojistenec():
    return render_template('novy_pojistenec.html')

#vytváří se nový pojištěnec
#data se ukládají do databáze
@app.route('/add', methods=['POST'])
def add():
    print("metoda add je volána")
    jmeno = request.form['jmeno']
    prijmeni = request.form['prijmeni']
    ulice = request.form['ulice']
    email = request.form['email']
    telefon = request.form['telefon']
    mesto = request.form['mesto']
    psc = request.form['psc']
    osoba = Osoba(jmeno, prijmeni, ulice, email, telefon, mesto, psc)
    print(osoba.jmeno)
    uloz = f"INSERT INTO pojistenci (jmeno, prijmeni, ulice, email, telefon, mesto, psc) VALUES (?, ?, ?, ?, ?, ?, ?);"
    print("data byla vložena do databáze")
    conn = sqlite3.connect('databaze_pojistovna.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pojistenci (jmeno, prijmeni, ulice, email, telefon, mesto, psc) VALUES (?, ?, ?, ?, ?, ?, ?);",
    (osoba.jmeno, osoba.prijmeni, osoba.ulice, osoba.email, osoba.telefon, osoba.mesto, osoba.psc))
    conn.commit()
    return redirect('/ulozeni.html')

#smazání pojištěnce dle jeho ID
@app.route('/smazani/<int:id_pojistenec>')
#pozor! Funguje, pouze metoda GET, ale ne POST!
def smazat_pojistence(id_pojistenec):
    print("Metoda smazání je volána")
    conn = sqlite3.connect('databaze_pojistovna.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM pojistenci WHERE id_pojistenec = ?', (id_pojistenec,))
    conn.commit()
    print("data byla smazána z databáze")
    return redirect('/smazani.html')

#stránka, kde je potvrzeno smazání pojištěnce
@app.route('/smazani.html')
def smazani():
    return render_template('smazani.html')


#nahrání dat pojištěnce pro editaci
# uložení dat do pickle pro převod do další metody 
@app.route('/editovat/<int:id_pojistenec>')
def editace(id_pojistenec):
    
    conn = sqlite3.connect('databaze_pojistovna.db')
    cursor = conn.cursor()
    dotaz = "SELECT * FROM pojistenci WHERE id_pojistenec = ?"
    cursor.execute(dotaz, (id_pojistenec, ))
    vysledek = cursor.fetchone()
    id_pojistenec, jmeno, prijmeni, ulice, email, telefon, mesto, psc = vysledek
    osoba_id = Osoba_id(id_pojistenec, jmeno, prijmeni, ulice, email, telefon, mesto, psc)
    print(osoba_id.jmeno)
    print(osoba_id.id_pojistenec)
    pojistenec = osoba_id
    print(pojistenec.jmeno)
    with open('pojistenec.pickle', 'wb') as file:
        pickle.dump(pojistenec, file)
    return render_template('/editace_pojistenec.html', pojistenec = pojistenec)

#nahrání dat ze souboru pickle
#uložení dat do databáze
@app.route('/ulozit_editaci/<pojistenec>', methods=['POST'])
def ulozit_editaci(pojistenec):
    with open('pojistenec.pickle', 'rb') as file:
        pojistenec = pickle.load(file)
    print(pojistenec.jmeno)
    conn = sqlite3.connect('databaze_pojistovna.db')
    cursor = conn.cursor()
    jmeno = request.form['jmeno']
    prijmeni = request.form['prijmeni']
    ulice = request.form['ulice']
    email = request.form['email']
    telefon = request.form['telefon']
    mesto = request.form['mesto']
    psc = request.form['psc']
    cursor = conn.cursor()
    cursor.execute("UPDATE pojistenci SET jmeno = ?, prijmeni = ?, ulice = ?, email = ?, telefon = ?, mesto = ?, psc = ? WHERE id_pojistenec = ?;",
    (jmeno, prijmeni, ulice, email, telefon, mesto, psc, pojistenec.id_pojistenec))
    conn.commit()
    print("data byla uložena do databáze")
    return redirect('/ulozeni.html')

#stránka, kde je potvrzeno uložení/editace pojištěnce
@app.route('/ulozeni.html')
def ulozeni():
    return render_template('ulozeni.html')

#vybrání dat pojištěnce z databáze a uložení do objektu
@app.route('/pojistenec/<int:id_pojistenec>')
def pojistenec(id_pojistenec):
    print("volána fce pojištěnec")
    conn = sqlite3.connect('databaze_pojistovna.db')
    cursor = conn.cursor()
    dotaz = "SELECT * FROM pojistenci WHERE id_pojistenec = ?"
    cursor.execute(dotaz, (id_pojistenec, ))
    vysledek = cursor.fetchone()
    id_pojistenec, jmeno, prijmeni, ulice, email, telefon, mesto, psc = vysledek
    osoba_id = Osoba_id(id_pojistenec, jmeno, prijmeni, ulice, email, telefon, mesto, psc)
    print(osoba_id.jmeno)
    print(osoba_id.id_pojistenec)
    pojistenec = osoba_id
    print(pojistenec.jmeno)
    return render_template('/pojistenec.html', pojistenec = pojistenec)

#převod na stránku pojištění    
@app.route('/pojisteni.html')
def pojisteni():
    return render_template('pojisteni.html')

#převod na stránku události
@app.route('/udalosti.html')
def udalosti():
    return render_template('udalosti.html')

#převod na stránku o aplikaci
@app.route('/oaplikaci.html')
def oaplikaci():
    return render_template('oaplikaci.html')

#převod na stránku o registraci
@app.route('/registrace.html')
def registrace():
    return render_template('registrace.html')

#převod na stránku přihlásit
@app.route('/prihlasit.html')
def prihlasit():
    return render_template('prihlasit.html')

if __name__ == '__main__':
    app.run(debug=True)

