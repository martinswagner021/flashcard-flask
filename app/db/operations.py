from flask import flash, redirect, request
import sqlalchemy as sa
import csv
from io import StringIO
from .middleware.handle_operations import check_table_exists
from db.connect import engine

def create_deck(file, table_name):
    metadata = sa.MetaData()

    if check_table_exists(table_name):
        flash(f"Table {table_name} already exists.")
        return redirect(request.url)
        
    # Create table dynamically using the headers
    table = sa.Table(table_name, metadata,
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('Front', sa.String(255)),
        sa.Column('Back', sa.String(255)),
        sa.Column('Plus', sa.String(255))
    )

    # Create the table in the database
    metadata.create_all(engine)
    
    data = file.read()
    text_stream = StringIO(data.decode('utf-8'))

    reader = csv.reader(text_stream, delimiter=',')
    with engine.begin() as conn:
        for row in reader:
            conn.execute(table.insert().values({
                'Front': row[0],
                'Back': row[1],
                'Plus': row[2]
            }))

def find_many_cards(table_name):
    metadata = sa.MetaData()
    table = sa.Table(table_name, metadata, autoload_with=engine)

    with engine.connect() as conn:
        result = conn.execute(
            sa.select(table.c["Front"], table.c["Back"], table.c["Plus"])
        ).mappings()
        cards = [
            {
                "Front": row["Front"],
                "Back": row["Back"],
                "Plus": row["Plus"]
            }
            for row in result
        ]

    return cards

def find_one_card(table_name, card_id):
    metadata = sa.MetaData()
    table = sa.Table(table_name, metadata, autoload_with=engine)

    with engine.connect() as conn:
        result = conn.execute(
            sa.select(table).where(table.c.id == card_id)
        ).mappings().fetchone()

    if result is None:
        return None

    return {
        "Front": result["Front"],
        "Back": result["Back"],
        "Plus": result["Plus"]
    }

def find_many_decks():
    with engine.connect() as conn:
        result = conn.execute(
            sa.text("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                  AND table_type = 'BASE TABLE'
            """)
        ).mappings()

        decks = [row["table_name"] for row in result]
    print(decks)
    return decks