import psycopg2
from psycopg2 import OperationalError
from  models.models import create_tables

def create_connection():
    connection = None
    try:
        connection = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='password',
            database='locate_parking',
            port='5432' 
            )
            

        create_tables(connection)
        
    except OperationalError as error:
        print(f"The error {error} occurred")
    
    return connection
