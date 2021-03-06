import csv
import itertools
import numpy as np
from utils.stock import *
from utils.log import PercentPrinter


'''
Creates a fund with the given symbols and weights
Returns: array with the daily investment for the fund
'''
def fund(symbols, weights):
    ans = 0
    for symbol, i in zip(symbols, range(len(symbols))):
        cumu = cumulative_return(get_close(symbol))
        investment = np.multiply(cumu, weights[i])
        ans = np.add(ans, investment)

    return ans

'''
Combinates the given symbols and find the one with the highest sharpe ratio
Return: Winner [symbols, weights, sharpe_ratio]
'''
def combine4(symbols, printPercent=False, printPercentValue=0.1, debugWinners=False):
    # Create a matrix, on each row there is the close price of one equity
    data = np.array(get_close(symbols[0]))
    for symbol in symbols:
        if symbol != symbols[0]:
            n = np.array(get_close(symbol))
            data = np.vstack((data, n))

    # Get the combinations of the stocks, order doesnt matter
    combinations = list(itertools.combinations(symbols, 4))

    # Get the permutation of the weights, order is important
    weights_list = []
    #weights_list = weights_list + list(set(itertools.permutations([1, 0, 0, 0])))
    #weights_list = weights_list + list(set(itertools.permutations([0.9, 0.1, 0, 0])))
    #weights_list = weights_list + list(set(itertools.permutations([0.8, 0.2, 0, 0])))
    #weights_list = weights_list + list(set(itertools.permutations([0.8, 0.1, 0.1, 0])))
    weights_list = weights_list + list(set(itertools.permutations([0.8, 0.1, 0.05, 0.05])))
    #weights_list = weights_list + list(set(itertools.permutations([0.7, 0.3, 0, 0])))
    #weights_list = weights_list + list(set(itertools.permutations([0.7, 0.2, 0.1, 0])))
    weights_list = weights_list + list(set(itertools.permutations([0.7, 0.1, 0.1, 0.1])))
    #weights_list = weights_list + list(set(itertools.permutations([0.6, 0.4, 0, 0])))
    #weights_list = weights_list + list(set(itertools.permutations([0.6, 0.3, 0.1, 0])))
    weights_list = weights_list + list(set(itertools.permutations([0.6, 0.3, 0.05, 0.05])))
    #weights_list = weights_list + list(set(itertools.permutations([0.6, 0.2, 0.2, 0])))
    weights_list = weights_list + list(set(itertools.permutations([0.6, 0.2, 0.1, 0.1])))
    #weights_list = weights_list + list(set(itertools.permutations([0.5, 0.4, 0.1, 0])))
    weights_list = weights_list + list(set(itertools.permutations([0.5, 0.4, 0.05, 0.05])))
    #weights_list = weights_list + list(set(itertools.permutations([0.5, 0.3, 0.2, 0])))
    weights_list = weights_list + list(set(itertools.permutations([0.5, 0.3, 0.1, 0.1])))
    weights_list = weights_list + list(set(itertools.permutations([0.5, 0.2, 0.2, 0.1])))
    weights_list = weights_list + list(set(itertools.permutations([0.25, 0.25, 0.25, 0.25])))
    weights_list = weights_list + list(set(itertools.permutations([0.3, 0.3, 0.2, 0.2])))
    num_iterations = len(combinations) * len(weights_list)

    # Loop
    winner, winner_s = [], 0

    if printPercent:
        percentPrinter = PercentPrinter(num_iterations, printPercentValue)
        
    for combination in combinations:
        # Get the rows number for each symbol of the combination to filter the matrix
        rows = []
        for item in combination:
           rows = rows + [symbols.index(item)]

        for weights in weights_list:
            # Print each X% to see how is going
            if printPercent:
                percentPrinter.next()

            # Create a fund with the selected equities / rows
            portfolio = 0
            for row, weight in zip(rows, weights):
                cumu = cumulative_return(data[row])
                investment = np.multiply(cumu, weight)
                portfolio = np.add(portfolio, investment)

            # Calculate the sharpe ratio and see if is higher that the previous
            s_new = sharpe_ratio(portfolio)
            
            if s_new > winner_s:
                winner = combination
                winner_weights = weights
                winner_s = s_new

                if debugWinners:
                    print "%s w/ %s = %s - NEW WINNER" % (str(winner), str(winner_weights), str(winner_s))
    
    return [winner, winner_weights, winner_s]

