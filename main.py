from flask import Flask, render_template, flash, request, url_for, redirect, session, g, jsonify
from flask_sqlalchemy import SQLAlchemy 
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, logout_user, current_user, login_user
from flask_login import login_manager
from functools import wraps
import json
from authlib.integrations.flask_client import OAuth


old_email = ''

app = Flask(__name__)



#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///TroTrousers.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fares.db'
app.config['SQLALCHEMY_BINDS'] = {
    'User':      'sqlite:///TroTrousers.db',
    'fares':      'sqlite:///fares.db',
    'userfares':  'sqlite:///userfares.db',
    'kumasifares':  'sqlite:///KumasiFaresdb.db',
    'obuasifares':  'sqlite:///ObuasiFaresdb.db',
    'accrafares':  'sqlite:///AccraFaresdb.db',
    'sefwifares':  'sqlite:///SefwiFaresdb.db',
    'nsawamfares':  'sqlite:///NsawamFaresdb.db'
}
db = SQLAlchemy(app)
app.secret_key = 'secretkey'
oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id='0HQbdZewdUuIHCBfLqPxtHnk5JxVXmbl',
    client_secret='pKLSq8968hvDSgZN0MM_mZ-5PmjzEsdwzmnUpM4drLzbfz7DlmbCpLvLawQ-dw55',
    api_base_url='https://111uuuccciii.us.auth0.com',
    access_token_url='https://111uuuccciii.us.auth0.com/oauth/token',
    authorize_url='https://111uuuccciii.us.auth0.com/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)


class User(db.Model):
    __bind_key__ = 'User' 
    id = db.Column(db.Integer, unique=True, primary_key=True)
    email = db.Column(db.String(30), unique=True, nullable=False)
    fname = db.Column(db.String(15), unique=False, nullable=False)
    lname = db.Column(db.String(15), unique=False, nullable=False)
    gender = db.Column(db.String(7), unique=False, nullable=False)
    dob = db.Column(db.String(10), unique=False, nullable=False)
    passhash = db.Column(db.String(180), unique=False, nullable=False)

    #def __repr__(self):
        #return 'User ' + str(self.id)

class fares(db.Model):
    __bind_key__ = 'fares'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    srcdest = db.Column(db.String(50), unique=False, nullable=False)
    fare = db.Column(db.String(15), unique=False, nullable=False)
    transit = db.Column(db.String(15), unique=False, nullable=False)

class userfares(db.Model):
    __bind_key__ = 'userfares'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    fullname = db.Column(db.String(50), unique=False, nullable=False)
    srcdest = db.Column(db.String(50), unique=False, nullable=False)
    fare = db.Column(db.String(15), unique=False, nullable=False)
    transit = db.Column(db.String(15), unique=False, nullable=False)


class kumasifares(db.Model):
    __bind_key__ = 'kumasifares'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    srcdest = db.Column(db.String(50), unique=False, nullable=False)
    fare = db.Column(db.String(15), unique=False, nullable=False)
    transit = db.Column(db.String(15), unique=False, nullable=False)

class sefwifares(db.Model):
    __bind_key__ = 'sefwifares'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    srcdest = db.Column(db.String(50), unique=False, nullable=False)
    fare = db.Column(db.String(15), unique=False, nullable=False)
    transit = db.Column(db.String(15), unique=False, nullable=False)

class obuasifares(db.Model):
    __bind_key__ = 'obuasifares'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    srcdest = db.Column(db.String(50), unique=False, nullable=False)
    fare = db.Column(db.String(15), unique=False, nullable=False)
    transit = db.Column(db.String(15), unique=False, nullable=False)


class accrafares(db.Model):
    __bind_key__ = 'accrafares'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    srcdest = db.Column(db.String(50), unique=False, nullable=False)
    fare = db.Column(db.String(15), unique=False, nullable=False)
    transit = db.Column(db.String(15), unique=False, nullable=False)

class nsawamfares(db.Model):
    __bind_key__ = 'nsawamfares'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    srcdest = db.Column(db.String(50), unique=False, nullable=False)
    fare = db.Column(db.String(15), unique=False, nullable=False)
    transit = db.Column(db.String(15), unique=False, nullable=False)

