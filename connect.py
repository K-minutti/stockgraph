import psycopg2
from config import config

def connect():
    """Connect to database server"""
    conn = None

    try: 
        params = config()

        print('Connecting to PostgreSQL databasae...')
        conn = psycopg2.connect(**params)

        cursor = conn.cursor()
        
        print('PostgreSQL database version:')#delete
        cursor.execute('SELECT version()')

        test_statement = cursor.fetchone()
        print(test_statement)

        cursor.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

if __name__ == "__main__":
    connect()