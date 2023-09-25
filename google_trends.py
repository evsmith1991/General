#install pytrends
!pip install pytrends
#import the libraries
import pandas as pd
from pytrends.request import TrendReq
pytrend = TrendReq()
# Get Google Keyword Suggestions
keywords = pytrend.suggestions(keyword='Personal Finance')
df = pd.DataFrame(keywords)
df.head(5)

#import the libraries
import pandas as pd
from pytrends.request import TrendReq
pytrend = TrendReq()

#get today's treniding topics
trendingtoday = pytrend.today_searches(pn='US')
trendingtoday.head(20)

# Get Google Top Charts
df = pytrend.top_charts(2022, hl='en-US', tz=300, geo='US') #geo='GLOBAL'
df.head()

#import the libraries
import pandas as pd                        
from pytrends.request import TrendReq
pytrend = TrendReq()

#provide your search terms
kw_list=['APY', 'HSA', 'Retirement', 'high yield', '529']

#search interest per region
#run model for keywords (can also be competitors)
pytrend.build_payload(kw_list, timeframe='today 1-m')

# Interest by Region
regiondf = pytrend.interest_by_region()
#looking at rows where all values are not equal to 0
regiondf = regiondf[(regiondf != 0).all(1)]

#drop all rows that have null values in all columns
regiondf.dropna(how='all',axis=0, inplace=True)

#visualise
regiondf.plot(figsize=(20, 12), y=kw_list, kind ='bar')

#import the libraries
import pandas as pd                        
from pytrends.request import TrendReq
pytrend = TrendReq()

#provide your search terms
#kw_list=['APY', 'HSA', 'Retirement', 'high yield', '529']
kw_list=['etf']

#historical interest
historicaldf = pytrend.get_historical_interest(kw_list, year_start=2020, month_start=10, day_start=1, hour_start=0, year_end=2021, month_end=10, day_end=1, hour_end=0, cat=0, geo='US', gprop='', sleep=0)

#visualise
#plot a timeseries chart
historicaldf.plot(figsize=(20, 12))

#plot seperate graphs, using theprovided keywords
historicaldf.plot(subplots=True, figsize=(20, 12))

#get interest by region for your search terms
pytrend.build_payload(kw_list=kw_list)
df = pytrend.interest_by_region()
df.head(200)

# Get realtime Google Trends data
df = pytrend.trending_searches(pn='united_states')
df.head()

#get related queries
related_queries = pytrend.related_queries()
related_queries.values()

#build lists dataframes

top = list(related_queries.values())[0]['top']
rising = list(related_queries.values())[0]['rising']

#convert lists to dataframes

dftop = pd.DataFrame(top)
dfrising = pd.DataFrame(rising)

#join two data frames
joindfs = [dftop, dfrising]
allqueries = pd.concat(joindfs, axis=1)

#function to change duplicates

cols=pd.Series(allqueries.columns)
for dup in allqueries.columns[allqueries.columns.duplicated(keep=False)]: 
    cols[allqueries.columns.get_loc(dup)] = ([dup + '.' + str(d_idx) 
                                     if d_idx != 0 
                                     else dup 
                                     for d_idx in range(allqueries.columns.get_loc(dup).sum())]
                                    )
allqueries.columns=cols

#rename to proper names

allqueries.rename({'query': 'top query', 'value': 'top query value', 'query.1': 'rising query', 'value.1': 'rising query value'}, axis=1, inplace=True) 

#check your dataset
allqueries.head(50)

#save to csv
#allqueries.to_csv('allqueries.csv')

#download from collab
#files.download("allqueries.csv")

# Related Topics, returns a dictionary of dataframes
related_topic = pytrend.related_topics()
related_topic.values()

from pytrends.request import TrendReq

# Initialize pytrends
pytrends = TrendReq(hl='en-US', tz=360)

# Define the search term
kw_list = ["personal finance"]

# Use pytrends to get Google Trends data
pytrends.build_payload(kw_list, timeframe='today 5-y', geo='US')