def __init__(fares, srcdest, fare):
    fares.srcdest = srcdest
    fares.fare = fare
    fares.transit = transit

def ensure_logged_in(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not (session.get('user_id') or session.get('profile')):
            flash("Please log in first")
            return redirect(url_for('login'))
        return fn(*args, **kwargs)
    return wrapper

@app.before_request
def before_request():
    if 'user_id' in session:
        user = User.query.filter_by(id = session['user_id']).first()
        g.userfname = user
    elif 'profile' in session:
        user = session['profile']
        g.username = user

@app.route('/')
def home():
    if request.method == "GET":
	    languages = ["Afriwa", "Ashiaman Main Station", "Tema Motorway, Rabout", "Ashiaman Traffic Light", "Accra Mall", "Shangrila", "MAdina", "Madina", "Afenyi", "Tema Comm 9 to 1", "Manso", "Zeenu", "School Junction", "Falcon", "Second Step", "New Junction", "Achimota", "Dowenya", "Methodist", "Police Station", "Barrier", "Dankwa First", "Prampram", "Tema, Comm.25", "Savanna", "Estate Junction", "Freezone", "Mateheko", "Afarawa", "Michel Camp", "Newton junction", "Afenya", "Teshie", "Tsuibleblo", "Nunga", "Lapaz", "Kosoa", "Lashibi", "Tema, Comm18", "KFC", "Lashibi Tx", "Nima", "Circle", "Adukurom", "Akropong", "Abum", "Begoro", "Ho", "Hohoe", "Dzodza", "Somunya", "Kpando", "Keta", "Kadjebi", "Akosombo", "Oyidi", "Dodowa", "Labadi", "Burma Camp", "Masalakye Dodowa", "Masalakye Oyibi", "Kumasi", "Nkwakwa", "Koforidua", "Kgeso", "Aflao", "Sogakope", "Ada", "Nungua", "Asamang Kese", "Oda", "Suhum", "Nsawam", "Latex Oasis", "Latex Oasis School Junction", "Ashiaman", "Botwe", "Tema", "Atadaka", "Lebanon", "Spintex", "Pekyi 1", "Pekyi 2", "Asamang", "County Hospital", "Kahuro", "Dompoase Aprabo", "Bokro", "Asante Bekwai", "Kokofu", "Ownien", "Kutenase", "Opoku Ware School", "Star Junction", "Tech Junction", "Daban", "Sokoban", "Ampayoo", "Krofrom Sokoban Road", "Ampabame(Sokoban)", "Esreso", "Krofrom (New Tafo)", "Suame Rounabout", "Kumasi Airport Rounabout", "Dichems", "Dichemso", "Atonsu, High School", "Atonsu,Monanco", "Atonsu,Agogo", "Bofoyedur", "Feyiase Kokoben", "Kwadaso IPT", "Susuanso", "Kuwait", "Aprabo", "Appiadu", "Appiadu Kokoben", "Donyinah", "Ayeduase", "Adwaase New site", "Boadi", "Kumasi Aiport Roundabout", "Suame, Magazine", "Ramseyer", "Nahinso", "Aboahu", "Asuofia", "A Line", "F Line", "St Abed", "Abono", "Mayanka", "Atonsu, Ako Junction", "Prestia", "Takoradi", "Boodie", "Bogoso", "Bodie", "Wasa Akropong", "Dedieso", "Gyapa", "Nkonya", "Anyanfore", "Bontomoroso", "Adobewora", "Sabronum", "Nyamebekyere Camp", "Adukrom", "Brepro", "Aponaponso", "Bokuruwa", "Esieinkyem", "Amoakokrom", "Yard", "Nsuterm", "Pokuase", "Bonsukrom", "Boahenekwaa", "Pataukro", "Amoaya", "Besease", "Bokabo", "Datano", "Adubia", "Agoroyesum", "Totokrom", "Akyekyekrom", "Ahutoakrom", "Manso Nkwanta", "Manso Abure", "Manso Atwere", "Abobaso", "Yawkese", "Kamiaago", "Kwatereso", "Nyamebekyere", "Ayebikrom", "Offinso", "Sankore", "Agona Wasa", "Ankaasie", "Dominase Nkwanta", "Jadua Kese", "Tepa", "Anyinasuso", "Ahafo Kenyase", "Awidiem", "Acherensua", "Bonsu Nkwanta", "Asawinso", "Techiman", "Nkronsa", "Wenchi", "Koforidua", "Nkwakwa", "Kintampo", "Akomadam", "Goaso", "New Edubiase", "Fomena", "Accra", "Bamfo Juntion", "Ayimi", "Asiyon", "Bomso", "Nkoransah", "Stadium", "Ahodwo", "Patasi", "Edwanase", "Asuoyeboah", "Kwamo", "Fumesua", "Asuofua", "Amanfrom", "Ohwim", "Atafoa", "Akoko Spears", "County Hospital (Abrepo)", "Kumasi Girls School", "Abrepo", "Bohyen", "Bohyen Ampame", "Islamic SHS", "Fawoade", "A line", "F line", "Mampongteng", "Anwomaso", "Odum", "Kentinkrono", "Jachie", "Jachie Pramso", "Fumesua Kyirekrom", "Apromase", "Domeabra", "Nana Ho", "Asawase", "Asokwa", "Ahinsan Market", "Aputuogya", "Anyinam Kotwi", "Asante Akyem, Agogo", "Konongo", "Nkawkaw", "Kumawu", "Asenua", "Ahwia", "Medoma", "Fawode", "Mamponteng", "Ntonsu", "Aboaso", "Kronom", "Maakro", "Krofrom", "Moshie Zongo", "Buokrom", "Sepe", "Buokrom South", "F-Line", "Nana Appiah", "Old Ash FM", "Pankrono", "Adabraka", "Aprade", "Parkoso", "Mampenase", "Kenyase", "Estate Junction", "Duase", "Kumasi Airport", "Antoa", "Bonwire", "Achiase", "Kole", "Obofour", "Gawo Junction", "Mr Mote", "Komfo Anokye Hospital", "Kwadaso", "Edwenase", "Asafo Market", "Asafo Labour", "Ejisu", "Effiduase", "Konogo", "Juaso", "Brewery", "Santasi, Anyinam", "Brofoyedu", "Pekyi No1", "Domenase", "Agyemasu", "Kroform", "Kumasi Airport Roundabout", "Aboabo", "Emina", "Aboude TUC", "Dakwadwom", "BarNas", "Ahodwo Roundabout", "+2Pub", "Ahodwo Melcom", "Ahodwo Station", "Kaase", "Guinness Brewery", "Ahinsan,Bus Stop", "Santasi Roundabout", "Anwia Nkwanta", "Krofrom(New Tafo)", "Suame Roundabout", "Abrepo Junction", "Atonsu, Bokro Ako Junction", "Atonsu, Bokro Last Stop", "Baba Yara Sports Stadium", "Afful Nkwanta", "Oforikrom", "Susuaso", "Amakom", "Asafo, Labour", "Atasomanso", "Kotei", "Anloga Junction", "Deduako", "Atonsu, High Scool", "Bantama", "Tafo", "Gyinase", "Atonsu", "TUC", "Atinga Junction", "Atonsu, Monanco", "Atonsu, Agogo", "Atonsu, High School Junction", "Bekwai Roundabout", "Ahiaw Nkwanta", "Foese Kokoben", "Dominase", "Ahenema Kokoben", "Brofoyedur", "Kotwi", "Nkronsah", "Trede", "Pekyi N01", "Pekyi N02", "Ahwia Nkwanta", "Adjemasu", "Bekwai", "Kwadwo", "IPT", "Asuoyeboa", "Tanoso", "Kumasi UEW", "Abuakwa", "Ahinsan", "Kumasi City Mall", "Asafo", "Santasi", "Atonsu Agogo", "Sofoline", "Tech", "Kejetia Roman Hill", "Kejetia, Roman Hill", "Kejetia", "Kejetia, Dr Mensah", "Adum", "Nsawam", "Nsawam Market", "Madina", "Aburi", "Circle", "Achimota", "Pokrom", "Amansaman", "Pokuase", "Adoagyiri", "Djankrom", "Prison Junction", "Avaga", "Nkyinikyini", "Oparekrom", "Aburi Junction", "Pakro", "Calvary Quaters", "Main Station", "Mobil", "Asante Akura", "Govt.Hospital", "Nurses Quaters", "Atsikope", "Fumso", "Asokwa Junction", "Fosu", "Anwaso", "New Edubiase", "Hwrom Asi", "Akwansrem", "Assin Fosu", "Praso", "Mankessim", "Agona Swedru", "Adamso", "Amponyase", "Amonyase", "Asoufenaso", "Ayaase", "Amankyem", "Dwafo", "Sikaman", "Befenase", "Yawaso", "Amoako", "Gromesa", "Bogoso", "Cape Coast", "Kofikrom", "Guasu", "Sam Jonah", "Bruno", "Danquah", "Precious Estate", "Anyinam", "Nyameso", "Nyamebekyere", "Kyekyewere", "Nana Ponko", "Nyankomasu", "Adansi Domeabra", "Kwabenakwa", "Asonkore", "Pomposo", "Akaporiso", "Akapriso", "Abusco", "BossMan", "Brahabebome", "Boefe", "Tutuka", "Kwabrafoso", "Anyimedukuro", "Wawasi", "Central Market(GPRTU)", "Horsey Park", "Dadieso", "Bawakrom", "Asafo", "Accra", "Kumasi", "Wiawso", "Bibiani", "Bodi", "Asawinso", "Dadiaso", "Akontombra"]
		
	    return render_template("index.html", languages=languages)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None

    if request.method == 'POST':
        new_email = request.form['email']
        new_fname = request.form['fname']
        new_lname = request.form['lname']
        new_gender = request.form['gender']
        new_dob = request.form['dob']
        new_pass = request.form['repassword']

        passcheck = request.form['password']
        user = User.query.filter_by(email=new_email).first()

        if user:
            error = 'Email already exists'
        elif new_email == '':
            error = 'Email cannot be blank!'
        elif new_fname == '':
            error = 'You must provide a first name!'
        elif new_lname == '':
            error = 'You must provide a Last name!'
        elif new_dob == '':
            error = 'Please Enter a Date of Birth!'
        elif new_pass != passcheck:
            error = 'Passwords do not match. Please try again!'
        else:
            hash_new_pass = generate_password_hash(new_pass, method='sha256')
            new_user = User(email=new_email, fname=new_fname, lname=new_lname, gender=new_gender, dob=new_dob, passhash=hash_new_pass)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created Successfully. You can login now')
            return redirect(url_for('login'))
    return render_template('signup.html', error = error)

@app.route('/login' , methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)
        session.pop('profile', None)
        old_email = request.form['email']
        passcheck = request.form['password']
        email = User.query.filter_by(email = old_email).first()
        if not email or not check_password_hash(email.passhash, passcheck):
            flash('Please check your login details and try again.')
            return redirect(url_for('login'))
        else:
            session['user_id'] = email.id
            flash('Welcome '+ old_email+'!')
            return redirect(url_for('member'))

    return render_template('login.html')

@app.route('/search' , methods=['POST'])
def search():
    
    languages = ["Afriwa", "Ashiaman Main Station", "Tema Motorway, Rabout", "Ashiaman Traffic Light", "Accra Mall", "Shangrila", "MAdina", "Madina", "Afenyi", "Tema Comm 9 to 1", "Manso", "Zeenu", "School Junction", "Falcon", "Second Step", "New Junction", "Achimota", "Dowenya", "Methodist", "Police Station", "Barrier", "Dankwa First", "Prampram", "Tema, Comm.25", "Savanna", "Estate Junction", "Freezone", "Mateheko", "Afarawa", "Michel Camp", "Newton junction", "Afenya", "Teshie", "Tsuibleblo", "Nunga", "Lapaz", "Kosoa", "Lashibi", "Tema, Comm18", "KFC", "Lashibi Tx", "Nima", "Circle", "Adukurom", "Akropong", "Abum", "Begoro", "Ho", "Hohoe", "Dzodza", "Somunya", "Kpando", "Keta", "Kadjebi", "Akosombo", "Oyidi", "Dodowa", "Labadi", "Burma Camp", "Masalakye Dodowa", "Masalakye Oyibi", "Kumasi", "Nkwakwa", "Koforidua", "Kgeso", "Aflao", "Sogakope", "Ada", "Nungua", "Asamang Kese", "Oda", "Suhum", "Nsawam", "Latex Oasis", "Latex Oasis School Junction", "Ashiaman", "Botwe", "Tema", "Atadaka", "Lebanon", "Spintex", "Pekyi 1", "Pekyi 2", "Asamang", "County Hospital", "Kahuro", "Dompoase Aprabo", "Bokro", "Asante Bekwai", "Kokofu", "Ownien", "Kutenase", "Opoku Ware School", "Star Junction", "Tech Junction", "Daban", "Sokoban", "Ampayoo", "Krofrom Sokoban Road", "Ampabame(Sokoban)", "Esreso", "Krofrom (New Tafo)", "Suame Rounabout", "Kumasi Airport Rounabout", "Dichems", "Dichemso", "Atonsu, High School", "Atonsu,Monanco", "Atonsu,Agogo", "Bofoyedur", "Feyiase Kokoben", "Kwadaso IPT", "Susuanso", "Kuwait", "Aprabo", "Appiadu", "Appiadu Kokoben", "Donyinah", "Ayeduase", "Adwaase New site", "Boadi", "Kumasi Aiport Roundabout", "Suame, Magazine", "Ramseyer", "Nahinso", "Aboahu", "Asuofia", "A Line", "F Line", "St Abed", "Abono", "Mayanka", "Atonsu, Ako Junction", "Prestia", "Takoradi", "Boodie", "Bogoso", "Bodie", "Wasa Akropong", "Dedieso", "Gyapa", "Nkonya", "Anyanfore", "Bontomoroso", "Adobewora", "Sabronum", "Nyamebekyere Camp", "Adukrom", "Brepro", "Aponaponso", "Bokuruwa", "Esieinkyem", "Amoakokrom", "Yard", "Nsuterm", "Pokuase", "Bonsukrom", "Boahenekwaa", "Pataukro", "Amoaya", "Besease", "Bokabo", "Datano", "Adubia", "Agoroyesum", "Totokrom", "Akyekyekrom", "Ahutoakrom", "Manso Nkwanta", "Manso Abure", "Manso Atwere", "Abobaso", "Yawkese", "Kamiaago", "Kwatereso", "Nyamebekyere", "Ayebikrom", "Offinso", "Sankore", "Agona Wasa", "Ankaasie", "Dominase Nkwanta", "Jadua Kese", "Tepa", "Anyinasuso", "Ahafo Kenyase", "Awidiem", "Acherensua", "Bonsu Nkwanta", "Asawinso", "Techiman", "Nkronsa", "Wenchi", "Koforidua", "Nkwakwa", "Kintampo", "Akomadam", "Goaso", "New Edubiase", "Fomena", "Accra", "Bamfo Juntion", "Ayimi", "Asiyon", "Bomso", "Nkoransah", "Stadium", "Ahodwo", "Patasi", "Edwanase", "Asuoyeboah", "Kwamo", "Fumesua", "Asuofua", "Amanfrom", "Ohwim", "Atafoa", "Akoko Spears", "County Hospital (Abrepo)", "Kumasi Girls School", "Abrepo", "Bohyen", "Bohyen Ampame", "Islamic SHS", "Fawoade", "A line", "F line", "Mampongteng", "Anwomaso", "Odum", "Kentinkrono", "Jachie", "Jachie Pramso", "Fumesua Kyirekrom", "Apromase", "Domeabra", "Nana Ho", "Asawase", "Asokwa", "Ahinsan Market", "Aputuogya", "Anyinam Kotwi", "Asante Akyem, Agogo", "Konongo", "Nkawkaw", "Kumawu", "Asenua", "Ahwia", "Medoma", "Fawode", "Mamponteng", "Ntonsu", "Aboaso", "Kronom", "Maakro", "Krofrom", "Moshie Zongo", "Buokrom", "Sepe", "Buokrom South", "F-Line", "Nana Appiah", "Old Ash FM", "Pankrono", "Adabraka", "Aprade", "Parkoso", "Mampenase", "Kenyase", "Estate Junction", "Duase", "Kumasi Airport", "Antoa", "Bonwire", "Achiase", "Kole", "Obofour", "Gawo Junction", "Mr Mote", "Komfo Anokye Hospital", "Kwadaso", "Edwenase", "Asafo Market", "Asafo Labour", "Ejisu", "Effiduase", "Konogo", "Juaso", "Brewery", "Santasi, Anyinam", "Brofoyedu", "Pekyi No1", "Domenase", "Agyemasu", "Kroform", "Kumasi Airport Roundabout", "Aboabo", "Emina", "Aboude TUC", "Dakwadwom", "BarNas", "Ahodwo Roundabout", "+2Pub", "Ahodwo Melcom", "Ahodwo Station", "Kaase", "Guinness Brewery", "Ahinsan,Bus Stop", "Santasi Roundabout", "Anwia Nkwanta", "Krofrom(New Tafo)", "Suame Roundabout", "Abrepo Junction", "Atonsu, Bokro Ako Junction", "Atonsu, Bokro Last Stop", "Baba Yara Sports Stadium", "Afful Nkwanta", "Oforikrom", "Susuaso", "Amakom", "Asafo, Labour", "Atasomanso", "Kotei", "Anloga Junction", "Deduako", "Atonsu, High Scool", "Bantama", "Tafo", "Gyinase", "Atonsu", "TUC", "Atinga Junction", "Atonsu, Monanco", "Atonsu, Agogo", "Atonsu, High School Junction", "Bekwai Roundabout", "Ahiaw Nkwanta", "Foese Kokoben", "Dominase", "Ahenema Kokoben", "Brofoyedur", "Kotwi", "Nkronsah", "Trede", "Pekyi N01", "Pekyi N02", "Ahwia Nkwanta", "Adjemasu", "Bekwai", "Kwadwo", "IPT", "Asuoyeboa", "Tanoso", "Kumasi UEW", "Abuakwa", "Ahinsan", "Kumasi City Mall", "Asafo", "Santasi", "Atonsu Agogo", "Sofoline", "Tech", "Kejetia Roman Hill", "Kejetia, Roman Hill", "Kejetia", "Kejetia, Dr Mensah", "Adum", "Nsawam", "Nsawam Market", "Madina", "Aburi", "Circle", "Achimota", "Pokrom", "Amansaman", "Pokuase", "Adoagyiri", "Djankrom", "Prison Junction", "Avaga", "Nkyinikyini", "Oparekrom", "Aburi Junction", "Pakro", "Calvary Quaters", "Main Station", "Mobil", "Asante Akura", "Govt.Hospital", "Nurses Quaters", "Atsikope", "Fumso", "Asokwa Junction", "Fosu", "Anwaso", "New Edubiase", "Hwrom Asi", "Akwansrem", "Assin Fosu", "Praso", "Mankessim", "Agona Swedru", "Adamso", "Amponyase", "Amonyase", "Asoufenaso", "Ayaase", "Amankyem", "Dwafo", "Sikaman", "Befenase", "Yawaso", "Amoako", "Gromesa", "Bogoso", "Cape Coast", "Kofikrom", "Guasu", "Sam Jonah", "Bruno", "Danquah", "Precious Estate", "Anyinam", "Nyameso", "Nyamebekyere", "Kyekyewere", "Nana Ponko", "Nyankomasu", "Adansi Domeabra", "Kwabenakwa", "Asonkore", "Pomposo", "Akaporiso", "Akapriso", "Abusco", "BossMan", "Brahabebome", "Boefe", "Tutuka", "Kwabrafoso", "Anyimedukuro", "Wawasi", "Central Market(GPRTU)", "Horsey Park", "Dadieso", "Bawakrom", "Asafo", "Accra", "Kumasi", "Wiawso", "Bibiani", "Bodi", "Asawinso", "Dadiaso", "Akontombra"]

    src = request.form['src']
    dest = request.form['dest']
    prov = request.form['prov']

    if src == dest:
        same = 'You chose the same location twice!'
        print(same)
        return render_template('index.html', same=same, languages=languages)
    
    else:

        if prov == 'Accra':
            database = accrafares

        elif prov == 'Kumasi':
            database = kumasifares
        
        elif prov == 'Obuasi':
            database = obuasifares

        elif prov == 'Nsawam':
            database = nsawamfares

        elif prov == 'Sefwi':
            database = sefwifares 

        un = str('_')
        srcdest = str(src)+str(un)+str(dest)
        check = database.query.filter_by(srcdest = srcdest).all()

        if check != []:
            print(check)
            return render_template('index.html', 
                                                singlefare = check , 
                                                src=src, 
                                                dest=dest, languages=languages )

        else:
            srcdest = str(dest)+str(un)+str(src)
            check = database.query.filter_by(srcdest = srcdest).all()
            if check != []:
                print(check)
                return render_template('index.html', 
                                                singlefare = check , 
                                                src=src, 
                                                dest=dest, languages=languages )
            else:
                same = 'Sorry, the fare you are looking for cannot be found'
                print(same)
                return render_template('index.html', same=same, languages=languages)

@app.route('/searchm' , methods=['POST'])
@ensure_logged_in
def searchm():
    src = request.form['src']
    dest = request.form['dest']
    if src == dest:
        same = 'You chose the same location twice!'
        return render_template('member.html', same=same)
    else:
        un = str('_')
        srcdest = str(src)+str(un)+str(dest)
        check = fares.query.filter_by(srcdest = srcdest).all()

    if check != []:
        return render_template('member.html', 
                                            singlefare = check , 
                                            src=src, 
                                            dest=dest )
    #print(check)
    else:
        srcdest = str(dest)+str(un)+str(src)
        check = fares.query.filter_by(srcdest = srcdest).all()
        if check != []:
            return render_template('member.html', 
                                            singlefare = check , 
                                            src=src, 
                                            dest=dest )
        else:
            same = 'Sorry, the fare you are looking for cannot be found'
            return render_template('member.html', same=same)

@app.route('/member')
@ensure_logged_in
def member():
    email = dict(session).get('email', None)
    return render_template('member.html', email=email)

@app.route('/company')
def company():
    return render_template('about.html')

@app.route('/report')
@ensure_logged_in
def report():
    return render_template('report.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/suggest', methods=['GET', 'POST'])
@ensure_logged_in
def suggest():
    if request.method == 'POST':
        fullname = request.form['fullname']
        src = request.form['src']
        dest = request.form['dest']
        fare = request.form['fare']
        transit = request.form['transit']
        un = str('_')
        srcdest = str(src)+str(un)+str(dest)
        new_fare = userfares(fullname=fullname, srcdest=srcdest, fare=fare, transit=transit)
        db.session.add(new_fare)
        db.session.commit()
        flash('Your fare has been submitted and will be Reviewed!')
        return redirect(url_for('member'))
    return render_template('suggest.html')



@app.route('/logout')
@ensure_logged_in
def logout():
  session.pop('user_id', None)
  flash('You have been signed out.')
  return redirect(url_for('login'))

@app.route('/loginG')
def loginG():
    session.pop('user_id', None)
    session.pop('profile', None)
    return auth0.authorize_redirect(redirect_uri='http://127.0.0.1:5000/authorize')

@app.route('/authorize')
def authorize():
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    # Store the user information in flask session.
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    print('here')
    print('here')
    print('here')
    print('here')
    print('here')
    print('here')
    print(session)
    return redirect('/member')

@app.route('/contact')
def contact():
   return render_template('contact.html')

@app.route('/faq')
def faq():
   return render_template('faq.html')

@app.route('/buysell')
def buy():
   return render_template('buysell.html')


if __name__ == "__main__":
    app.run(debug=True) 
