from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_dance.contrib.google import make_google_blueprint, google
from flask import jsonify
from flask_mail import Mail, Message
from flask_login import login_user, logout_user, login_required



app = Flask(__name__)


app.config['SECRET_KEY'] = 'a_random_and_secure_key_1234'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Flask-Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'pyaephyothein0404@gmail.com'  
app.config['MAIL_PASSWORD'] = 'oeok rzrg esuz ionw'  
app.config['MAIL_DEFAULT_SENDER'] = ('MusicWeb', 'pyaephyothein0404@gmail.com')  


# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)




app.config["GOOGLE_OAUTH_CLIENT_ID"] = ""
app.config["GOOGLE_OAUTH_CLIENT_SECRET"] = ""
google_bp = make_google_blueprint(redirect_to="home")
app.register_blueprint(google_bp, url_prefix="/login") 



# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

# Dummy data for tracks and artists not finished yet
artists = [
    {"name": "Eminem", "image": "static/images/eminem.jpg"},
    {"name": "Metro Boomin", "image": "static/images/metroboomin.jpg"},
    {"name": "Metro Boomin", "image": "static/images/metroboomin.jpg"},

]

# Tracks data 
tracks = [
    {"id": 1, "title": "Eminem - Lose Yourself", "file": "songs/Eminem - Lose Yourself [HD].mp3", "image": "images/images6.jpg"},
    {"id": 2, "title": "Eminem - Somebody Save Me (feat. Jelly Roll)", "file": "songs/Eminem - Somebody Save Me (feat. Jelly Roll) [Official Music Video].mp3", "image": "images/images 1.jpeg"},
    {"id": 3, "title": "Future, Metro Boomin - Like That", "file": "songs/Future, Metro Boomin - Like That (Official Audio).mp3", "image": "images/images22.jpg"},
    {"id": 4, "title": "Justin Bieber - Intentions ft. Quavo", "file": "songs/Justin Bieber - Intentions (Official Video (Short Version)) ft. Quavo.mp3", "image": "images/images7.jpg"},
    {"id": 5, "title": "Kendrick Lamar - Not Like Us", "file": "songs/Kendrick Lamar - Not Like Us.mp3", "image": "images/images8.jpeg"},
    {"id": 6, "title": "Kendrick Lamar Euphoria (Drake Diss) (Lyrics).mp3", "file": "songs/Kendrick Lamar Euphoria (Drake Diss) (Lyrics).mp3", "image": "images/images9.png"},
    {"id": 7, "title": "LANY - Malibu Nights", "file": "songs/LANY - Malibu Nights (Official Music Video).mp3", "image": "images/images10.jpg"},
    {"id": 8, "title": "The Emptiness Machine.mp3", "file": "songs/The Emptiness Machine.mp3", "image": "images/images3.jpeg"},
    {"id": 9, "title": "Travis Scott - MO CITY FLEXOLOGIST", "file": "songs/LANY - Malibu Nights (Official Music Video).mp3", "image": "images/images10.jpg"},
    {"id": 10, "title": "Travis_Scott_Fein_ft.Playboi Carti .mp3", "file": "songs/Travis_Scott_Fein_ft.Playboi Carti .mp3", "image": "images/images5.jpg"},
]

# Routes
@app.route('/')
def home():
    return render_template("home.html", tracks=tracks)

@app.route('/musics')
def musics():
    return render_template("musics.html", tracks=tracks)

@app.route('/artist')
def artist():
    return render_template("artist.html", artists=artists)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        
        if email_exists:
            flash("Email is already in use.", category='error')
            return render_template('signup.html')  
        
        
        elif username_exists:
            flash("Username is already in use.", category='error')
            return render_template('signup.html')  

        
        elif password != confirm_password:
            flash('Passwords do not match', category="error")
            return render_template('signup.html')  

        
        elif len(username) < 2:
            flash('Username is too short', category='error')
            return render_template('signup.html') 

        
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(username=username, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            
            send_success_email(email, username)

            
            flash('Sign-up successful! Please log in.', category='success')
            return redirect(url_for('login'))  

    return render_template('signup.html')


def send_success_email(email, username):
    
    msg = Message(
        subject="Welcome to Your App!",
        recipients=[email],
        body=f"Hello {username},\n\nThank you for signing up for our service!\n\nBest regards,\nThe Your App Team"
    )
    mail.send(msg)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_or_username = request.form.get('email_or_username')
        password = request.form.get('password')

       
        if not email_or_username or not password:
            flash('All fields are required!', category='error')
            return render_template('login.html')

        
        user = User.query.filter((User.email == email_or_username) | (User.username == email_or_username)).first()

        
        if not user:
            flash('No account found with that email/username.', category='error')
            return render_template('login.html')

        
        if not bcrypt.check_password_hash(user.password, password):
            flash('Incorrect password.', category='error')
            return render_template('login.html')

        
        session['user_id'] = user.id
        session['username'] = user.username

        flash(f'Welcome back, {user.username}!', category='success')
        return redirect(url_for("musics"))
 

    return render_template('login.html')

@app.route('/login/google')
def google_login():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    user_info = resp.json()

    user = User.query.filter_by(email=user_info["email"]).first()
    if not user:
        user = User(username=user_info.get("name"), email=user_info["email"], password="default_password")
        db.session.add(user)
        db.session.commit()

    session['user_id'] = user.id
    session['username'] = user.username
    flash(f"Welcome, {user.username}!", category="success")
    return redirect(url_for("muiscs"))

@app.route('/users', methods=['GET'])
def view_users():
    """Route to view all users in the database."""
    users = User.query.all()
    user_data = [{"id": user.id, "username": user.username, "email": user.email} for user in users]
    return jsonify(user_data)


# API route to fetch track data 

@app.route('/api/tracks', methods=['GET'])
def get_tracks():
    return jsonify(tracks)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

