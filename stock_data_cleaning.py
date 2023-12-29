# THIS SCRIPT PROVIDES A DICTIONARY OF STOCK-PRICE DATAFRAMES FROM A RAW CSV FILE

#VARIABLES TO SET - DEFAULT IS MINUTE AGGREGATION AND CLOSING PRICE
csv_path = 'lowvolstocks.csv' #REPLACE WITH YOUR FILE PATH - CSV SHOULD HAVE DATE, TIME_M, SYM_ROOT, SYM_SUFFIX, SIZE, PRICE (ADDITIONAL COLUMNS ARE OKAY)
time_aggregation = 'T' #REPLACE WITH DESIRED TIME AGGREGATION -  'S' FOR SECOND, 'T' FOR MINUTE, 'H' FOR HOUR, 'D' FOR DAY, 'W' FOR WEEK
price_type = 'closing' #REPLACE WITH DESIRED PRICE TYPE - 'closing' FOR CLOSING PRICE, 'average' FOR VOLUME-WEIGHTED AVERAGE PRICE

#SCRIPT BELOW
import pandas as pd
import datetime as dt
import matplotlib.dates as mdates

unclean_data = pd.read_csv(csv_path)

def split_df_by_stock(data):
    '''Splits the data into individual stocks
    Returns dictionary of dataframes, where each key is the stock's ticker symbol
    '''
    grouped = data.groupby('SYM_ROOT')
    stock_dfs = {stock: group for stock, group in grouped}
    return stock_dfs

def aggregate_df_by_time_frame(data, time_frame, price_type):
    '''Converts into standard format for analysis, aggregating the data by minute
    Assumes timedate does not repeat (ie. assumes data is of one stock)

    INPUTS:
    data: dataframe object with variables TIME_M, DATE, PRICE, SIZE
    time_frame: string object with time frame to aggregate by, 'T' for minute, 'S' for second, 'H' for hour, 'D' for day, 'W' for week
    price_type: string object with price type to aggregate by, 'closing' for last price, 'average' for volume-weighted average price
    '''
    agg_data = data #copy dataframe to avoid mutability issues

    #Create date-time column from DATE and TIME_M columns, ignoring the microseconds data
    agg_data['TIME_M'] = agg_data['TIME_M'].apply(lambda x: x[:7])
    agg_data['DATETIME'] = pd.to_datetime(agg_data['DATE'] + ' ' + agg_data['TIME_M'])
    #Set datetime as index
    agg_data.set_index('DATETIME', inplace=True)

    #IF PRICE_TYPE IS 'closing', aggregate price and size by time_aggregation and remove rows with no volume
    if price_type == 'closing':
        agg_data = agg_data.resample(time_frame).agg({'SIZE': 'sum', 'PRICE': 'last'})
        agg_data = agg_data[agg_data['SIZE'] != 0]
    elif price_type == 'average':
        agg_data['SIZE_PRICE'] = agg_data['SIZE'] * agg_data['PRICE']
        agg_data = agg_data.resample(time_frame).agg({'SIZE': 'sum', 'SIZE_PRICE': 'sum'})
        agg_data = agg_data[agg_data['SIZE'] != 0]
        agg_data['PRICE'] = agg_data['SIZE_PRICE'] / agg_data['SIZE']
    else:
        raise ValueError('price_type must be "closing" or "average"')

    #Remove columns that are not needed
    agg_data = agg_data[['PRICE', 'SIZE']]
    return agg_data

def format_data(unclean_data, time_aggregation, price_type):
    """"Returns a dictionary of formatted dataframes for the time_aggregation and price_type
    """
    stocks_df_dict = split_df_by_stock(unclean_data)
    for stock in stocks_df_dict:
        stocks_df_dict[stock] = aggregate_df_by_time_frame(stocks_df_dict[stock], time_aggregation, price_type)
    return stocks_df_dict

#EXAMPLE USAGE
stocks_df_dict = format_data(unclean_data, time_aggregation, price_type)
print('Johnson and Johnson Stock:', stocks_df_dict['JNJ'].head())
print('Merck and Co Stock:', stocks_df_dict['MRK'].head())