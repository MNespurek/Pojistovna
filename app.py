from flask import Flask, url_for, render_template, request, redirect, session
from flask_paginate import Pagination, get_page_parameter
from databaze import Databaze
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from osoba import Osoba
from osoba import OsobaId
from osoba import OsobaVypis
from osoba import Registrace
from osoba import Uzivatel
from pojisteni import Pojisteni
from pojisteni import PojisteniId
from pojisteni import PojisteniDetail
from pojisteni import PojisteniSeznam
import pickle
import sqlite3


app = Flask(__name__)
#vytváří se databáze
databaze_pojistovna = Databaze('databaze_pojistovna.db')
databaze_pojistovna.vytvor_tabulku()
app.config['SECRET_KEY'] = 'tajny_klic_pro_podepsani'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dabaze_pojistovna.db'
db = SQLAlchemy(app)



#hlavní stránka
@app.route('/')
def index():
    return render_template('pojistenec/index.html')

# vyspání všech pojištěnců
@app.route('/pojistenec/pojistenci')
def pojistenci():
    seznam_pojistencu = []
    conn = sqlite3.connect('databaze_pojistovna.db')
    cursor = conn.cursor()
    dotaz = 'SELECT id_pojistenec, jmeno, prijmeni, mesto FROM pojistenci'
    cursor.execute(dotaz)
    vysledek = cursor.fetchall()
    print(vysledek)
    for item in vysledek:
        id_pojistenec, jmeno, prijmeni, mesto = item
        osoba = OsobaVypis(id_pojistenec, jmeno, prijmeni, mesto)
        seznam_pojistencu.append(osoba)
        print(osoba.jmeno)
    page = int(request.args.get(get_page_parameter(), 1))
    per_page = 3
    total = len(seznam_pojistencu)
    pagination = Pagination(page = page,per_page = per_page, total = total, prev_label = "předchozí", next_label = "následující", css_framework='bootstrap5')
    start = (page-1) * per_page
    end = start + per_page
    zobrazeni_pojistencu = seznam_pojistencu[start:end]
    return render_template('pojistenec/pojistenci.html', seznam_pojistencu = zobrazeni_pojistencu, pagination = pagination)

#převod na stránku nového pojištěnce
@app.route('/pojistenec/novy_pojistenec')
def novy_pojistenec():
    return render_template('pojistenec/novy_pojistenec.html')

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
    conn = sqlite3.connect('databaze_pojistovna.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pojistenci (jmeno, prijmeni, ulice, email, telefon, mesto, psc) VALUES (?, ?, ?, ?, ?, ?, ?);",
    (osoba.jmeno, osoba.prijmeni, osoba.ulice, osoba.email, osoba.telefon, osoba.mesto, osoba.psc))
    conn.commit()
    return redirect('pojistenec/ulozeni')

#smazání pojištěnce dle jeho ID
@app.route('/pojistenec/smazani/<int:id_pojistenec>')
#pozor! Funguje, pouze metoda GET, ale ne POST!
def smazat_pojistence(id_pojistenec):
    print("Metoda smazání je volána")
    conn = sqlite3.connect('databaze_pojistovna.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM pojistenci WHERE id_pojistenec = ?', (id_pojistenec,))
    conn.commit()
    print("data byla smazána z databáze")
    return redirect('/pojistenec/smazani')

#stránka, kde je potvrzeno smazání pojištěnce
@app.route('/pojistenec/smazani')
def smazani():
    return render_template('pojistenec/smazani.html')


#nahrání dat pojištěnce pro editaci
# uložení dat do pickle pro převod do další metody 
@app.route('/pojistenec/editovat/<int:id_pojistenec>')
def editace(id_pojistenec):
    conn = sqlite3.connect('databaze_pojistovna.db')
    cursor = conn.cursor()
    dotaz = "SELECT * FROM pojistenci WHERE id_pojistenec = ?"
    cursor.execute(dotaz, (id_pojistenec, ))
    vysledek = cursor.fetchone()
    id_pojistenec, jmeno, prijmeni, ulice, email, telefon, mesto, psc = vysledek
    osoba_id = OsobaId(id_pojistenec, jmeno, prijmeni, ulice, email, telefon, mesto, psc)
    print(osoba_id.jmeno)
    print(osoba_id.id_pojistenec)
    pojistenec = osoba_id
    print(pojistenec.jmeno)
    with open('pojistenec.pickle', 'wb') as file:
        pickle.dump(pojistenec, file)
    return render_template('/pojistenec/editace_pojistenec.html', pojistenec = pojistenec)

