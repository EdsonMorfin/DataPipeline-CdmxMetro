import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv
import os

load_dotenv()

def close_connection(connection):
    if (connection):
        connection.close()
        print("PostgreSQL connection is closed")

def open_connection():
    """Open postgress conection getting keys from .env file

    Returns:
        connection,curser used for postgresql operations
    """
    try:
        # Connect to an existing database
        connection = psycopg2.connect(user=os.getenv("USER"),
                                    password=os.getenv("PASSWORD"),
                                    host=os.getenv("HOST"),
                                    port=os.getenv("PORT"),
                                    database=os.getenv("DATABASE"))

        # Create a cursor to perform database operations
        cursor = connection.cursor()
        # Print PostgreSQL details
        print("PostgreSQL server information")
        print(connection.get_dsn_parameters(), "\n")
        # Executing a SQL query
        cursor.execute("SELECT version();")
        # Fetch result
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    return connection,cursor


def create_table():
    """
    Create initial table, pass if it exist
    """

    commands = (
    """
    CREATE TABLE metro_position(database_sende
        _id SERIAL PRIMARY KEY,
        id SMALLINT,
        date_updated 	TIMESTAMP,
        vehicle_id 	INT,
        vehicle_label 	INT,
        vehicle_current_status 	SMALLINT,
        position_latitude 	FLOAT(30),
        position_longitude 	FLOAT(30),
        geographic_point 	VARCHAR(50),
        position_speed 	INT,
        position_odometer 	INT,
        trip_schedule_relationship 	INT,
        trip_id 	INT,
        trip_start_date 	INT,
        trip_route_id 	INT,
        road VARCHAR(100),
        neighbourhood VARCHAR(100),
        delegation VARCHAR(100),
        state VARCHAR(100),
        postal_code VARCHAR(100),
        country VARCHAR(100)
    )
    """)
    connection = None
    try:
        connection,cursor=open_connection()
        cursor.execute("select exists(select * from information_schema.tables where table_name=%s)", ('metro_position',))
        a = cursor.fetchone()[0]
        if a != True:
            print("Table already exist")
            cursor.execute(commands)
            connection.commit()
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            close_connection(connection)

def insert_metro_values(record):
    """ Insert metro api response into postgresql table

    Args:
        record (dict): _description_
    """
    connection,cursor = open_connection()
    keys,values = '',''
    for x in record:
        if x != "_id": #Pass initial value

            record[x]= ((record[x].replace("T", " ").replace(".000Z", ""))) if (x =='date_updated') else record[x] ## convert datetime into string
            record[x] = 0 if (record[x]==None) else record[x] # convert None into 0
            keys+= x + ',' # Add a final comma
            values += "'"+str(record[x])+"'"+',' #Add ' and a final comma

    insert_query = "INSERT INTO metro_position ({}) VALUES ({})".format(keys[:-1],values[:-1]) # write the insert query and delete the last comma of key and values
    cursor.execute(insert_query)
    connection.commit()
    cursor.close()
    close_connection(connection)
