import csv
import itertools
from utils import *
import numpy as np


'''
Creates a fund with the given symbols and weights
Returns: array with the daily investment for the fund
'''
def fund(symbols, weights):
    ans = 0
    i = 0
    for symbol in symbols:
        cumu = cumulative_return(get_close(symbol))
        investment = np.multiply(cumu, weights[i])
        ans = np.add(ans, investment)
        i = i + 1

    return ans

'''
Combinates the given symbols and find the one with the highest sharpe ratio
Return: Winner [symbols, weights, sharpe_ratio]
'''
def combine4(symbols, debugPercent=False, debugPercentValue=0.1, debugWinners=False):
    # Create a matrix, on each row there is the info of one equity
    data = np.array(get_close(symbols[0]))
    for symbol in symbols:
        if symbol != symbols[0]:
            n = np.array(get_close(symbol))
            data = np.vstack((data, n))

    # Get the combinations of the stocks, order doesnt matter
    combinations = list(itertools.combinations(symbols, 4))

    # Get the permutation of the weights, order is important
    weights = []
    #weights = weights + list(set(itertools.permutations([1, 0, 0, 0])))
    #weights = weights + list(set(itertools.permutations([0.9, 0.1, 0, 0])))
    #weights = weights + list(set(itertools.permutations([0.8, 0.2, 0, 0])))
    #weights = weights + list(set(itertools.permutations([0.8, 0.1, 0.1, 0])))
    weights = weights + list(set(itertools.permutations([0.8, 0.1, 0.05, 0.05])))
    #weights = weights + list(set(itertools.permutations([0.7, 0.3, 0, 0])))
    #weights = weights + list(set(itertools.permutations([0.7, 0.2, 0.1, 0])))
    weights = weights + list(set(itertools.permutations([0.7, 0.1, 0.1, 0.1])))
    #weights = weights + list(set(itertools.permutations([0.6, 0.4, 0, 0])))
    #weights = weights + list(set(itertools.permutations([0.6, 0.3, 0.1, 0])))
    weights = weights + list(set(itertools.permutations([0.6, 0.3, 0.05, 0.05])))
    #weights = weights + list(set(itertools.permutations([0.6, 0.2, 0.2, 0])))
    weights = weights + list(set(itertools.permutations([0.6, 0.2, 0.1, 0.1])))
    #weights = weights + list(set(itertools.permutations([0.5, 0.4, 0.1, 0])))
    weights = weights + list(set(itertools.permutations([0.5, 0.4, 0.05, 0.05])))
    #weights = weights + list(set(itertools.permutations([0.5, 0.3, 0.2, 0])))
    weights = weights + list(set(itertools.permutations([0.5, 0.3, 0.1, 0.1])))
    weights = weights + list(set(itertools.permutations([0.5, 0.2, 0.2, 0.1])))
    weights = weights + list(set(itertools.permutations([0.25, 0.25, 0.25, 0.25])))
    weights = weights + list(set(itertools.permutations([0.3, 0.3, 0.2, 0.2])))
    num_iterations = len(combinations) * len(weights)
    print "# Iterations: %s" % num_iterations

    # Loop
    winner = []
    winner_s = 0
    it = 0
    percent_complete = num_iterations * debugPercentValue # To see how the process is going
    if debugPercent == True:
        print "Starting..."
    for combination in combinations:
        # Get the rows for each symbol of the combination to filter the matrix
        rows = []
        for item in combination:
            rows = rows + [symbols.index(item)]

        for weight in weights:
            # Print each 10% to see how is going
            if debugPercent == True:
                it = it + 1
                if it > percent_complete:
                    print "%s percent complete" % (100 * percent_complete / num_iterations)
                    percent_complete = percent_complete + (num_iterations * debugPercentValue)


            # Create a fund with the selected equities / rows
            fund = 0
            i = 0
            for row in rows:
                cumu = cumulative_return(data[row])
                investment = np.multiply(cumu, weight[i])
                fund = np.add(fund, investment)
                i = i + 1

            # Calculate the sharpe ratio and see if is higher that the previous
            s_new = sharpe_ratio(fund)
            
            if s_new > winner_s:
                winner = combination
                winner_weight = weight
                winner_s = s_new
                if debugWinners == True:
                    print "%s w/ %s = %s - NEW WINNER" % (str(winner), str(winner_weight), str(winner_s))
            else:
                pass
                #print "%s w/ %s = %s" % (str(combination), str(weight), str(s_new))

    if debugPercent == True:
        print "100 percent complete"
    return [winner, winner_weight, winner_s]

'''
Creates a fund_report.csv file with the information of a fund created by the symbols and weights
'''
def fund_report(symbols, weights):
    ammount = 1000000
    # Get the close values of each equity
    close = list(np.array(get_close(symbols[0])))
    for symbol in symbols:
        if symbol != symbols[0]:
            n = np.array(get_close(symbol))
            close = close.append(n)

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
    fund_cumu = cumulative_return(fund_inv)
    fund_daily = daily_return(fund_inv)

    # --------------------------------------
    # Write the file
    csv_file = csv.writer(open("fund_report.csv", "wb"))

    # Create the header
    row = []
    for symbol in symbols:
        row.append(symbol)
        row.append(symbol + " cumu_ret")
        row.append(symbol + " investment")

    row.append("Fund Invest")
    row.append("Fund cumu_ret")
    row.append("Fund daily_ret")
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
        row.append(fund_cumu[i])
        row.append(fund_daily[i])
        # Write the row
        csv_file.writerow(row)

    # Write the summary
    csv_file.writerow('')

    for i in range(len(symbols)):
        csv_file.writerow([symbols[i] + " weight: ", weights[i]])

    csv_file.writerow('')

    csv_file.writerow(['Annual return', anual_return(fund_inv)])
    csv_file.writerow(['AVG Daily return', avg_daily_return(fund_inv)])
    csv_file.writerow(['STD Daily return', std_daily_return(fund_inv)])
    csv_file.writerow(['Sharpe ratio', sharpe_ratio(fund_inv)])


if __name__ == '__main__':
    #symbols = read_symbols("symbols.txt")
    symbols = ['CNC', 'TRGP', 'ROST', 'OKE', 'HUM', 'VFC', 'BIIB', 'MA', 'WCG']
    symbols = ['CNC', 'ROST', 'OKE', 'BIIB'] # Best from previous line
    symbols = ['HDGE', 'AGOL', 'GGGG' ,'SDIV', 'FWDB', 'NKY'] # Best EFT from a site
    symbols = ['AGOL', 'GGGG', 'SDIV', 'NKY'] # Best from previous line
    symbols = ['CNC', 'TRGP', 'ROST', 'OKE', 'HUM', 'VFC', 'BIIB', 'MA', 'WCG', "AAPL", "GLD"]
    symbols = ['ROST', 'OKE', 'BIIB', 'GLD'] # Best from previous line
    symbols = ['BIIB', 'PFE', 'BMY', 'D', 'PM', 'GLD'] # Best stocks for bloomberg
    # [('BIIB', 'BMY', 'PM', 'GLD'), (0.10000000000000001, 0.5, 0.20000000000000001, 0.20000000000000001), 2.1376875820661292] 
    symbols = ['BBH', 'IHE', 'PJP', 'XLU', 'VPU', 'IDU', 'FXG', 'PPH', 'XLP', 'VDC'] # Best ETF stocks for bloomberg
    print combine4(symbols, debugPercent=True, debugPercentValue=0.1, debugWinners=True)
    #fund_report(symbols, [0.3, 0.3, 0.2, 0.2])










