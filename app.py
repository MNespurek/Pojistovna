from flask import Flask, url_for, render_template, request, redirect, session
from flask_paginate import Pagination, get_page_parameter
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#vytváří se databáze
app.config['SECRET_KEY'] = 'tajny_klic_pro_podepsani'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_pojistovna.db'
db = SQLAlchemy(app)

class Pojistenci(db.Model):
    id_pojistenec = db.Column(db.Integer, primary_key=True, autoincrement=True)
    jmeno = db.Column(db.String, nullable = False)
    prijmeni = db.Column(db.String, nullable = False)
    ulice = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False)
    telefon = db.Column(db.String, nullable = False)
    mesto = db.Column(db.String, nullable = False)
    psc = db.Column(db.String, nullable = False)
    pojisteni = db.relationship('Pojisteni', backref='pojistenci', cascade='all, delete')

class Pojisteni(db.Model):
    id_pojisteni = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_pojistenec = db.Column(db.Integer, db.ForeignKey('pojistenci.id_pojistenec'))
    nazev = db.Column(db.String, nullable = False)
    castka = db.Column(db.String, nullable = False)
    predmet = db.Column(db.String, nullable = False)
    platnost_od = db.Column(db.String, nullable = False)
    platnost_do = db.Column(db.String, nullable = False)

#hlavní stránka
@app.route('/')
def index():
    return render_template('pojistenec/index.html')

# vyspání všech pojištěnců
@app.route('/pojistenec/pojistenci')
def pojistenci():
    seznam_pojistencu = []
    pojistenci = Pojistenci.query.all()
    for pojistenec in pojistenci:
        seznam_pojistencu.append(pojistenec)
        print(pojistenec.jmeno)
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
    pojistenec = Pojistenci(jmeno = jmeno, prijmeni = prijmeni, ulice = ulice, email = email, telefon = telefon, mesto = mesto, psc = psc)
    db.session.add(pojistenec)
    db.session.commit()
    return redirect('pojistenec/ulozeni')

#smazání pojištěnce dle jeho ID
@app.route('/pojistenec/smazani/<int:id_pojistenec>')
def smazat_pojistence(id_pojistenec):
    print("Metoda smazání je volána")
    pojistenec = db.session.get(Pojistenci, id_pojistenec)
    db.session.delete(pojistenec)
    db.session.commit()
    return redirect('/pojistenec/smazani')

#stránka, kde je potvrzeno smazání pojištěnce
@app.route('/pojistenec/smazani')
def smazani():
    return render_template('pojistenec/smazani.html')

#editace pojištěnce
@app.route('/pojistenec/editovat/<int:id_pojistenec>', methods=['GET', 'POST'])
def editace(id_pojistenec):
    print("volaná fce editace")
    pojistenec = db.session.get(Pojistenci, id_pojistenec)
    if pojistenec:
        if request.method == 'POST':
            print("metoda Post volána")
            pojistenec.jmeno = request.form['jmeno']
            pojistenec.prijmeni = request.form['prijmeni']
            pojistenec.ulice = request.form['ulice']
            pojistenec.email = request.form['email']
            pojistenec.telefon = request.form['telefon']
            pojistenec.mesto = request.form['mesto']
            pojistenec.psc = request.form['psc']
            db.session.commit()
            print("data uložena do databáze")
            return redirect('/pojistenec/ulozeni')
        else:
            print("volána fce editace data nahrána")
            return render_template('pojistenec/editace_pojistenec.html', pojistenec = pojistenec)
    else:
        return "Pojištěnec neexistuje"

#stránka, kde je potvrzeno uložení/editace pojištěnce
@app.route('/pojistenec/ulozeni')
def ulozeni():
    return render_template('/pojistenec/ulozeni.html')

#detail pojištěnce včetně pojištění
@app.route('/pojistenec/pojistenec/<int:id_pojistenec>')
def pojistenec(id_pojistenec):
    pojistenec = db.session.get(Pojistenci, id_pojistenec)
    pojisteni = db.session.query(Pojisteni).filter_by(id_pojistenec = id_pojistenec).all()
    seznam_pojisteni = []
    for poj in pojisteni:
        seznam_pojisteni.append(poj)
    page = int(request.args.get(get_page_parameter(), 1))
    per_page = 3
    total = len(seznam_pojisteni)
    pagination = Pagination(page = page,per_page = per_page, total = total, prev_label = "předchozí", next_label = "následující", css_framework='bootstrap5')
    start = (page-1) * per_page
    end = start + per_page
    zobrazeni_pojistencu = seznam_pojisteni[start:end]

    return render_template('/pojistenec/pojistenec.html', pojistenec = pojistenec, seznam_pojisteni = zobrazeni_pojistencu, pagination = pagination)

