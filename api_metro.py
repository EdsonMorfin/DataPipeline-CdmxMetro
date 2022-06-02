from datetime import date, datetime
from textwrap import indent
from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI
import psycopg2
from psycopg2 import Error
from psycopg2 import sql
from dotenv import load_dotenv
import json
import os

app = FastAPI()
load_dotenv()

def close_connection(connection):
    if (connection):
        connection.close()
        print("PostgreSQL connection is closed")

def open_connection():
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


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/test")
def get_unidades():
    connection,cursor = open_connection()
    get_all_unidades = "SELECT * FROM metro_position LIMIT 5"
    cursor.execute(get_all_unidades)
    colnames = [desc[0] for desc in cursor.description]
    #colnames = json.dumps(colnames) # replace single quote with double quote
    unidades = cursor.fetchall()
    cursor.close()
    close_connection(connection)
    return get_json_response(colnames,unidades)

def convert_datetime(datetime):
    return datetime.strftime("%m/%d/%Y %H:%M:%S")

def get_json_response(column_names,query_response):
    api_response = '{ "response":['
    for response in query_response:
        response = list(response)
        response_dic = dict(zip(column_names,response)) # append two elements in a dict
        if 'date_updated' in response_dic:
            response_dic['date_updated'] = convert_datetime(response_dic['date_updated']) #format datetime
        api_response += json.dumps(response_dic)+','
    api_response = api_response[:-1] + ']}'
    return json.loads(api_response)


get_unidades()
