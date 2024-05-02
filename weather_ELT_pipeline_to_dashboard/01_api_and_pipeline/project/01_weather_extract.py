import requests
import os
from dotenv import load_dotenv
load_dotenv()
import pandas as pd
import json
import datetime
from sqlalchemy.dialects.postgresql import JSON as postgres_json
from sqlalchemy import create_engine, types, text
from sqlalchemy_utils import database_exists, create_database

# load .env
load_dotenv()

#load your .env file and read the api key for weather api
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
db_user = os.getenv('POSTGRES_USER')
db_pw = os.getenv('POSTGRES_PW')
host = os.getenv('POSTGRES_HOST')
db = os.getenv('DB_CLIMATE')

# creating url and the engine
url = f"postgresql://{db_user}:{db_pw}@{host}/{db}"

engine = create_engine(url)

cities = ['Marvejols, France', 'Ansbach, Germany', 'Morgan City, Louisiana',
          'Lerwick, Shetland Islands', 'Bedburg, Germany', 'London, UK',
          'Dao Capiz, Philippines', 'Argos, Peloponnese, Greece', 
          'window rock, arizona', 'Pamir Post, Tajikistan']

data_rows = []


for city in cities:
    
    #climate_data[city] = {}
    
    for day in pd.date_range(start='10/12/2022', end='10/12/2023'):
    
        api_url = f"http://api.weatherapi.com/v1/history.json?key={WEATHER_API_KEY}&q={city}&dt={day.date()}"
        response = requests.request("GET", api_url)
        result = json.loads(response.text)

        if response.status_code == 200:
            data_rows.append({
                'extracted_at': datetime.datetime.now(),
                'extracted_data': result
            })
        else:
            print(f'data couldn\'t be loaded from api {(response.reason, response.status_code)}')

# make it a dataframe
climate_df = pd.DataFrame(data_rows)

# creating database or checking if it already there
if not database_exists(engine.url):
    create_database(engine.url)

print(f'database exists? {database_exists(engine.url)}')

# define data types for table in DB
dtype_dict = {'extracted_at':types.DateTime,
              'extracted_data':postgres_json}

# importing data into the table 'raw_temp' in the database
climate_df.to_sql('raw_temp', con=engine, if_exists='append', dtype=dtype_dict)


    ## LOCATIONS ##
# Marvejols, France: The Beast of Gevaudan, France
# Ansbach, Germany: The Wolf of Ansbach, Germany
# Morgan City, Louisiana, USA: The Legend of the Rougarou, Louisiana, USA
# Lerwick, Shetland Islands: The Wulver of Shetland, Scotland
# Bedburg, Germany: The Werewolf of Bedburg, Germany
# London, UK: An American Werewolf in London
# Dao Capiz, Philippines: Aswang, Philippines
# Argos, Peloponnese, Greece: Lycanthropy in Ancient Greece
# window rock, arizona: Skin-walkers, Navajo Nation (Southwestern United States)
# Pamir Post, Tajikistan: Nüwa and Fuxi, Chinese Mythology