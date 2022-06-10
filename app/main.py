import requests
from database_sender import *
from geopy.geocoders import Nominatim

api_url ="https://datos.cdmx.gob.mx/api/3/action/datastore_search?resource_id=ad360a0e-b42f-482c-af12-1fd72140032e&limit=300"
response = requests.get(api_url)
data_response= response.json()


def get_address(coordinates: str ) -> dict :
    """
    Parameters
    ----------
    coordinates: str
        example: '19.2926006317,-99.1774978638'
    ----------
    Returns
    -------
    address of the given coordinates in a dict format {'road':value, 'neighbourhood': value ....}
    """
    geoLoc = Nominatim(user_agent="GetLoc")
    locname = geoLoc.reverse(coordinates)
    key = 'road,neighbourhood,delegation,state,postal_Code,Country'
    keys = key.split(',')
    values = locname.address.split(',')
    address_names = {}
    for i in range(0,-abs(len(keys)),-1):
        key = keys[i].strip()
        value = values[i].strip()
        address_names[key]=value
    return keys,address_names

def append_address():
    """
    this function its used to append the address of a given coordinate
    """
    records = data_response['result']['records']
    for i in range(len(records)):
        address_keys,address_names = get_address(records[i]['geographic_point'])
        for x in range (len(address_names)):
            records[i][address_keys[x]] = address_names[address_keys[x]]
        insert_metro_values(records[i])

if __name__ == "__main__":
    create_table()
    append_address()
    print("PENEEEE")
