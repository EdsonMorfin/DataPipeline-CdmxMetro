# DataPipeline-CdmxMetro
A basic data pipeline using CDMX api:https://datos.cdmx.gob.mx/dataset/prueba_fetchdata_metrobus/resource/ad360a0e-b42f-482c-af12-1fd72140032e?view_id=75155643-88fc-4a58-8467-6df728426396 
It gets the position of CDMX Metro with his Delegation 

## How to install it
- Install libraries with `pip install requirements.txt`
- run main.py #ONCE 
- run api server with `uvicorn api_metro:app --reload`

## Endpoints
 Get all Metro units:
 - http://127.0.0.1:8000/units 

 Get single Metro unit with given Id:
 - http://127.0.0.1:8000/unit/{id}

 Get Availabable Alcaldias:
 - http://127.0.0.1:8000/alcaldias
 
 Get Metro units that are in certain alcaldia with given name:
 - http://127.0.0.1:8000/units/alcaldia/{alcaldia_name}


