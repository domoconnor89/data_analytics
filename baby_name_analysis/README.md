# Project: USA BABY NAMES ANALYSIS


### Project Description

The US authorities have registered the names of all US citizens born since 1880. The record is publicly available. For data protection reasons, only names that have been used at least 5 times are listed in the data record.

**🎯 Goal:** Design, implement, and present a visualization using the baby names dataset.

## Project Challenges

### Write code to combine datasets for analysis

- Create code that loops over every year in the baby names data folder and combine the datasets into one dataset.
- Define an empty DataFrame with the column names 'names,' 'gender,' 'frequency,' and 'year' as df.
- Loop over each year and apply the `parse_dataset()` function to each year and save it in a variable such as df_temp.
- Within the loop, add a column to df_temp 
- Use the `pd.concat()` function to combine df and df_temp in every iteration until all datasets have been combined into one.
- Save the DataFrame in your data folder for later use.

### Analyzing Names

- Write functions to quickly display interesting insights for any given year.
- Provide a similar anaysis to the above but for any given name.
- Provide a review of naming trends since the year 2000
- What have been the trends for gender ambiguous names over the years?

### Visualize the Names Dataset

- Create a plot which displays the poplarity and gender-neutrality of a series of names, ensuring this is easy to interpret.