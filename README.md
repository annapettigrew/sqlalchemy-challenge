# sqlalchemy-challenge


# Using Python and SQLAlchemy to perform basic climate analysis and data exploration of the climate database.

##Part 1: Climate Analysis and Exploration

###Used the provided starter notebook and hawaii.sqlite files to complete the climate analysis and data exploration.
###Used SQLAlchemy’s create_engine to connect to the SQLite database.
###Used SQLAlchemy’s automap_base() to reflect the tables into classes and saved a reference to those classes
###Linked Python to the database by creating a SQLAlchemy session.

##Precipitation Analysis

###Found the most recent date in the dataset.
###Retrieved the previous 12 months of precipitation data by querying the 12 previous months of data. 
###Selected only the date and prcp values.
###Loaded the query results into a Pandas DataFrame, and set the index to the date column.
###Sorted the DataFrame values by date.
###Ploted the results by using the DataFrame plot method

##Station Analysis

###Designed a query to calculate the total number of stations in the dataset.
###Designed a query to find the most active stations (the stations with the most rows).
###Listed the stations and observation counts in descending order.
###Used the most active station id, to calculate the lowest, highest, and average temperatures.
###Designed a query to retrieve the previous 12 months of temperature observation data (TOBS).
###Filtered by the station with the highest number of observations.
###Queried the previous 12 months of temperature observation data for this station.
###Ploted the results as a histogram with bins=12


##Design the Climate App

###After completing the initial analysis,I designed a Flask API based on the queries I developed.