#výpis pojištění    
@app.route('/pojisteni/pojisteni/')
def pojisteni():
    seznam_pojisteni = []
    pojisteni = Pojisteni.query.all()
    for poj in pojisteni:
        pojistenec = db.session.get(Pojistenci, poj.id_pojistenec)
        
        poj.jmeno = pojistenec.jmeno
        poj.prijmeni = pojistenec.prijmeni
        print(poj.nazev)
        seznam_pojisteni.append(poj)
        
    page = int(request.args.get(get_page_parameter(), 1))
    per_page = 3
    total = len(seznam_pojisteni)
    pagination = Pagination(page = page,per_page = per_page, total = total, prev_label = "předchozí", next_label = "následující", css_framework='bootstrap5')
    start = (page-1) * per_page
    end = start + per_page
    zobrazeni_pojisteni = seznam_pojisteni[start:end]
    return render_template('/pojisteni/pojisteni.html', seznam_pojisteni = zobrazeni_pojisteni, pojisteni = pojisteni, pojistenec = pojistenec, pagination = pagination)

@app.route('/nove_pojisteni/<int:id_pojistenec>')
def nove_pojisteni(id_pojistenec):
    print("volána stránka nové pojištění")
    pojistenec = db.session.get(Pojistenci, id_pojistenec)
    return render_template('/pojisteni/nove_pojisteni.html', pojistenec = pojistenec, id_pojistenec = pojistenec.id_pojistenec)

@app.route('/add_pojisteni/<int:id_pojistenec>', methods = ['POST'])
def add_pojisteni(id_pojistenec):
    print(id_pojistenec)
    nazev = request.form['nazev']
    castka = request.form['castka']
    predmet = request.form['predmet']
    platnost_od = request.form['platnost_od']
    platnost_do = request.form['platnost_do']
    pojisteni = Pojisteni(id_pojistenec = id_pojistenec, nazev = nazev, castka = castka, predmet = predmet, platnost_od = platnost_od, platnost_do = platnost_do)
    db.session.add(pojisteni)
    db.session.commit()
    print("data byla vložena do databáze")
    return redirect ('/pojistenec/ulozeni')

@app.route('/pojisteni/detail_pojisteni/<int:id_pojisteni>')
def detail_pojisteni(id_pojisteni):
    print("volána fce detail pojištění")
    pojisteni = db.session.query(Pojisteni).get(id_pojisteni)
    return render_template('/pojisteni/detail_pojisteni.html', pojisteni = pojisteni)

#smazání pojištěnce dle jeho ID
@app.route('/pojisteni/smazani/<int:id_pojisteni>')

def smazat_pojisteni(id_pojisteni):
    print("Metoda smazání je volána")
    pojisteni = db.session.get(Pojisteni, id_pojisteni)
    db.session.delete(pojisteni)
    db.session.commit()
    print("data byla smazána z databáze")
    return redirect('/pojistenec/smazani')

#editace pojištěnce
@app.route('/pojisteni/editace_pojisteni/<int:id_pojisteni>', methods=['GET', 'POST'])
def editace_pojisteni(id_pojisteni):
    print("volána fce editace pojištění")
    pojisteni = db.session.get(Pojisteni, id_pojisteni)
    if pojisteni:
        if request.method == 'POST':
            pojisteni.nazev = request.form['nazev']
            pojisteni.castka = request.form['castka']
            pojisteni.predmet = request.form['predmet']
            pojisteni.platnost_od = request.form['platnost_od']
            pojisteni.platnost_do = request.form['platnost_do']
            db.session.commit()
            print("data uložena do databáze")
            return redirect('/pojistenec/ulozeni')
        else:
            print("volána fce editace pojištění nahrání dat")
            return render_template('/pojisteni/editace_pojisteni.html', pojisteni = pojisteni)
    else:
        return "Pojištění neexistuje"


#převod na stránku události
@app.route('/udalosti.html')
def udalosti():
    return render_template('/ostatni/udalosti.html')

#převod na stránku o aplikaci
@app.route('/oaplikaci.html')
def oaplikaci():
    return render_template('/ostatni/oaplikaci.html')

#převod na stránku o registraci

@app.route('/registrace')
def registrace():
    return render_template('/ostatni/registrace.html')

#přidat novou registraci
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

#přihlášení
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
    with app.app_context():
        db.create_all()

    app.run(debug=True)
    

