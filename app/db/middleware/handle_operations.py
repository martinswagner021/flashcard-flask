from sqlalchemy import inspect
from db.connect import engine

def check_table_exists(table_name):
    """
    Check if a table exists in the database.
    
    :param engine: SQLAlchemy engine object
    :param table_name: Name of the table to check
    :return: True if table exists, False otherwise
    """
    inspector = inspect(engine)
    if table_name in inspector.get_table_names():
        return True
    return False