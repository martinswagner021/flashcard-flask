from flask import Flask, request, redirect, flash
from upload.routes import upload_bp
from cards.routes import card_bp, get_decks

app = Flask(__name__)
app.secret_key = "super-secret-key"

app.register_blueprint(upload_bp, url_prefix='/upload')
app.register_blueprint(card_bp, url_prefix='/cards')

@app.route('/')
def index():
    # Get list of all decks from the cards blueprint
    decks = get_decks()
    
    deck_links = '\n'.join([f'<li><a href="/cards/{deck}/random">{deck}</a></li>' for deck in decks])
    
    return f'''
    <h1>Welcome to the Flashcard App!</h1>
    <p>Available Decks:</p>
    <ul>
        {deck_links if decks else '<li>No decks available yet</li>'}
    </ul>
    <p>Other endpoints:</p>
    <ul>
        <li><a href="/upload">Upload a new deck (CSV file)</a></li>
        <li>Add "/random" to a deck URL to get a random card</li>
    </ul>
    '''

app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)