# Project: ELT PIPELINE TO ONLINE DASHBOARD USING THE WEATHER API

### Project Description

**🎯 Goal:** 
Construct ELT data pipeline using python, pandas, more advanced SQL, SQLalchemy, and dbt.
Design and deploy a web app with using dash.

## Project Challenges

Connect a database with Python and design a pipeline. Next, automate the pipeline and connect the data to a Dashboard to visualize the results.

Work with a large, messy, real-world dataset using the Weather API, which contains daily temperature records from all over the world. 

Design interactive charts and maps to create an interactive web app, using dash and deploying with render!

### <ins>Identify Data Sources</ins>
- Access data from real world API using a python script (www.weatherapi.com)

### <ins>Retrieve Data</ins>
- Querying the API and using SQLalchemy and import raw data into postgres database
- Setting logging in order to catch problems and log successes
- Connect database to dbt cloud - which will be used to parse and prepare the data

### <ins>Data Wrangling, Exploration and Cleaning</ins>
- Use Common Table Expressions in SQL
- Clean and prepare the data on dbt cloud using CTE and the power of dbt
- Prepare data marts that will be used to answer stakeholders questions
- Create dataframes out of the datamarts
- Filter the dataframes for the graphs needed for the dashboard

### <ins>Analyze Data</ins>
- Use interactive visualizations to analyze data

### <ins>Present Data to Stakeholders</ins>
- Create interactive temperature bar plots for different locations using plotly
- Create an interactive climate map with plotly
- Create a web app using dash
- Integrate these interactive visuals into dash
- Deploy the dash app to share it via link
