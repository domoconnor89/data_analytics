## Getting API credentials (API-Key) ready:

- Create a login at the weatherapi [https://www.weatherapi.com/pricing.aspx]

- Check out the metrics available in the History API.

- Create a .env file for your project with the API Keys. 
    - ***Tip:*** Save the .env file at the highest level within the repo ... as long as the file is in a higher hirarchy folder dotenv will find it.

- Make sure the .env file contains the API Key that you registered at weatherapi.com and other DB credentials:

```python
WEATHER_API = 'xxxxxxxxxxxxxxxxx' # input actual API-key

POSTGRES_USER = 'postgres'
POSTGRES_PW = '¡123?abc!' # input actual password
POSTGRES_HOST = '00.000.000.00' # input actual host
POSTGRES_PORT = '5432'

DB_CLIMATE = 'climate'
```