# Get Google Keyword Suggestions
suggestions = pytrends.suggestions(keyword='personal finance')

# Print the first 5 suggestions
for i in range(min(5, len(suggestions))):
    print(suggestions[i]['title'], '-', suggestions[i]['type'])


from pytrends.request import TrendReq
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from pandas.plotting import register_matplotlib_converters

# Required for pandas to plot datetime values with matplotlib
register_matplotlib_converters()

# Initialize pytrends
pytrends = TrendReq(hl='en-US', tz=360)

# Define the search terms
kw_list = ['HSA', 'IRA', 'Roth IRA', '529 plan', 'impact investing']

# Get Google Trends data
pytrends.build_payload(kw_list, timeframe='today 5-y', geo='US')
data = pytrends.interest_over_time()

# Drop the 'isPartial' column
data.drop(columns=['isPartial'], inplace=True)

# Plot the data
data.plot(figsize=(14,7))
plt.title('Google Search Volume Over Last 5 Years')
plt.ylabel('Relative Search Volume')
plt.xlabel('Date')
plt.grid(True)
plt.show()

# Define the forecasting period (5 years = 52 weeks/year * 5)
forecasting_period = 52 * 5

# Forecast for each term
for term in kw_list:
    # Initialize the model
    model = SARIMAX(data[term], order=(1, 1, 1), seasonal_order=(1, 1, 0, 52))
    model_fit = model.fit(disp=False)

    # Make predictions
    forecast = model_fit.predict(len(data), len(data) + forecasting_period)
    forecast.index = pd.date_range(start=data.index[-1], periods = forecasting_period+2, freq='W')[1:]

    # Plot the forecast
    plt.figure(figsize=(14,7))
    plt.plot(data[term])
    plt.plot(forecast)
    plt.title(f'Google Search Volume Forecast for "{term}" Over Next 5 Years')
    plt.ylabel('Relative Search Volume')
    plt.xlabel('Date')
    plt.grid(True)
    plt.show()

from pytrends.request import TrendReq
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from pandas.plotting import register_matplotlib_converters

# Required for pandas to plot datetime values with matplotlib
register_matplotlib_converters()

# Initialize pytrends
pytrends = TrendReq(hl='en-US', tz=360)

# Define the search terms
kw_list = ['HSA', 'IRA', 'Roth IRA', '529 plan', 'values-based investing']

# Get Google Trends data
pytrends.build_payload(kw_list, timeframe='today 5-y', geo='US')
data = pytrends.interest_over_time()

# Drop the 'isPartial' column
data.drop(columns=['isPartial'], inplace=True)

# Plot the data
data.plot(figsize=(14,7))
plt.title('Google Search Volume Over Last 5 Years')
plt.ylabel('Relative Search Volume')
plt.xlabel('Date')
plt.grid(True)
plt.show()

# Define the forecasting period (5 years = 52 weeks/year * 5)
forecasting_period = 52 * 5

# Create a new DataFrame to store the forecasts
forecasts = pd.DataFrame()

# Forecast for each term
for term in kw_list:
    # Initialize the model
    model = SARIMAX(data[term], order=(1, 1, 1), seasonal_order=(1, 1, 0, 52))
    model_fit = model.fit(disp=False)

    # Make predictions
    forecast = model_fit.predict(len(data), len(data) + forecasting_period)
    forecast.index = pd.date_range(start=data.index[-1], periods = forecasting_period+2, freq='W')[1:]

    # Store the forecast in the forecasts DataFrame
    forecasts[term] = forecast

# Plot the forecast
plt.figure(figsize=(14,7))
for term in kw_list:
    plt.plot(data[term])
    plt.plot(forecasts[term])
plt.title('Google Search Volume Forecasts Over Next 5 Years')
plt.ylabel('Relative Search Volume')
plt.xlabel('Date')
plt.legend(kw_list)
plt.grid(True)
plt.show()
