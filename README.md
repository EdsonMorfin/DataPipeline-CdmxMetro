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

## State machine diagram
![Untitled](https://user-images.githubusercontent.com/73849076/173126970-b5ae6246-8085-4e51-a5f5-e045ff22c946.png)

## Data Modeling
 ERD
![image](https://user-images.githubusercontent.com/73849076/173127994-1c6c17bd-0e36-48f9-9f1c-bbdb2d1d1522.png)
DLL
![image](https://user-images.githubusercontent.com/73849076/173128212-e3183d7b-34fe-4526-a9bc-bef5ebd378ec.png)
![image](https://user-images.githubusercontent.com/73849076/173128337-0767fb7f-a1b6-4192-ad59-61cd0a11342a.png)






