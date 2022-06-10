from sqlite3 import Timestamp
from fastapi import FastAPI
from dotenv import load_dotenv
import json
from app.utils.database_sender import open_connection,close_connection
app = FastAPI()
load_dotenv()


@app.get("/")
def read_root():
    return {"Hola_Soy": "EdsonPaulMorfin"}


@app.get("/units")
def get_unidades():
    query_request = """
                        SELECT * FROM metro_position
                        ORDER BY
                            DATE(date_updated)=DATE(NOW()) DESC,
                            DATE(date_updated)<DATE(NOW()) DESC,
                            DATE(date_updated)>DATE(NOW()) ASC
                        """
    column_names,query_response = get_query_response(query_request)
    return get_json_response(column_names,query_response)


@app.get("/unit/{id}") # by id
async def get_unidades(id):
    query_request = """
                        SELECT * FROM metro_position
                        WHERE
                            vehicle_id = {}
                        ORDER BY
                            DATE(date_updated)=DATE(NOW()) DESC,
                            DATE(date_updated)<DATE(NOW()) DESC,
                            DATE(date_updated)>DATE(NOW()) ASC
                        """.format(id)
    column_names,query_response = get_query_response(query_request)
    return get_json_response(column_names,query_response)


@app.get("/alcaldias") # by id
async def get_unidades():
    query_request = """
                        SELECT delegation FROM metro_position
                        GROUP BY
                            delegation
                        """
    column_names,query_response = get_query_response(query_request)
    return get_json_response(column_names,query_response)

@app.get("/units/alcaldia/{alcaldia}") # by id
async def get_unidades(alcaldia):
    query_request = """
                        SELECT * FROM metro_position
                        WHERE
                            delegation = '{}'
                        ORDER BY
                            DATE(date_updated)=DATE(NOW()) DESC,
                            DATE(date_updated)<DATE(NOW()) DESC,
                            DATE(date_updated)>DATE(NOW()) ASC
                        """.format(alcaldia)
    column_names,query_response = get_query_response(query_request)
    return get_json_response(column_names,query_response)


def convert_datetime(datetime: Timestamp) -> str:
    """Return timestamp in str format

    Args:
        datetime (Timestamp): date and time

    Returns:
        datetime format ex:06/28/2020 10:05:05
    """
    return datetime.strftime("%m/%d/%Y %H:%M:%S")

def get_query_response(query: str) -> list:
    """This function get data from postgres database and return it

    Args:
        query (str): SQL query

    Returns:
        column_names (list) : name of colums, used to make the dict
        query_response(list[tuple]) : data get by SQL query
    """
    connection,cursor = open_connection()
    cursor.execute(query)
    column_names = [desc[0] for desc in cursor.description]
    query_response = cursor.fetchall()
    cursor.close()
    close_connection(connection)
    return column_names,query_response

def get_json_response(column_names: list,query_response: list) -> str:
    """Transform Dict into Api Body format

    Args:
        column_names (list): name of colums
        query_response (list): data response of query

    Returns:
        api_response (str): return data in json format
    """
    api_response = '{ "response":['
    for response in query_response:
        response = list(response)
        response_dic = dict(zip(column_names,response)) # append two elements in a dict
        if 'date_updated' in response_dic:
            response_dic['date_updated'] = convert_datetime(response_dic['date_updated']) #format datetime
        api_response += json.dumps(response_dic)+','
    api_response = api_response[:-1] + ']}'
    return json.loads(api_response)
