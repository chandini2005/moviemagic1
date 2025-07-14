from flask import Flask, render_template, request, redirect, session, flash, url_for
import uuid
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# ------------------------ Mock Databases ------------------------
mock_users = {}         # { email: hashed_password }
mock_bookings = []      # list of dicts for bookings

mock_movies = {
    "1": {
        "id": "1",
        "title": "Oppenheimer",
        "image": "oppenheimer.jpg",
        "rating": "8.6/10",
        "duration": "3h",
        "genre": "Biography / Drama",
        "price": 190,
        "theme": "bg-oppenheimer"
    },
    "2": {
        "id": "2",
        "title": "Avengers: Endgame",
        "image": "endgame.jpg",
        "rating": "8.4/10",
        "duration": "3h 1m",
        "genre": "Action / Sci-Fi",
        "price": 220,
        "theme": "bg-endgame"
    },
    "3": {
        "id": "3",
        "title": "Barbie",
        "image": "barbie.jpg",
        "rating": "7.1/10",
        "duration": "1h 54m",
        "genre": "Comedy / Adventure",
        "price": 180,
        "theme": "bg-barbie"
    },
    "4": {
        "id": "4",
        "title": "Jawan",
        "image": "jawan.jpg",
        "rating": "7.8/10",
        "duration": "2h 49m",
        "genre": "Action / Thriller",
        "price": 200,
        "theme": "bg-jawan"
    },
    "5": {
        "id": "5",
        "title": "Leo",
        "image": "leo.jpg",
        "rating": "8.1/10",
        "duration": "2h 44m",
        "genre": "Action / Crime / Drama",
        "price": 210,
        "theme": "bg-leo"
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()

        if email in mock_users:
            flash("Email already registered.")
            return redirect('/register')

        mock_users[email] = password
        flash("Registered successfully! Please log in.")
        return redirect('/login')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()

        if mock_users.get(email) == password:
            session['user'] = email
            flash("Login successful!")
            return redirect('/home')
        else:
            flash("Invalid credentials.")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.")
    return redirect('/login')

@app.route('/home')
def home():
    if 'user' not in session:
        return redirect('/login')
    return render_template('home.html', user=session['user'], movies=mock_movies)

@app.route('/booking')
def booking_page():
    if 'user' not in session:
        return redirect('/login')

    movie_id = request.args.get('movie')
    movie = mock_movies.get(movie_id)

    if not movie:
        flash("Movie not found.")
        return redirect('/home')

    return render_template('booking_form.html', movie=movie)

@app.route('/book', methods=['POST'])
def book_ticket():
    if 'user' not in session:
        return redirect('/login')

    movie_title = request.form['movie']
    date = request.form['date']
    time = request.form['time']
    seat = request.form['seat']

    booking = {
        'Email': session['user'],
        'Movie': movie_title,
        'Date': date,
        'Time': time,
        'Seat': seat,
        'BookingID': str(uuid.uuid4())
    }

    mock_bookings.append(booking)

    send_mock_email(
        booking['Email'],
        booking['Movie'],
        booking['Date'],
        booking['Time'],
        booking['Seat'],
        booking['BookingID']
    )

    return render_template('tickets.html', booking=booking)

@app.route('/tickets')
def tickets():
    if 'user' not in session:
        return redirect('/login')

    user_bookings = [b for b in mock_bookings if b['Email'] == session['user']]
    if not user_bookings:
        flash("No bookings found.")
        return redirect('/home')

    return render_template('tickets.html', booking=user_bookings[-1])

# ------------------------ Utilities ------------------------

def send_mock_email(email, movie, date, time, seat, booking_id):
    print(f"""
    EMAIL SENT TO: {email}
    Booking Confirmed:
    Movie: {movie}
    Date: {date}
    Time: {time}
    Seat: {seat}
    Booking ID: {booking_id}
    """)
@app.route('/set_theme/<theme>')
def set_theme(theme):
    if theme not in ['light', 'dark', 'neon']:
        flash("Invalid theme selected.")
        return redirect(url_for('home'))

    session['theme'] = theme
    flash(f"{theme.capitalize()} theme applied!")
    return redirect(request.referrer or url_for('home'))
@app.context_processor
def inject_theme():
    return {'theme': session.get('theme', 'light')}

# ------------------------ Main Entry ------------------------

if __name__ == '__main__':
    app.run(debug=True)