'''
Creates a fund_report.csv file with the information of a fund created by the symbols and weights
'''
def fund_report(symbols, weights):
    ammount = 1000000
    # Get the close values of each equity
    close = np.array(get_close(symbols[0]))
    for symbol in symbols:
        if symbol != symbols[0]:
            n = np.array(get_close(symbol))
            close = np.vstack((close, n))

    # Get the cumu_ret of each equity
    cumu_ret = np.array(cumulative_return(close[0]))
    for i in range(len(symbols)):
        if i != 0:
            n = np.array(cumulative_return(close[i]))
            cumu_ret = np.vstack((cumu_ret, n))

    # Get the inv of each equity
    inv = np.array(cumulative_return(close[0]))
    inv = np.multiply(inv, ammount * weights[0])

    for i in range(len(symbols)):
        if i != 0:
            n = np.array(cumulative_return(close[i]))
            n = np.multiply(n, ammount * weights[i])
            inv = np.vstack((inv, n))

    # Get the values for the fun
    fund_inv = fund(symbols, weights)
    fund_inv = np.multiply(fund_inv, ammount)
    #fund_cumu = cumulative_return(fund_inv)
    fund_daily = daily_return(fund_inv)

    # --------------------------------------
    # Write the file
    csv_file = csv.writer(open("fund_report.csv", "wb"))

    # Create the header
    row = []
    for symbol in symbols:
        row.append(symbol)
        row.append(symbol + " Cumulative Return")
        row.append(symbol + " Investment")

    row.append("Portfolio ")
    #row.append("Portfolio cumu_ret")
    row.append("Portfolio Daily Return")
    csv_file.writerow(row)

    for i in range(len(close[0])):
        row = []
        # Add the values of each equity
        for j in range(len(symbols)):
            row.append(close[j][i])
            row.append(cumu_ret[j][i])
            row.append(inv[j][i])
        # Add the values of the fund
        row.append(fund_inv[i])
        #row.append(fund_cumu[i])
        row.append(fund_daily[i])
        # Write the row
        csv_file.writerow(row)

    # Write the summary
    csv_file.writerow('')
    ammount = 1000000
    csv_file.writerow(['Ammount', ammount])
    csv_file.writerow(['Equity', 'Price', 'Percentage', '# Shares'])

    for weight, i in zip(weights, range(len(symbols))):
        price = close[i][0]
        csv_file.writerow([symbols[i], price, weight, (ammount * weight / price)])

    csv_file.writerow('')

    csv_file.writerow(['Annual return', anual_return(fund_inv)])
    csv_file.writerow(['AVG Daily return', avg_daily_return(fund_inv)])
    csv_file.writerow(['STD Daily return', std_daily_return(fund_inv)])
    csv_file.writerow(['Sharpe ratio', sharpe_ratio(fund_inv)])


if __name__ == '__main__':
    #symbols = read_symbols("symbols.txt")
    symbols = ['CNC', 'TRGP', 'ROST', 'OKE', 'HUM', 'VFC', 'BIIB', 'MA', 'WCG'] # Best stocks from a site
    symbols = ['CNC', 'ROST', 'OKE', 'BIIB'] # Best from previous line ******
    
    symbols = ['CNC', 'TRGP', 'ROST', 'OKE', 'HUM', 'VFC', 'BIIB', 'MA', 'WCG', "AAPL", "GLD"] # Same as 1 but with AAPL and GLD
    symbols = ['ROST', 'OKE', 'BIIB', 'GLD'] # Best from previous line
    
    symbols = ['BIIB', 'PFE', 'BMY', 'D', 'PM', 'GLD'] # Best stocks on EFT for bloomberg w/ GLD
    
    symbols = ['IHE', 'PJP', 'XLU', 'VPU', 'IDU', 'FXG', 'XLP', 'VDC'] # Best ETF stocks for bloomberg
    symbols = ['IHE', 'PJP', 'XLU', 'VPU'] # Best from previous line ('IHE', 'PJP', 'XLU', 'VPU')
    
    symbols = ['COG', 'EP', 'BIIB', 'MA', 'ISRG', 'HUM', 'VFC', 'RRC', 'CMD', 'OKE'] # Best stocks for bloomberg
    symbols = ['EP', 'ISRG', 'CMD', 'OKE'] # Best from previous line
    
    #ans = combine4(symbols, printPercent=True, printPercentValue=0.5, debugWinners=False)
    ans = [('EP', 'ISRG', 'CMD', 'OKE'), (0.1, 0.1, 0.3, 0.5), 2.6618132161761916]
    print ans
    fund_report(ans[0], ans[1])










