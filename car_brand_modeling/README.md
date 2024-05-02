# Project: PREDICTIVE MODELLING AND CLUSTERING OF CAR BRANDS

### Project Description

Develop a predictive model using linear regression to estimate the MSRP of cars based on their features. The data used comes from Kaggle and it describes almost 12000 car models sold in the United States between 1990 and 2018.

Understanding the factors that influence car pricing is essential for both sellers and buyers. Several factors determine vehicle value so by analyzing these features and their impact on MSRP (Manufacturer’s Suggested Retail Price), we can build a model that provides reliable price estimations.

**🎯 Goal:**  Explore the Cars data and fit a regression line to it. 

## Project Challenges

### EDA

- Clean the data
- Split the dataframe into training and test data
- Analyse the training data, examining its various features, distributions, and patterns

### Linear Regression

- Subset the train dataframe to extract the numerical columns.
- Generate a heatmap of the subset dataframe to indentify the feature which has the highest correlation to the price column.
- Build a simple linear regression model with price as the identified target variable.
- Add extra features with high correlation to the price. Observe and explain how R2 changes.

### Feature Engineering

- Impute and drop missing values for both the train and test datasets.
- Apply one-hot encoder to the categorical subset of the train dataset.
- Add numerical features to the encoded dataframe.
- Build a linear regression model using the encoded categorical and numerical features.
- Make predictions and plot predicted and actual values in one scatter plot.
- Apply `StandardScaler()` to the numerical subset of the train dataset.
- Create a dataframe with encoded categorical and scaled numerical features for train dataset.
- Build a new linear regression model using the encoded categorical and scaled numerical features.

### Clustering
- Analyse clusters to gain a deeper understanding of the market landscape and identify target customer segments with similar preferences and needs.
- Check the distribution of data and standardize.
- Use the elbow method to determine the number of clusters.
- Repeat k-means clustering using the appropriate number of clusters selected from the elbow method. 
- Visualize the results.
