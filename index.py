from flask import Flask, url_for, render_template, request, redirect, session, abort, g, current_app, flash
from flask_paginate import Pagination, get_page_parameter
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
from flask_principal import Principal, Permission, RoleNeed, UserNeed, identity_loaded, Identity, ActionNeed, AnonymousIdentity, identity_changed, identity_loaded
from datetime import datetime

app = Flask(__name__)
#vytváří se databáze
app.config['SECRET_KEY'] = 'tajny_klic_pro_podepsani'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:admin@localhost/db_pojistovna'
db = SQLAlchemy(app)
#objekt pro logování
login = LoginManager()
login.init_app(app)

#odkaz na stránku, pokud není uživatel přihlášený
login.login_view = 'nutna_registrace'

#inicializace rozšíření Principal
principals = Principal(app)

#definování uživatelů aplikace
pracovnik = Permission(RoleNeed('pracovnik'))
vedouci = Permission(RoleNeed('vedouci'))
administrator = Permission(RoleNeed('administrator'))

#kontrola identity uživatele - id_uzivatel a id_role
@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    identity.user = current_user
    if hasattr(current_user, 'id_uzivatel'):
        identity.provides.add(UserNeed(current_user.id_uzivatel))
    
    if hasattr(current_user, 'id_role'):
        if current_user.id_role == 1:
            identity.provides.add(RoleNeed('pracovnik'))
        if current_user.id_role == 2:
            identity.provides.add(RoleNeed('vedouci'))
        if current_user.id_role == 3:
            identity.provides.add(RoleNeed('administrator'))
        
#tabulka pojištěnci
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

#tabulka pojištění
class Pojisteni(db.Model):
    id_pojisteni = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_pojistenec = db.Column(db.Integer, db.ForeignKey('pojistenci.id_pojistenec'))
    nazev = db.Column(db.String, nullable = False)
    castka = db.Column(db.String, nullable = False)
    predmet = db.Column(db.String, nullable = False)
    platnost_od = db.Column(db.String, nullable = False)
    platnost_do = db.Column(db.String, nullable = False)

#tabulka uživatel
class Uzivatel(UserMixin, db.Model):
    id_uzivatel = db.Column(db.Integer, primary_key=True, autoincrement=True)
    jmeno = db.Column(db.String)
    prijmeni = db.Column(db.String)
    hash_heslo = db.Column(db.String)
    email = db.Column(db.String)
    id_role = db.Column(db.Integer, db.ForeignKey('role.id_role'))
    
    def nastav_heslo(self, heslo):
        self.hash_heslo = generate_password_hash(heslo)

    def kontrola_hesla(self, heslo):
        return check_password_hash(self.hash_heslo, heslo)
    
    #získání id_uzivatele
    def get_id(self):
        return str(self.id_uzivatel)

    @staticmethod
    def get(id_uzivatel):
        return Uzivatel(id_uzivatel)


#tabulka role
#vytvoření rolí podle oprávnění
class Role(db.Model):
    id_role = db.Column(db.Integer, primary_key=True, autoincrement=True )
    nazev = db.Column(db.String, unique=True)
    muze_vytvaret = db.Column(db.Boolean, default=True)
    muze_cist = db.Column(db.Boolean, default=True)
    muze_upravit = db.Column(db.Boolean, default=False)
    muze_mazat = db.Column(db.Boolean, default=False)
    uzivatele = db.relationship('Uzivatel', backref='role')

def muze_cist():
    return current_user.role.muze_cist
    
def muze_vytvaret():
    return current_user.role.muze_vytvaret
    
def muze_upravit():
    return current_user.role.muze_upravit
    
def muze_mazat():
    return current_user.role.muze_mazat

#kontrola logování
@login.user_loader
def load_user(id_uzivatel):
    return db.session.get(Uzivatel, id_uzivatel)

#definování příhlášení uživatele
class LoginForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[DataRequired()], render_kw={"placeholder": "Heslo"})

