import os
import datetime
import urllib
import urllib2
import numpy as np
import matplotlib.mlab as mlab


'''
Downloads the equities information from Yahoo Finance
'''
def yahoo_pull(symbols, start_date, end_date=None, data_path='./data/'):
    #Create path if it doesn't exist
    if not (os.access(data_path, os.F_OK)):
        os.makedirs(data_path)

    #utils.clean_paths(data_path)

    if end_date == None:
        end_date = datetime.datetime.now()

    miss_ctr = 0  # Counts how many symbols we could not get
    for symbol in symbols:
        symbol_name = symbol
        if symbol[0] == '$':
            symbol = '^' + symbol[1:]

        symbol_data = list()
        print "Getting: " + str (symbol_name)

        try:
            params = urllib.urlencode({
                                        's': str(symbol),
                                        'a': start_date.month - 1, 'b': start_date.day, 'c': start_date.year,
                                        'd': end_date.month - 1, 'e': end_date.day, 'f': end_date.year
                                    })
            url_get = urllib2.urlopen("http://ichart.finance.yahoo.com/table.csv?%s" % params)

            header = url_get.readline()
            symbol_data.append(url_get.readline())
            while (len(symbol_data[-1]) > 0):
                symbol_data.append(url_get.readline())

            symbol_data.pop(-1)  # The last element is going to be the string of length zero. We don't want to write that to file.
            # now writing data to file
            f = open(data_path + symbol_name + ".csv", 'w')

            #Writing the header
            f.write(header)

            while (len(symbol_data) > 0):
                f.write(symbol_data.pop(0))

            f.close()
            print "Done: " + str (symbol_name)

        except urllib2.HTTPError:
            miss_ctr = miss_ctr + 1
            print "Unable to fetch data for stock: " + str(symbol_name)
        except urllib2.URLError:
            print "URL Error for stock: " + str(symbol_name)

    print "All done. Got " + str(len(symbols) - miss_ctr) + " stocks. Could not get " + str(miss_ctr) + " stocks."


'''
Get the data of a symbol already downloaded
'''
def get_data(symbol):
    #return genfromtxt('./data/%s.csv' % symbol, delimiter=',', skip_header=1)
    return mlab.csv2rec('./data/%s.csv' % symbol)[::-1] # Reverse

'''
Get only the close column of a symbol
'''
def get_close(symbol):
    return get_data(symbol).adj_close

'''
Completes the data for missing records
Saves the new files
'''
def complete_data(symbols):
    for symbol in symbols:
        complete_data_single(symbol, saveNewFile=True)

'''
Completes the data for missing records can return the array or 
save a new file
'''
def complete_data_single(symbol, saveNewFile=False):
    good_dates = get_data("SPY").date
    data = get_data(symbol)
    dates = data.date
    
    # First check if the records from the first days are missing
    # and fill this data with the record found
    if not(good_dates[0] in dates):
        # First find the most recent values that is on the data
        open_val = data[0][1]
        high = data[0][2]
        low = data[0][3]
        close = data[0][4]
        volume = data[0][5]
        adj_close = data[0][6]
        
        # Then add that record to the beginning until data starts
        # it is necesary to modify the date
        i = 0
        while not(good_dates[i] in dates):
            new = (good_dates[i], open_val, high, low, close, volume, adj_close)
            #n = np.array(most_recent, dtype=data.dtype)
            data = np.insert(data, i, new, 0)  
            i = i + 1

    # TODO: Missing values not onthe beginning

    if saveNewFile:
        try:
            os.remove('./data/%s - old.csv' % symbol)
        except:
            pass
        os.rename('./data/%s.csv' % symbol, './data/%s - old.csv' % symbol)
        mlab.rec2csv(data, './data/%s.csv' % symbol, delimiter=',')

    return data
        

'''
Calculates the daily return for an array
Returns: An array with every return
'''
def daily_return(close):
    daily_ret = 0  # First return is 0
    for i in range(len(close)):
        if i != 0:
            ret = (close[i] / close[i - 1]) - 1
            daily_ret = np.append(daily_ret, ret)

    return daily_ret

'''
Calculates the anual return for an array
Returns: int with the return
'''
def anual_return(close):
    return close[len(close) - 1] / close[0] - 1

'''
Calculates the cumulative return for an array
Returns: array with each cumulative return
'''
def cumulative_return(close):
    init_val = close[0]
    cum_ret = 1  # First return is 100%
    for i in range(len(close)):
        if i != 0:
            ret = (close[i] / init_val)
            cum_ret = np.append(cum_ret, ret)

    return cum_ret

'''
Calculates the average daily return of an array
Return: int with the avg
'''
def avg_daily_return(close):
    return np.average(daily_return(close))

'''
Calculates the standar deviation of the daily return of an array
Return: int with the std
'''
def std_daily_return(close):
    return np.std(daily_return(close), dtype=np.float64)

'''
Calculates the sharpe ratio of an array
Return: int with the sharpe ratio
'''
def sharpe_ratio(close):
    day = daily_return(close)
    avg = np.average(day)
    std = np.std(day, dtype=np.float64)
    return np.sqrt(252) * avg / std

'''
Reads a .txt file and returns the symbols from that file
'''
def read_symbols(s_symbols_file):
    symbols = []
    file = open(s_symbols_file, 'r')
    for f in file.readlines():
        symbols.append(f.strip())
    file.close()

    return symbols

if __name__ == '__main__':
    symbols = ['COG', 'EP', 'BIIB', 'MA', 'ISRG', 'HUM', 'VFC', 'RRC', 'CMD', 'OKE'] # Best stocks for bloomberg
    start_date = datetime.date(2011, 1, 1)
    end_date = datetime.date(2011, 12, 31)
    yahoo_pull(symbols, start_date, end_date, data_path='../data/')
    #complete_data(symbols)
    
    