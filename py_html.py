from flask import Flask, url_for, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pojistenci.html')
def pojistenci():
    return render_template('pojistenci.html')

@app.route('/pojisteni.html')
def pojisteni():
    return render_template('pojisteni.html')

@app.route('/novy_pojistenec.html')
def novy_pojistenec():
    return render_template('novy_pojistenec.html')

@app.route('/osoba.html')
def osoba():
    return render_template('osoba.html')

if __name__ == '__main__':
    app.run(debug=True)