#třída pro registraci
class RegistrationForm(FlaskForm):
    jmeno = StringField('jmeno', validators=[DataRequired()], render_kw={"placeholder": "Jméno"})
    prijmeni = StringField('prijmeni', validators=[DataRequired()], render_kw={"placeholder": "Příjmení"})
    heslo = PasswordField('heslo', validators=[DataRequired()], render_kw={"placeholder": "heslo"})
    potvrzeni_hesla = PasswordField('potvrzeni_hesla', validators=[DataRequired(), EqualTo('heslo')], render_kw={"placeholder": "Opakování hesla"})
    email = StringField('email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    submit = SubmitField('registrovat')

#kontrola rolí, zda jsou v databázi, pokud ne, vytvoří se
def kontrola_roli():
    role = Role.query.all()
    if not role:
        pracovnik_role = Role(nazev="pracovnik")
        vedouci_role = Role(nazev="vedouci", muze_upravit=True)
        administrator_role = Role(nazev="administrator", muze_upravit=True, muze_mazat=True)
        db.session.add(pracovnik_role)
        db.session.add(vedouci_role)
        db.session.add(administrator_role)
        db.session.commit()

#hlavní stránka
@app.route('/')
def index():
    return render_template('pojistenec/index.html', current_user=current_user)

# vyspání všech pojištěnců
@app.route('/pojistenec/pojistenci')
@login_required
def pojistenci():
        seznam_pojistencu = []
        pojistenci = Pojistenci.query.all()
        for pojistenec in pojistenci:
            seznam_pojistencu.append(pojistenec)
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
@login_required
def novy_pojistenec():
    return render_template('pojistenec/novy_pojistenec.html')

#vytváří se nový pojištěnec
#data se ukládají do databáze
@app.route('/add', methods=['POST'])
@login_required
def add():
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
@login_required
def smazat_pojistence(id_pojistenec):
    if muze_mazat():
        pojistenec = db.session.get(Pojistenci, id_pojistenec)
        db.session.delete(pojistenec)
        db.session.commit()
        return redirect('/pojistenec/smazani')
    return render_template('/ostatni/opravneni.html')

#stránka, kde je potvrzeno smazání pojištěnce
@app.route('/pojistenec/smazani')
@login_required
def smazani():
    return render_template('pojistenec/smazani.html')

#editace pojištěnce
@app.route('/pojistenec/editovat/<int:id_pojistenec>', methods=['GET', 'POST'])
@login_required
def editace(id_pojistenec):
    if muze_upravit():
        pojistenec = db.session.get(Pojistenci, id_pojistenec)
        if pojistenec:
            if request.method == 'POST':
                pojistenec.jmeno = request.form['jmeno']
                pojistenec.prijmeni = request.form['prijmeni']
                pojistenec.ulice = request.form['ulice']
                pojistenec.email = request.form['email']
                pojistenec.telefon = request.form['telefon']
                pojistenec.mesto = request.form['mesto']
                pojistenec.psc = request.form['psc']
                db.session.commit()
                return redirect('/pojistenec/ulozeni')
            else:
                return render_template('pojistenec/editace_pojistenec.html', pojistenec = pojistenec)
        
    return render_template('/ostatni/opravneni.html')

#stránka, kde je potvrzeno uložení/editace pojištěnce
@app.route('/pojistenec/ulozeni')
@login_required
def ulozeni():
    return render_template('/pojistenec/ulozeni.html')

#detail pojištěnce včetně pojištění
@app.route('/pojistenec/pojistenec/<int:id_pojistenec>')
@login_required
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
@login_required
def pojisteni():
    seznam_pojisteni = []
    pojisteni = Pojisteni.query.all()
    for poj in pojisteni:
        pojistenec = db.session.get(Pojistenci, poj.id_pojistenec)
        poj.jmeno = pojistenec.jmeno
        poj.prijmeni = pojistenec.prijmeni
        seznam_pojisteni.append(poj)
        
    page = int(request.args.get(get_page_parameter(), 1))
    per_page = 3
    total = len(seznam_pojisteni)
    pagination = Pagination(page = page,per_page = per_page, total = total, prev_label = "předchozí", next_label = "následující", css_framework='bootstrap5')
    start = (page-1) * per_page
    end = start + per_page
    zobrazeni_pojisteni = seznam_pojisteni[start:end]
    return render_template('/pojisteni/pojisteni.html', seznam_pojisteni = zobrazeni_pojisteni, pojisteni = pojisteni, pagination = pagination)

#vytváření nového pojištění
@app.route('/nove_pojisteni/<int:id_pojistenec>')
@login_required
def nove_pojisteni(id_pojistenec):
    pojistenec = db.session.get(Pojistenci, id_pojistenec)
    return render_template('/pojisteni/nove_pojisteni.html', pojistenec = pojistenec, id_pojistenec = pojistenec.id_pojistenec)

#nové pojištění
@app.route('/add_pojisteni/<int:id_pojistenec>', methods = ['POST'])
@login_required
def add_pojisteni(id_pojistenec):
    nazev = request.form['nazev']
    castka = request.form['castka']
    predmet = request.form['predmet']
    platnost_od = request.form['platnost_od']
    platnost_do = request.form['platnost_do']
    pojisteni = Pojisteni(id_pojistenec = id_pojistenec, nazev = nazev, castka = castka, predmet = predmet, platnost_od = platnost_od, platnost_do = platnost_do)
    db.session.add(pojisteni)
    db.session.commit()
    return redirect ('/pojistenec/ulozeni')

#detail pojištění
@app.route('/pojisteni/detail_pojisteni/<int:id_pojisteni>')
@login_required
def detail_pojisteni(id_pojisteni):
    pojisteni = db.session.get(Pojisteni, id_pojisteni)
    urci_obrazek = pojisteni.nazev
    obrazek = verze_obrazku(urci_obrazek)
    return render_template('/pojisteni/detail_pojisteni.html', pojisteni = pojisteni, obrazek = obrazek)

#vybrání obrázku dle zadaných kritérií
def verze_obrazku(urci_obrazek):
    if urci_obrazek == "pojištění domu":
        obrazek = "../../static/obrazky/dum.png"
    elif urci_obrazek == "pojištění auta":
        obrazek = "../../static/obrazky/auto.png"
    elif urci_obrazek == "pojištění chaty":
        obrazek = "../../static/obrazky/chata.png"
    return obrazek

#smazání pojištěnce dle jeho ID
@app.route('/pojisteni/smazani/<int:id_pojisteni>')
@login_required

def smazat_pojisteni(id_pojisteni):
    if muze_mazat():
        pojisteni = db.session.get(Pojisteni, id_pojisteni)
        db.session.delete(pojisteni)
        db.session.commit()
        return redirect('/pojistenec/smazani')
    return render_template('/ostatni/opravneni.html')

#editace pojištěnce
@app.route('/pojisteni/editace_pojisteni/<int:id_pojisteni>', methods=['GET', 'POST'])
@login_required
def editace_pojisteni(id_pojisteni):
    if muze_upravit():
        pojisteni = db.session.get(Pojisteni, id_pojisteni)
        if pojisteni:
            if request.method == 'POST':
                pojisteni.nazev = request.form['nazev']
                pojisteni.castka = request.form['castka']
                pojisteni.predmet = request.form['predmet']
                pojisteni.platnost_od = request.form['platnost_od']
                pojisteni.platnost_do = request.form['platnost_do']
                db.session.commit()
                return redirect('/pojistenec/ulozeni')
            else:
                return render_template('/pojisteni/editace_pojisteni.html', pojisteni = pojisteni)
        else:
            return "Pojištění neexistuje"
    return render_template('/ostatni/opravneni.html')

#převod na stránku události
@app.route('/udalosti.html')
@login_required
def udalosti():
    return render_template('/ostatni/udalosti.html')

#převod na stránku o aplikaci
@app.route('/oaplikaci.html')
def oaplikaci():
    return render_template('/ostatni/oaplikaci.html')

#převod na stránku pro registraci
@app.route('/nutna_registrace.html')
def nutna_registrace():
    return render_template('/ostatni/nutna_registrace.html')

#přidat novou registraci
@app.route('/registrace', methods = ['GET', 'POST'])
def registrace():
    form = RegistrationForm()
    if form.validate_on_submit():
        email_databaze = form.email.data
        generovany_hash = generate_password_hash(form.heslo.data)
        uzivatel_email = db.session.query(Uzivatel).filter_by(email = email_databaze).first()
        if uzivatel_email:
            return render_template('/ostatni/registrace_stejny_email.html', form=form)
        else:
            uzivatel = Uzivatel(jmeno = form.jmeno.data, prijmeni = form.prijmeni.data, hash_heslo = generovany_hash, email = form.email.data, id_role=int(1))
            db.session.add(uzivatel)
            db.session.commit()
            return redirect(url_for('prihlasit'))
    else:
        return render_template('ostatni/registrace.html', form=form) 

#přihlášení
@app.route('/prihlasit', methods = ['GET', 'POST'])
def prihlasit():
    form = LoginForm()
    if form.validate_on_submit():
        uzivatel = Uzivatel.query.filter_by(email=form.email.data).first()
        if uzivatel and uzivatel.kontrola_hesla(form.password.data):
            login_user(uzivatel)
            identity_changed.send(current_app._get_current_object(), identity=Identity(uzivatel.id_uzivatel))
            return redirect(url_for('index'))
        else:
            return render_template ('/ostatni/prihlasit_heslo.html', form=form)
    return render_template('/ostatni/prihlasit.html', form=form)

@app.route('/odhlasit')
def odhlasit():
    logout_user()
    session.pop('identity.name', None)
    session.pop('identity.auth_type', None)
    with app.app_context():
        identity_changed.send(app, identity=AnonymousIdentity())
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        kontrola_roli()
    app.run(debug=True)   