#nahrání dat ze souboru pickle
#uložení dat do databáze
@app.route('/pojistenec/ulozit_editaci/<pojistenec>', methods=['POST'])
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
    return redirect('/pojistenec/ulozeni')

#stránka, kde je potvrzeno uložení/editace pojištěnce
@app.route('/pojistenec/ulozeni')
def ulozeni():
    return render_template('/pojistenec/ulozeni.html')

#vybrání dat pojištěnce z databáze a uložení do objektu
@app.route('/pojistenec/pojistenec/<int:id_pojistenec>')
def pojistenec(id_pojistenec):
    
    conn = sqlite3.connect('databaze_pojistovna.db')
    cursor = conn.cursor()
    dotaz = "SELECT * FROM pojistenci WHERE id_pojistenec = ?"
    cursor.execute(dotaz, (id_pojistenec, ))
    vysledek = cursor.fetchone()
    id_pojistenec, jmeno, prijmeni, ulice, email, telefon, mesto, psc = vysledek
    
    osoba_id = OsobaId(id_pojistenec, jmeno, prijmeni, ulice, email, telefon, mesto, psc)
    pojistenec = osoba_id
    
    dotaz_pojisteni = "SELECT id_pojisteni, nazev, castka FROM pojisteni WHERE id_pojistenec = ?"
    cursor.execute(dotaz_pojisteni, (id_pojistenec, ))
    vysledek_pojisteni = cursor.fetchall()
    print(vysledek_pojisteni)
    seznam_pojisteni = []
    for item in vysledek_pojisteni:
        id_pojisteni, nazev, castka = item
        print(nazev)
        pojisteni = PojisteniId(id_pojisteni, nazev, castka)
        seznam_pojisteni.append(pojisteni)
    page = int(request.args.get(get_page_parameter(), 1))
    per_page = 3
    total = len(seznam_pojisteni)
    pagination = Pagination(page = page,per_page = per_page, total = total, prev_label = "předchozí", next_label = "následující", css_framework='bootstrap5')
    start = (page-1) * per_page
    end = start + per_page
    zobrazeni_pojistencu = seznam_pojisteni[start:end]

    return render_template('/pojistenec/pojistenec.html', pojistenec = pojistenec, seznam_pojisteni = zobrazeni_pojistencu, pagination = pagination)

#převod na stránku pojištění    
@app.route('/pojisteni/pojisteni/')
def pojisteni():
    seznam_pojisteni = []
    conn = sqlite3.connect('databaze_pojistovna.db')
    cursor = conn.cursor()
    dotaz = 'SELECT p.id_pojistenec, p.id_pojisteni, po.jmeno, po.prijmeni,  p.nazev, p.castka FROM pojisteni as p JOIN pojistenci as po ON p.id_pojistenec = po.id_pojistenec;'
    cursor.execute(dotaz)
    vysledek = cursor.fetchall()
    print(vysledek)
    for item in vysledek:
        id_pojistenec, id_pojisteni, jmeno, prijmeni, nazev, castka = item
        pojisteni = PojisteniSeznam(id_pojistenec, id_pojisteni, jmeno, prijmeni, nazev, castka)
        seznam_pojisteni.append(pojisteni)
        print(pojisteni.jmeno, pojisteni.nazev)
    page = int(request.args.get(get_page_parameter(), 1))
    per_page = 3
    total = len(seznam_pojisteni)
    pagination = Pagination(page = page,per_page = per_page, total = total, prev_label = "předchozí", next_label = "následující", css_framework='bootstrap5')
    start = (page-1) * per_page
    end = start + per_page
    zobrazeni_pojisteni = seznam_pojisteni[start:end]
    return render_template('/pojisteni/pojisteni.html', seznam_pojisteni = zobrazeni_pojisteni, pojisteni = pojisteni, pagination = pagination)

