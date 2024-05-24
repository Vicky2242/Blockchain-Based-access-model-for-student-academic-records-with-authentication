from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import hashlib

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # SQLite database
db = SQLAlchemy(app)
app.secret_key='your_secret_key'

class Institution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    institution_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __int__(self,id,institution_name,address,contact_number,username,password):
        self.id=id
        self.institution_name=institution_name
        self.address=address
        self.contact_number=contact_number
        self.username=username
        self.password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode("utf-8"))
    
with app.app_context():
    db.create_all()


# Serve static files (CSS and JS) from the 'static' directory
app.static_folder = 'static'

users = [
    {'username': 'admin', 'password': 'admin123'},
    {'username': 'institution1', 'password': 'pass123'},
]

# Homepage route
@app.route('/')
def index():
    return render_template('index.html')

def hash_function(input_string):
    # Create a new SHA-256 hash object
    hash_object = hashlib.sha256()

    # Update the hash object with the input string
    hash_object.update(input_string.encode())

    # Get the hexadecimal representation of the hashed value
    hashed_value = hash_object.hexdigest()

    return hashed_value

  
@app.route('/institution/login', methods=['GET', 'POST'])
def institution_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        institution = Institution.query.filter_by(username=username).first()

        if institution and institution.check_password(password):
            # Store institution details in session
            session['institution_id'] = institution.id
            session['institution_name'] = institution.name
            session['address'] = institution.address
            session['contact_number'] = institution.contact_number
            session['username'] = institution.username
            session['password'] = institution.password
            return redirect('/dashboard')
        else:
            return render_template('institution_login.html', error='Invalid username or password')

    return render_template('institution_login.html')

    

@app.route('/institution/dashboard')
def institution_dashboard():
    if session['institution_name']:
      return render_template('institution_dashboard.html')
    
    return redirect('/institution/login')

@app.route('/institution/signup', methods=['GET', 'POST'])
def institution_signup():

    if request.method == 'POST':
        institution_name=request.form['institution_name']
        address=request.form['address']
        contact_number=request.form['contact_number']
        username=request.form['username']
        password=request.form['password']

        new_institution=Institution(institution_name=institution_name,address=address,contact_number=contact_number,username=username,password=password)
        db.session.add(new_institution)
        db.session.commit()
        return redirect('/institution/login')

    return render_template('institution_signup.html') 

@app.route('/authority/login')
def authority_login():
    # Add authentication logic here
    return render_template('authority_login.html')

@app.route('/authority/signup')
def authority_signup():
    return render_template('authority_signup.html')  # Render the HTML template for authority signup


# Student Login Routes
@app.route('/student/login')
def student_login():
    # Add authentication logic here
    return render_template('student_login.html')

if __name__ == '__main__':
    app.run(debug=True)
