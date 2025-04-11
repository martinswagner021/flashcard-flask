from flask import Blueprint, request, redirect, flash, jsonify
from db.operations import create_deck, find_many_cards, find_one_card, find_many_decks
import random

card_bp = Blueprint('cards', __name__)

@card_bp.route('/<deck>', methods=['GET'])
def get_cards(deck):
    return jsonify(find_many_cards(deck))

@card_bp.route('/<deck>/<int:id>', methods=['GET'])
def get_specific_card(deck, id):
    return jsonify(find_one_card(deck, id))

@card_bp.route('/<deck>/random', methods=['GET'])
def get_random_card(deck):
    cards = find_many_cards(deck)
    random_card = random.choice(cards) if cards else None
    return f'''
        <h2>Deck: {deck}</h2>
        <p><strong>Front:</strong> {random_card['Front']}</p>
        <p><strong>Back:</strong> {random_card['Back']}</p>
        <p><strong>Part of Speech:</strong> {random_card['Plus']}</p>
        <a href="/cards/{deck}/random">Next Random</a> | <a href="/">Back to Home</a>
    '''

def get_decks():
    return find_many_decks()  # Assuming fetch_all_tables() exists in db.operations
    
# @app.route('/test/<name>/<int:age>')
# def test_name_age(name, age):
#     return f'This is a test endpoint for {name}, who is {age} years old!'