@app.route('/nove_pojisteni/<int:id_pojistenec>')
def nove_pojisteni(id_pojistenec):
    print("volána stránka nové pojištění")
    conn = sqlite3.connect('databaze_pojistovna.db')
    cursor = conn.cursor()
    dotaz = "SELECT * FROM pojistenci WHERE id_pojistenec = ?"
    cursor.execute(dotaz, (id_pojistenec, ))
    vysledek = cursor.fetchone()
    id_pojistenec, jmeno, prijmeni, ulice, email, telefon, mesto, psc = vysledek
    
    pojistenec = OsobaId(id_pojistenec, jmeno, prijmeni, ulice, email, telefon, mesto, psc)
    return render_template('/pojisteni/nove_pojisteni.html', pojistenec = pojistenec, id_pojistenec = pojistenec.id_pojistenec)

@app.route('/add_pojisteni/<int:id_pojistenec>', methods = ['POST'])
def add_pojisteni(id_pojistenec):
    print(id_pojistenec)
    nazev = request.form['nazev']
    castka = request.form['castka']
    predmet = request.form['predmet']
    platnost_od = request.form['platnost_od']
    platnost_do = request.form['platnost_do']
    pojisteni = Pojisteni(id_pojistenec, nazev, castka, predmet, platnost_od, platnost_do)
    print(pojisteni.nazev)
    print(pojisteni.platnost_od)
    print(pojisteni.predmet)
    conn = sqlite3.connect('databaze_pojistovna.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pojisteni (id_pojistenec, nazev, castka, predmet, platnost_od, platnost_do) VALUES (?, ?, ?, ?, ?, ?);", (id_pojistenec, pojisteni.nazev, pojisteni.castka, pojisteni.predmet, pojisteni.platnost_od, pojisteni.platnost_do))
    conn.commit()
    print("data byla vložena do databáze")
    return redirect ('/pojistenec/ulozeni')

@app.route('/pojisteni/detail_pojisteni/<int:id_pojisteni>')
def detail_pojisteni(id_pojisteni):
    print("volána fce detail pojištění")

    conn = sqlite3.connect('databaze_pojistovna.db')
    cursor = conn.cursor()
    dotaz_pojisteni = "SELECT * FROM pojisteni WHERE id_pojisteni = ?"
    cursor.execute(dotaz_pojisteni, (id_pojisteni, ))
    vysledek_pojisteni = cursor.fetchone()
    print(vysledek_pojisteni)
    id_pojisteni, id_pojistenec, nazev, castka, predmet, platnost_od, platnost_do = vysledek_pojisteni
    pojisteni = PojisteniDetail(id_pojisteni, id_pojistenec, nazev, castka, predmet, platnost_od, platnost_do)
    return render_template('/pojisteni/detail_pojisteni.html', pojisteni = pojisteni)

#smazání pojištěnce dle jeho ID
@app.route('/pojisteni/smazani/<int:id_pojisteni>')
#pozor! Funguje, pouze metoda GET, ale ne POST!
def smazat_pojisteni(id_pojisteni):
    print("Metoda smazání je volána")
    conn = sqlite3.connect('databaze_pojistovna.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM pojisteni WHERE id_pojisteni = ?', (id_pojisteni,))
    conn.commit()
    print("data byla smazána z databáze")
    return redirect('/pojistenec/smazani')

#nahrání dat pojištěnce pro editaci
# uložení dat do pickle pro převod do další metody 
@app.route('/pojisteni/editace_pojisteni/<int:id_pojisteni>')
def editace_pojisteni(id_pojisteni):
    print("volána fce editace pojištění")
    conn = sqlite3.connect('databaze_pojistovna.db')
    cursor = conn.cursor()
    dotaz = "SELECT * FROM pojisteni WHERE id_pojisteni = ?"
    cursor.execute(dotaz, (id_pojisteni, ))
    vysledek = cursor.fetchone()
    id_pojisteni, id_pojistenec, nazev, predmet, castka, platnost_od, platnost_do = vysledek
    pojisteni = PojisteniDetail(id_pojisteni, id_pojistenec, nazev, predmet, castka, platnost_od, platnost_do)
    print(pojisteni.nazev)
    print(pojisteni.id_pojistenec)
    print(pojisteni.platnost_do)
    with open('pojisteni.pickle', 'wb') as file:
        pickle.dump(pojisteni, file)
    return render_template('/pojisteni/editace_pojisteni.html', id_pojisteni = pojisteni.id_pojisteni, pojisteni = pojisteni)

#nahrání dat ze souboru pickle
#uložení dat do databáze
@app.route('/pojisteni/ulozit_editaci/<int:id_pojisteni>', methods=['POST'])
def ulozit_editaci_pojisteni(id_pojisteni):
    with open('pojisteni.pickle', 'rb') as file:
        pojisteni = pickle.load(file)
    print(pojisteni.nazev)
    print(pojisteni.castka)
    conn = sqlite3.connect('databaze_pojistovna.db')
    cursor = conn.cursor()
    nazev = request.form['nazev']
    castka = request.form['castka']
    predmet = request.form['predmet']
    platnost_od = request.form['platnost_od']
    platnost_do = request.form['platnost_do']
    cursor = conn.cursor()
    cursor.execute("UPDATE pojisteni SET nazev = ?, castka = ?, predmet = ?, platnost_od = ?, platnost_do = ? WHERE id_pojisteni = ?;",
    (nazev, castka, predmet, platnost_od, platnost_do, id_pojisteni))
    conn.commit()
    print("data byla uložena do databáze")
    return redirect('/pojistenec/ulozeni')

#převod na stránku události
@app.route('/udalosti.html')
def udalosti():
    return render_template('/ostatni/udalosti.html')

#převod na stránku o aplikaci
@app.route('/oaplikaci.html')
def oaplikaci():
    return render_template('/ostatni/oaplikaci.html')

@app.route('/registrace')
def registrace():
    return render_template('/ostatni/registrace.html')


#převod na stránku o registraci
@app.route('/nova_registrace', methods = ['POST'])
def nova_registrace():
    print("metoda registrace je volána")
    conn = sqlite3.connect('databaze_pojistovna.db')
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM registrace")
    emaily = cursor.fetchall()
    print(emaily)
    jmeno = request.form['jmeno']
    prijmeni = request.form['prijmeni']
    heslo = request.form['heslo']
    potvrzeni_heslo = request.form['potvrzeni_heslo']
    email = request.form['email']
    for email_db in emaily:
        print(email_db)
        vysledek = ", ".join(email_db)
        print(email)
        print(vysledek)
        if vysledek == email:
            return render_template('/ostatni/registrace_heslo.html')
        if heslo != potvrzeni_heslo:
            return render_template('/ostatni/registrace_heslo.html')
        else:
            hash_heslo = generate_password_hash(heslo)
            registrace = Registrace(jmeno, prijmeni, hash_heslo, email)
            print(registrace.hash_heslo)
            conn = sqlite3.connect('databaze_pojistovna.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO registrace (jmeno, prijmeni, hash_heslo, email) VALUES (?, ?, ?, ?);",
            (registrace.jmeno, registrace.prijmeni, registrace.hash_heslo, registrace.email))
            conn.commit()
            return redirect('pojistenec/ulozeni')


#převod na stránku přihlásit
@app.route('/prihlasit')
def prihlasit():
    return render_template('/ostatni/prihlasit.html')


@app.route('/overit_prihlaseni', methods = ['POST'])
def overit_prihlaseni():
    print("volána fce ověřit přihlášení")
    email = request.form['email']
    heslo = request.form['heslo']
    print(heslo)
    conn = sqlite3.connect('databaze_pojistovna.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id_registrace, email, hash_heslo FROM registrace where email = ?", (email, ))
    vysledek = cursor.fetchone()
    id_registrace, email, hash_heslo = vysledek
    uzivatel = Uzivatel(id_registrace, email, hash_heslo)
    print(uzivatel.email)
    print(uzivatel.id_registrace)
    print(uzivatel.hash_heslo)
    print(heslo)
    if check_password_hash(uzivatel.hash_heslo, heslo):
        session['id_registrace'] = uzivatel.id_registrace
        return render_template('/ostatni/potvrdit_prihlaseni.html')
    else:
        return render_template('/ostatni/prihlasit_heslo.html')
    
    







# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if 'logged_in' not in session:
#             return redirect(url_for('prihlasit'))
#         return f(*args, **kwargs)
#     return decorated_function

# def admin_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if 'logged_in' not in session or session['role'] != 'administrátor':
#             return redirect(url_for('prihlasit'))
#         return f(*args, **kwargs)
#     return decorated_function



if __name__ == '__main__':
    app.run(debug=True)
